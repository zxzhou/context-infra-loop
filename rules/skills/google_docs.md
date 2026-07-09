# Skill: Google Docs Operations

Control Google Docs through CLI commands: publish Markdown files, create documents, search, modify, share, and manage tabs.

## When to Use

Trigger this skill when the user says things like:
- "Help me create a Google Doc"
- "Send this Markdown to Google Docs"
- "Search my Google Docs"
- "Share this document with xxx"
- "Modify that document's title/content"
- Any request involving creating, searching, modifying, or sharing Google Docs

## Prerequisites

- Project location: `adhoc_jobs/gdocs_skill/`
- Python venv: `adhoc_jobs/gdocs_skill/.venv/` (created with `uv`)
- OAuth credentials: `adhoc_jobs/gdocs_skill/secrets/credentials.json` must exist
- First use requires OAuth authorization through a browser popup; see the project `README.md`

## Invocation

Run all commands from the project directory through `python -m gdocs`. All output is JSON.

```bash
cd /path/to/knowledge_working/adhoc_jobs/gdocs_skill && source .venv/bin/activate
```

## Common Scenarios

### Scenario 1: Publish a Markdown File to Google Docs

This is the most common request.

```bash
python -m gdocs publish path/to/report.md --title "AI Frontline 2026-03-08"
```

Share with someone immediately after publishing:

```bash
python -m gdocs publish path/to/report.md --title "Report" --share someone@example.com --role writer
```

### Scenario 2: Tab Management

List all tabs in a document:

```bash
python -m gdocs tab list DOC_ID
```

Add a new tab to a document:

```bash
python -m gdocs tab add DOC_ID "Tab Title"
python -m gdocs tab add DOC_ID "Tab Title" path/to/content.md --format markdown
```

Update the content of an existing tab by clearing it and rewriting it:

```bash
python -m gdocs tab replace DOC_ID TAB_ID path/to/updated.md
```

Markdown format is used by default. For plain text:

```bash
python -m gdocs tab replace DOC_ID TAB_ID file.txt --format plain
```

Rename a tab:

```bash
python -m gdocs tab rename DOC_ID TAB_ID "New Title"
```

### Scenario 3: Create an Empty Document

```bash
python -m gdocs create --title "New Document"
```

### Scenario 4: Search Documents

```bash
python -m gdocs search "keyword"
python -m gdocs search "keyword" --max-results 20
```

### Scenario 5: Share a Document

```bash
python -m gdocs share DOC_ID --email user@example.com --role writer
python -m gdocs share DOC_ID --email user@example.com --role reader --message "Please review"
```

### Scenario 6.5: Delete Documents (Clean Up Tests / Discarded Docs)

```bash
python -m gdocs delete DOC_ID                # Move to trash (default, recoverable for 30 days)
python -m gdocs delete DOC_ID --permanent    # Permanently delete immediately (not recoverable)
```

**When to use**:
- Debugging test docs left behind by failed publish/create runs
- A single operation creates multiple duplicate docs (see Troubleshooting)
- Sub-agents automatically create scaffold docs during tests

**Discipline**: Before every create/publish, consider whether it will leave behind an unnecessary doc. If it is a debug doc, **delete it immediately after use** so it does not pollute the user's Drive. Default trash mode gives you a 30-day recovery window.

### Scenario 6: Modify Title / Get Link

```bash
python -m gdocs title DOC_ID "New Title"
python -m gdocs link DOC_ID
python -m gdocs link DOC_ID --public
```

## Supported Markdown Syntax

| Syntax | Effect |
|--------|--------|
| `# Title` | Heading 1 |
| `## Title` | Heading 2 |
| `### Title` | Heading 3 |
| `**bold**` | Bold |
| `*italic*` | Italic |
| `***bold italic***` | Bold + italic |
| `` `code` `` | Monospace font (Courier New) |
| `[text](url)` | Hyperlink |
| `- item` | Unordered list |
| `1. item` | Ordered list |
| `---` | Divider line (gray centered line) |
| `> quoted text` | Quote block (left indent + left border) |
| `\| col \| col \|` | Native table (header automatically bolded) |

### Scenario 7: Insert a Local Image into a Document

