# AI-Generated Presentation Slides Workflow

## Metadata

- **Type**: Workflow
- **Use Case**: Creating high-quality presentations for corporate training, technical talks, keynotes, and similar settings
- **Repo**: [github.com/grapeot/nbp_slides](https://github.com/grapeot/nbp_slides)
- **Created**: 2026-02-25
- **Source**: Lessons from AI talk practice

---

## Core Idea

Use AI image generation (Gemini) to "render" talk content into a complete slide deck instead of assembling it manually. Each slide is a complete high-resolution image, with text and visual elements generated as one integrated whole.

**Key difference**:

- Old way: drag elements in PowerPoint/Keynote and align them one by one
- New way: write Markdown prompts, render each full slide with Gemini, and present with Reveal.js

---

## Step 1: Clone Repo

```bash
git clone <your-slides-repo>
cd <slides-repo-dir>
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Create a `.env` file:
```
GEMINI_API_KEY=your_key_here
```

---

## Step 2: Define Visual Style

Edit `visual_guideline.md`. This is the visual anchor for all generated slides.

### Reference Style: **"Clean Ink"**

```
- Background: cool light gray (#F0F4F8) + ultra-fine grid
- Illustration style: deep navy linework, flat color fills, the precision of engineering drawings
- Typography: sans-serif fonts (Inter/SF Pro), every slide must have a bold header
- Forbidden: realistic photography, glossy 3D, generic clipart
- Mascot: <your-mascot> (only for title and closing slides)
```

### Key Balance Principle (Very Important)

**The ultimate design goal for slides is dual-use: both a presentation tool and a handout.**

This is the core trade-off. One end is the Steve Jobs style: purely visual, incomprehensible without the speaker. The other is the classroom style: pure text, death by PowerPoint. We need to find the sweet spot in the middle:

- **As a handout**: if the slides are sent to someone who did not attend the talk, they should understand the core argument by reading the slides alone, without extra explanation
- **As a presentation**: listeners who arrive late or lose focus should be able to catch up to the speaker's position quickly from the current slide

This dual requirement means slide text cannot be merely "labels" or "keyword reminders" (that is the Steve Jobs style). It must contain **actual arguments and content** while still avoiding article-length paragraphs.

**Concrete execution standards:**

- **Target ratio**: about 40% illustration / about 60% readable text
- **Layout model**: left-right split, with diagram/flow/concept visual on the left and 2-4 lines of key text on the right
- **Text choice**: the text on the slide should be the core point of that slide, not a hint or reference to the point. Readers should know what you mean when they see the text
- **Visual choice**: illustrations should be concept diagrams, comparison diagrams, or flow diagrams that help explain the point, not decorative images that merely fill space
- Text must be legible from the back of a presentation room
- **Self-check**: after writing a slide, cover the speaker notes and ask yourself: could a smart person who has never heard this talk understand what the slide is trying to say from this slide alone? If not, there is not enough text. If yes but it feels boring, there is not enough visual substance

### Color Semantics (Especially Useful for Contrast Talks)

- **Orange (#C75B39)**: old paradigm / problem side (e.g. ChatGPT, before)
- **Teal (#0A6A74)**: new paradigm / solution side (e.g. Cursor, after)
- **Navy (#1C2526)**: body ink

---

## Step 3: Write `outline_visual.md`

This is the "source code" for the slide deck. Each slide uses this format:

```markdown
#### Slide N: Title Name
*   **Layout**: Layout description (e.g. Left diagram + right text panel)
*   **Scene**:
    *   **Prompt**: [Detailed visual description, including:
        - Bold header text
        - Specific content and style for the illustration area
        - Exact readable text content for the text area
        - Color, line, and typography instructions]
*   **Asset**: imgs/some_logo.png  <- optional, used when there is a logo or screenshot
```

### Prompt Writing Guidelines

1. **Write text content verbatim into the prompt**; do not merely say "add some explanatory text"
2. Make the illustration description specific ("a large circle with a gap at the lower left, a human silhouette standing in the gap")
3. Make the text area complete (not placeholders, but actual content)
4. Clearly label `LEFT PANEL` / `RIGHT PANEL` in the prompt

### About "not" Constructions

**Avoid negative constructions in slide text** (such as "you're not a user", "it doesn't know").
Use positive statements to express the same meaning instead, for example:

| Avoid | Use Instead |
|------|------|
| "you're not a user of the tool" | "you end up serving as a component of the tool" |
| "it doesn't know your config" | "it goes in blind: config unknown" |
| "this isn't just faster" | "this is a categorical shift" |
| "not just coding" | "brainstorming, drafting, planning, everything" |

---

## Step 4: Prepare Assets (Optional)

If a slide involves brand logos, screenshots, or QR codes:

1. Put the files in the `imgs/` directory
2. Add this line to the corresponding slide in `outline_visual.md`: `*   **Asset**: imgs/filename.png`
3. The asset will be injected into the prompt during generation

**Common asset sources**:
- Company logos: download PNGs from the official site or uxwing.com
- Screenshots: capture directly and save
- QR codes: generate with the Python `qrcode` library or an online tool

AI cannot reliably generate brand logos; it will hallucinate them. When a logo is needed, always provide the real file as an asset.

---

## Step 5: Generate the 1K Version (Fast Iteration)

```bash
# Generate all slides (8 parallel processes, fast)
python tools/generate_slides.py

# Generate only specific slides (for iteration)
python tools/generate_slides.py --slides 3 5 8
```

Generated files are placed at `generated_slides/slide_XX_0.jpg` (1K resolution).

**Note**: `ThreadPoolExecutor(max_workers=8)` in `generate_slides.py` should be set to 8; the default may be 4.

---

## Step 6: Preview

```bash
python start-server.py  # or open index.html directly
```

`index.html` uses Reveal.js to display images. Press `S` to open speaker notes mode.

---

## Step 7: Enlarge to 4K (Before Formal Release)

**Important: test on a single image first and confirm it can enlarge to 4K or higher before processing everything.**

```bash
# Step 1: test one slide first
python tools/generate_slides.py --enlarge --slides 1

# Verify: inspect generated_slides/slide_01_0_4k.jpg dimensions
file generated_slides/slide_01_0_4k.jpg
# Should show something like "3840 x 2160" or larger

# Step 2: after confirming enlargement works, process all slides in parallel
python tools/generate_slides.py --enlarge
```

Enlargement calls the Gemini API again and costs more. Testing on one slide first is mandatory.

---

## Step 8: Update `index.html`

For each section in `index.html`, update the `data-background` path:

- 1K version: `generated_slides/slide_XX_0.jpg`
- 4K version: `generated_slides/slide_XX_0_4k.jpg`

Speaker notes go inside each section's `<aside class="notes">`.

---

## Speaker Notes Writing Principles

- English for native speakers, conversational, and ready to read aloud
- About 120-150 words per slide
- **Avoid negative constructions** (same principle as slide text)
- First person, using "I", with warmth and a point of view
- Prefer concrete details over abstract summaries

---

## Common Troubleshooting

| Problem | Cause | Solution |
|------|------|------|
| AI draws a broken logo | AI hallucination; logo is not real pixels | Provide the real logo file in `imgs/` as an asset |
| Inconsistent style | Slide prompts differ too much | Strengthen the "container" description in `visual_guideline.md`, or regenerate |
| Garbled / illegible text | Generated font is too small or too ornate | Specify in the prompt: "all text must be fully legible printed sans-serif" |
| AI treats Cursor as a mouse cursor | Confuses Cursor the company with the cursor pointer | Provide the Cursor company logo as an asset and explicitly say "Cursor company logo" in the prompt |

---

## Project File Structure

```
slides/
├── outline_visual.md      # Source code (edit this every time)
├── visual_guideline.md    # Visual language definition
├── speak_notes.md         # Talk script (English, read aloud)
├── index.html             # Reveal.js player + speaker notes
├── imgs/                  # Assets (logos, screenshots, etc.)
├── generated_slides/      # Rendered output
│   ├── slide_01_0.jpg     # 1K version
│   └── slide_01_0_4k.jpg  # 4K version
├── tools/
│   ├── generate_slides.py      # Main generator (max_workers=8)
│   ├── gemini_generate_image.py # Gemini API wrapper
│   └── gemini_enlarge_image.py  # 4K enlarger
└── .env                   # GEMINI_API_KEY=...
```
