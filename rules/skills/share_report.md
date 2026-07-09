# Skill: Share Report to Web

Convert a Markdown report to HTML, publish it to <your-domain>/share, and return an accessible URL.

## When to Use

Trigger this skill when the user says things like:
- "Help me share this report"
- "Publish this"
- "Share it"
- "Give me a link"
- Any request to share a Markdown file for others to read

## Prerequisites

- pandoc is installed (local `/opt/homebrew/bin/pandoc`)
- Passwordless SSH to `<your-server>` is configured
- CSS template is at `tools/share_report.css`
- GA4 tracking snippet is at `tools/share_report_ga4.html`
- TTS narration snippet is at `tools/share_report_tts.html`
- Local project directory: `adhoc_jobs/yage_share/` (contains manifest.json, gen_index.py, site/)

## Usage

### H1 Deduplication (Required Reading)

`--metadata title` makes pandoc automatically generate an `<h1>`. If the first line of the Markdown file is also `# Title`, the HTML will contain two h1 elements. **Before publishing, remove the `# ` line from the Markdown file** and provide the h1 only through metadata title:

```bash
# Remove the first-line # Title and generate a temporary file
tail -n +2 <input.md> > /tmp/<slug>_no_h1.md
# Use /tmp/<slug>_no_h1.md as the input for the following pandoc command
```

### Complete Publishing Flow

#### Step 1: Generate SEO Meta Snippet

Based on the article content, generate a temporary HTML snippet file `/tmp/<slug>_seo.html` containing:

```html
<meta name="description" content="<article summary under 150 characters>">
<meta name="author" content="<your-name>">
<meta property="og:title" content="<report title>">
<meta property="og:description" content="<article summary under 150 characters>">
<meta property="og:url" content="https://<your-domain>/share/<slug>.html">
<meta property="og:type" content="article">
<meta property="article:published_time" content="<YYYY-MM-DD>">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="<report title>">
<meta name="twitter:description" content="<article summary under 150 characters>">
<link rel="canonical" href="https://<your-domain>/share/<slug>.html">
```

#### Step 2: Convert with pandoc (SEO + GA4 + TTS)

```bash
pandoc /tmp/<slug>_no_h1.md \
  -o adhoc_jobs/yage_share/site/<slug>.html \
  --standalone \
  --embed-resources \
  --metadata title="<report title>" \
  --css tools/share_report.css \
  --include-in-header=/tmp/<slug>_seo.html \
  --include-in-header=tools/share_report_ga4.html \
  --include-after-body=tools/share_report_tts.html
```

Note: write the output directly into the `adhoc_jobs/yage_share/site/` directory.

#### Step 3: Update manifest.json

Edit `adhoc_jobs/yage_share/manifest.json` and add a new entry to the `articles` array:

```json
{
  "slug": "<slug>",
  "title": "<report title>",
  "date": "<YYYY-MM-DD>",
  "description": "<article summary under 150 characters>",
  "author": "<your-name>",
  "indexed": false,
  "is_temporary": false
}
```

**Indexing control** (important):
- **Default `indexed: false`** - the article does not appear in the index.html list
- Set to `true` only when the user explicitly says something like:
  - "add it to the index", "put it in index", "list it publicly", "include this article in the index"
- When uncertain, default to `false`; it can be changed afterward

**Temporary marker** (optional):
- **Default `is_temporary: false`** (false by default, can be omitted)
- Set to `true` when triggered by: "temporary", "time-sensitive", "can delete after expiration"
- Purpose: mark time-sensitive content for later batch cleanup
- Orthogonal to `indexed`: temporary articles can be indexed, and non-temporary articles can be unindexed

#### Step 4: Conditionally Update index.html

**Run this step only when `indexed: true`**:

```bash
cd adhoc_jobs/yage_share && python3 gen_index.py
```

This reads manifest.json, filters articles with `indexed: true`, and generates `site/index.html` sorted by date descending.

#### Step 5: Upload to Remote

```bash
# Upload article
rsync adhoc_jobs/yage_share/site/<slug>.html <your-server>:/var/www/yage/share/
ssh <your-server> "chmod 644 /var/www/yage/share/<slug>.html"

# If index.html was updated, upload it too
rsync adhoc_jobs/yage_share/site/index.html <your-server>:/var/www/yage/share/
ssh <your-server> "chmod 644 /var/www/yage/share/index.html"
```

#### Step 6: Git Commit manifest Changes

```bash
cd adhoc_jobs/yage_share && git add manifest.json && git commit -m "add: <slug>"
```

### Slug Naming Rules

- Lowercase English, words joined with `-`
- End with date `YYYYMMDD`
- Examples: `iran-war-survey-20260302`, `ai-agent-report-20260315`

### Final URL

```
https://<your-domain>/share/<slug>.html
```

## Verification

After upload, use curl to confirm accessibility:

```bash
curl -s -o /dev/null -w "%{http_code}" https://<your-domain>/share/<slug>.html
# Should return 200
```

## CSS Template Notes

`tools/share_report.css` features:
- 800px max-width centered layout
- Chinese font stack (PingFang SC / Microsoft YaHei)
- Automatic dark mode (`prefers-color-scheme: dark`)
- Table, blockquote, and code block styles
- Responsive adaptation for mobile

To modify global styles, edit `tools/share_report.css`; future publications will automatically use the new style.

## Reports with Images

When Markdown references local images (`![](path/to/image.png)`):

```bash
# Use --resource-path to specify the image search directory, usually the Markdown file's directory
pandoc <input.md> \
  -o adhoc_jobs/yage_share/site/<slug>.html \
  --standalone \
  --embed-resources \
  --resource-path=<md-file-directory> \
  --metadata title="<report title>" \
  --css tools/share_report.css \
  --include-in-header=/tmp/<slug>_seo.html \
  --include-in-header=tools/share_report_ga4.html \
  --include-after-body=tools/share_report_tts.html
```

`--embed-resources` converts images into base64 data URIs embedded in the HTML.

Verify before publishing:
```bash
# Confirm images were embedded
grep -c 'data:image' adhoc_jobs/yage_share/site/<slug>.html
# Should output the number of images (>0)
```

## TTS Narration

`tools/share_report_tts.html` is automatically injected into every report through `--include-after-body`, providing:

- A floating speaker button in the lower-right corner: click to read aloud, click again to pause, long-press 0.8 seconds to stop
- Browser-native Web Speech API (`speechSynthesis`), with no backend and no cost
- Automatically skips code blocks and tables, and segments by Chinese punctuation (about 200 characters per segment)
- Built-in workaround for Chrome's 14-second interruption bug (segmented playback + periodic pause/resume)
- Automatically hides the button in browsers that do not support `speechSynthesis`

To modify TTS behavior, such as speech rate or segment length, edit `tools/share_report_tts.html`.

## Notes

- HTML is self-contained (CSS + GA4 + images + TTS are all embedded) and does not depend on external files
- The share directory is publicly accessible; do not upload sensitive content
- To delete published content: `ssh <your-server> "rm /var/www/yage/share/<slug>.html"`
- **Important: when using `--metadata title`, the first line of the Markdown file should not be a `# ` title**. pandoc automatically generates an h1 element from metadata; if the Markdown also contains a `# ` title, the HTML output will contain two h1 elements. Solution: delete the `# ` title line from the Markdown and let pandoc's metadata title provide the h1 by itself.
- Local project directory `adhoc_jobs/yage_share/` is the source of truth for manifest and site
- HTML files under `site/` are ignored by .gitignore; only manifest.json and scripts are tracked by git
