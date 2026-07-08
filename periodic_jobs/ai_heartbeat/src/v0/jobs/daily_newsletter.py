#!/usr/bin/env python3
"""
Daily newsletter generator for an AI notes publication.

Two-loop architecture: extract topics from a message export, run parallel research,
apply axiom lens to identify gaps, run targeted second research, then write.

Usage:
  python daily_newsletter.py               # Run for yesterday (default)
  python daily_newsletter.py --date 20260301  # Run for a specific date
  python daily_newsletter.py --dry-run     # Generate only, skip Kit publish
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
try:
    from opencode_client import OpenCodeClient
except ImportError:
    print("Error: Could not import OpenCodeClient. Ensure path is correct.")
    sys.exit(1)


DEFAULT_MODEL = "anthropic/claude-opus-4-6"


def run_daily_newsletter(date_str: str, dry_run: bool = False, model_id: str = DEFAULT_MODEL):
    """
    Triggers a newsletter generation session in OpenCode.

    Args:
        date_str: Date in YYYYMMDD format (e.g. "20260301")
        dry_run: If True, generate newsletter file but skip Kit publish
        model_id: OpenCode model ID to use
    """
    client = OpenCodeClient()

    date_display = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    session_title = f"Daily Newsletter {date_display}"
    session_id = client.create_session(session_title)

    if not session_id:
        print("Failed to create OpenCode session.")
        return

    chat_csv = f"periodic_jobs/ai_heartbeat/daily_messages/{date_str}.csv"
    output_path = f"contexts/survey_sessions/daily_ai_newsletter/ai_frontline_{date_str}.md"

    # Guard: abort if chat CSV doesn't exist
    if not Path(chat_csv).exists():
        print(f"ABORT: Chat CSV not found: {chat_csv}")
        print("The message export for this date has not been generated yet.")
        print("Create the CSV before running this job, or override the script for your own message source.")
        return

    if dry_run:
        publish_step = """## Phase 7: Skip Publishing (dry-run mode)

The file has been generated. Do not publish to Kit."""
    else:
        publish_step = f"""## Phase 7: Publish to Kit

Run the following command to email all subscribers and publish to the web:

```bash
source periodic_jobs/ai_heartbeat/.venv/bin/activate && \
  python periodic_jobs/ai_heartbeat/src/v0/kit_broadcast.py \
  {output_path}
```

The script sends automatically after two minutes. Return the broadcast ID to the user for tracking."""

    publication_name = os.getenv("NEWSLETTER_PUBLICATION_NAME", "AI Notes")
    subscribe_url = os.getenv("NEWSLETTER_SUBSCRIBE_URL", "https://example.com/subscribe")

    prompt = f"""You are the editor of {publication_name}. Generate the newsletter issue for {date_display}.

This task uses a two-loop architecture: extract topics from a message export, run parallel research, use the axiom system to identify gaps, run targeted follow-up research, then write the issue. Follow the phases in order.

---

## Phase 0: Read Framework Files

Read these files first:

- `periodic_jobs/ai_heartbeat/docs/newsletter_design.md`: complete newsletter design spec if present.
- `contexts/survey_sessions/daily_ai_newsletter/ai_frontline_20260301.md`: first-issue sample for structure and tone if present.
- `rules/skills/workflow_parallel_subagents.md`: parallel-agent workflow for Phase 2.

Do not read axiom files yet. Axioms are a thinking lens for Phase 3 and should be selected after you understand the chat and first research results.

## Phase 1: Extract Group-Chat Topics

Read `{chat_csv}`. The CSV format is `sender,content`. Extract 2-3 high-signal topics worth deeper investigation. For each topic, output a topic card in the chat response, not a file:

```markdown
### Topic N: [Name]
- One-sentence description: ...
- Core judgment this topic should support: ...
- Why readers should care: ...
- Key chat excerpts: ...
- Related links shared in the chat: ...
- One detail that should survive into the final article: ...
- Research questions:
  1. ...
  2. ...
  3. ...
```

Ignore casual chatter, stickers, and purely social interaction. Prioritize technical depth, industry observations, disputed judgments, and comments from the primary user.

## Phase 2: Parallel Research

Read `rules/skills/workflow_parallel_subagents.md` before this phase. Start background librarian agents in parallel:

1. One agent per topic, using the topic card research questions. Ask for deep research on 3-5 concrete subquestions, a 500-800 word English summary, and source URLs for all key facts.
2. One broad news agent to scan major AI news from {date_display}, including frontier models, funding, safety events, regulation, infrastructure, and tooling.

After notifications arrive, collect complete outputs for every agent. If output is paginated, increase the message range until all content is collected. Do not continue with incomplete research.

## Phase 3: Axiom-Guided Synthesis and Gap Detection

1. Read `rules/axioms/INDEX.md`.
2. Cross-check chat topics against research results and broad news. Look for structural resonance between separate threads.
3. Select and read 2-3 relevant axiom detail files.
4. Identify unanswered deeper questions, missing evidence, and hidden connections that need factual support.