```bash
python -m gdocs image DOC_ID path/to/image.png --width 468
```

By default, the image is inserted at the end of the document. Insert at a specified position if you know the character index:

```bash
python -m gdocs image DOC_ID image.png --index 2050 --width 468
```

`--width 468` is full width. The image is uploaded to Google Drive before insertion into the document.

**Markdown publication flow with images**: `![alt](local_path.png)` in Markdown is not automatically converted into an image. After publishing, the alt text remains as plain text, such as `!Monthly Revenue by Course`. Correct procedure:

1. Publish the Markdown first; image placeholders become alt text
2. Use the Google Docs API to scan the document and find the index of the alt text
3. Insert images one by one with `gdocs image --index`, working from the bottom of the document upward to avoid index shifts

Batch insertion example (Python, bottom to top):

```python
from gdocs.auth import get_credentials
from googleapiclient.discovery import build

creds = get_credentials(Path("secrets"))
docs = build("docs", "v1", credentials=creds)
doc = docs.documents().get(documentId=DOC_ID).execute()

# Find the startIndex of each "!alt text" placeholder paragraph
# Sort by index descending
# Call one by one: gdocs image DOC_ID path --index {start} --width 468
```

Note: after inserting an image, all subsequent document indexes shift, so you must insert from back to front. To delete an inserted image, use `deleteContentRange` in batchUpdate.

## Notes

- OAuth scope is `drive.file`, so it can only access files created by this app or explicitly opened by the user
- Search can only find documents within the above scope, not the entire Google Drive
- Document deletion is not supported (for safety)
- All output is JSON; errors go to stderr
- Credentials are stored in the project `secrets/` directory and are gitignored
- Tokens refresh automatically; after expiration, authorization will restart automatically

## Troubleshooting

### What to Do When CLI Publish Fails

**Normal error information** (after 2026-04-08): `{"error": "Failed to create document '...': HTTP 503 - <body>"}`. RuntimeError now includes the status code and response body, so the cause is directly visible.

**Status code quick reference**:
- **429 / 5xx**: transient error. `client.py` already retries 3 times with exponential backoff. If it still fails, the Google API is actually down. **Retry the whole command directly**; do not fall back to a workaround.
- **400**: request format error, such as title containing special characters, content too large, or invalid parameters. Inspect the response body for the specific field.
- **401 / 403**: OAuth invalid. Delete `secrets/token.json` and authorize again.
- **404**: `doc_id` does not exist or there is no permission.

**Anti-pattern: falling back to a workaround chain**

If CLI publish fails, **do not** do this:
1. Run `gdocs create` to test auth, leaving behind a test doc
2. Call `client.create_document()` directly in Python, bypassing later CLI steps
3. Repair with `gdocs tab replace`
4. Share again

**Correct approach**: first inspect the error status code and body. If it is transient, retry the CLI publish command directly. If it is permanent, diagnose from the specific field in the body. If you must create a debug doc to verify auth, **clean it up immediately with `gdocs delete DOC_ID` after use**.

**Known trigger scenarios**:
- Publishing large files (>15,000 characters) occasionally triggers 5xx; auto-retry already exists, and if all 4 attempts fail, consider splitting into tabs
- Occasional Google API 503; auto-retry usually covers it

### CLI Publish Formatting Is Wrong (Markdown Did Not Render as Headings / Tables)

**Symptom**: the doc is created successfully, but all content is plain text with no heading styles.

**Cause**: calling `client.create_document()` directly does not go through the `content_format="markdown"` path. The CLI publish path is correct (lines 90-98 of `__main__.py` use `content_format="markdown"`).

**Fix**: rewrite the same doc with `gdocs tab replace DOC_ID t.0 file.md --format markdown`. Get the tab id with `gdocs tab list DOC_ID` (default is `t.0`). **Do not create a new doc**; that leaves the original doc in the user's Drive.

### OAuth Reauthorization

### OAuth Reauthorization

If you encounter OAuth-related errors (403 access_denied, token invalid, etc.):
1. Delete `secrets/token.json`
2. Run the command again; the browser will open the authorization page
3. Confirm the current Google account is in the OAuth consent screen's Test users list