Output a second-round research list with 2-4 concrete queries or questions in the chat response.

## Phase 4: Targeted Follow-Up Research

If gaps remain, start 1-2 focused background librarian agents. These queries should come from the axiom lens and should add depth that the first round missed. Require source URLs and concrete data. Skip this phase only if the evidence chain is already sufficient.

## Phase 5: Write and Save the Newsletter

Synthesize the chat, both research rounds, and the axiom lens. Save the finished Markdown directly to `{output_path}`.

Use this structure exactly:

```markdown
# [{publication_name}] {date_display}

> [One sentence revealing the hidden thread across all topics.]

**Quick brief: [One or two sentences summarizing the core points across 2-3 topics.]**

## [Topic One Title]

[Paragraphs...]

---

## [Topic Two Title]

[Paragraphs...]

---

## Also Worth Knowing

**[Title]**: [One or two sentences + source link]

---

[Fixed footer]
```

Depth requirements:

1. Do not merely paraphrase the chat; add analysis, missing questions, and external evidence.
2. Each topic must dig at least two layers below the initial observation.
3. Use data to advance the argument, not as decoration.
4. Look for structural mappings between chat threads and external news.
5. Use axioms as an internal thinking lens, but do not mention axiom names or numbers in the article.
6. Keep each topic centered on a judgment, not an inventory of facts.
7. Open each section with the value of the section before diving into evidence.

Readability requirements:

- Start from concrete scenes before abstract claims.
- Keep one idea per paragraph.
- Split long sentences.
- Anchor abstract concepts with examples.
- Attribute the primary user's comments by role; refer to other chat participants generically.
- Use a conversational English tone without becoming casual about evidence.
- Bridge between cases before switching examples.
- State units and time windows for costs, tokens, duration, frequency, and scale.
- Treat links shared in the group chat as source material, not just citations.

Structure requirements:

1. Opening blockquote: one insight sentence that reveals the hidden thread across the issue.
2. Quick brief: a bold one- or two-sentence summary immediately after the blockquote.
3. Two or three topic sections.
4. Also Worth Knowing: two or three short news items with source links.
5. Fixed footer.

Separate sections with `---`. Write in English. Preserve technical terms. Keep a calm analytical voice. Every key claim needs an inline source link. Avoid emoji and long dash punctuation. Prefer paragraphs over bullets except where structure requires bullets.

Length: 55-75 lines of Markdown. Information density matters more than breadth. After saving, run `wc -l` and adjust if the file is outside that range.

Fixed footer:

```markdown
---

*This issue cross-checks community discussion with public AI industry information.*

*This newsletter was generated from AI-domain research and group-chat context. Please watch for possible hallucinations.*

*Subscribe: [{subscribe_url}]({subscribe_url})*
```

## Phase 6: Self-Review

Output self-review results in the chat response, not in the Markdown file. If fixes are needed, edit `{output_path}`. Check:

1. Does any topic merely restate chat messages without added analysis?
2. Does each topic dig at least two layers deeper?
3. Is the file 55-75 lines?
4. Does every key claim have an inline source or an [Unverified] label?
5. Did any explicit axiom name or number leak into the article?
6. Is Also Worth Knowing populated?
7. Did any product or project turn into a feature list rather than supporting a larger judgment?
8. Are transitions between cases bridged clearly?
9. Are units and time windows explicit?
10. Does the writing follow `rules/COMMUNICATION.md`: direct positive phrasing, no long dash punctuation, no inflated marketing language?

Fix issues before continuing.

{publish_step}
"""

    print(f"Triggering daily newsletter for {date_display} (Session: {session_id})...")
    print(f"Model: {model_id}")
    print(f"Chat CSV: {chat_csv}")
    print(f"Output: {output_path}")
    if dry_run:
        print("Mode: dry-run (no Kit publish)")

    result = client.send_message(session_id, prompt, model_id=model_id)

    if not result:
        print("No immediate response from server. Sending continuation ping...")
        result = client.send_message(session_id, "Continue", model_id=model_id)

    if result:
        client.wait_for_session_complete(session_id)
        messages = client.get_session_messages(session_id) or []
        assistants = [m for m in messages if (m.get("info") or {}).get("role") == "assistant"]
        if assistants:
            info = assistants[-1].get("info") or {}
            print(f"Resolved model: {info.get('providerID')}/{info.get('modelID')}")
        print(f"Newsletter for {date_display} complete.")
    else:
        print("Failed to start newsletter session.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate daily AI newsletter")
    parser.add_argument(
        "--date", "-d",
        default=(datetime.now() - timedelta(days=1)).strftime("%Y%m%d"),
        help="Date in YYYYMMDD format (default: yesterday)",
    )
    parser.add_argument(
        "--model", "-M",
        default=DEFAULT_MODEL,
        help=f"OpenCode model ID (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Generate newsletter file but skip Kit publish",
    )
    args = parser.parse_args()

    print(f"Starting daily newsletter generation for {args.date}...")
    run_daily_newsletter(date_str=args.date, dry_run=args.dry_run, model_id=args.model)
    print("Done.")
