#!/usr/bin/env python3
import os
import time
import argparse
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
try:
    from opencode_client import OpenCodeClient
except ImportError:
    print("Error: Could not import OpenCodeClient. Ensure path is correct.")
    sys.exit(1)

def run_ai_news_survey(mode="weekly", model_id="anthropic/claude-opus-4-6", publish_to_kit=False):
    """
    Delegates the AI News Survey and personalized report generation to the OpenCode Agent.
    Uses axiom-based evaluation framework for evidence-tiered, builder-focused reporting.
    
    Args:
        mode: "weekly" (7 days) or "daily" (1 day)
        model_id: OpenCode model ID to use
        publish_to_kit: If True, publish newsletter to Kit subscribers instead of personal email
    """
    client = OpenCodeClient()
    
    date_str = datetime.now().strftime('%Y/%m/%d')
    date_file = datetime.now().strftime('%Y%m%d')
    
    if mode == "daily":
        days_back = 1
        session_title = f"Daily AI News {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        report_filename = f"daily_ai_newsletter_{date_file}.md"
        report_path = f"contexts/survey_sessions/daily_ai_newsletter/{report_filename}"
        report_title = "AI Daily"
        period_desc = "today"
        days_desc = "1 day"
        max_lines = 100
    else:
        days_back = 7
        session_title = f"Autonomous AI News Survey {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        report_filename = f"ai_news_weekly_{date_file}.md"
        report_path = f"contexts/survey_sessions/{report_filename}"
        report_title = "AI Weekly"
        period_desc = "this week"
        days_desc = "7 days"
        max_lines = 300
    
    session_id = client.create_session(session_title)
    
    if not session_id:
        print("Failed to create OpenCode session.")
        return

    if publish_to_kit:
        delivery_instruction = f"""### Phase 6: Delivery

- **Kit publishing**: use Kit Broadcast to email all subscribers and publish to the web:
  ```bash
  python3 periodic_jobs/ai_heartbeat/src/v0/kit_broadcast.py {report_path}
  ```
  The script converts Markdown to HTML and sends to Kit subscribers after two minutes.
  - **Email subject**: use the report title from the first line."""
    else:
        delivery_instruction = f"""### Phase 6: Delivery

- **Email notification**: send the full HTML email with `--file`:
  ```bash
  python3 tools/send_email_to_myself.py "[{report_title}] {date_str}: [one sentence describing the most important verified fact from {period_desc}]" "" --file {report_path}
  ```
  The script converts Markdown to styled HTML.
  - **Email subject**: [{report_title}] {date_str}: [one sentence describing the most important verified fact from {period_desc}]"""

    prompt = f"""You are a senior AI industry researcher responsible for producing a {report_title} insight report.

## Step 0: Read the Axiom System First

Before research, read `rules/axioms/INDEX.md` to establish the evaluation frame. Then choose 3-5 relevant axiom files to read in depth based on the current topic. These axioms are your evaluation function: what deserves attention, what should be filtered, and how the report should be layered.

## Success Criteria

The target reader is a builder-practitioner who builds AI systems and has limited time. Useful means:

1. Facts and opinions are strictly separated. Put the fact table first and analysis later.
2. Every fact has an evidence tier: [Official], [Primary reporting], [Third-party test], [Industry analysis], or [Unverified].
3. Every fact includes a real source URL.
4. Evidence tiers must match source URLs. Official claims require official domains when labeled [Official].
5. Key numbers must be cross-checked. If only one non-official source exists, label the number [Unverified].
6. Use a builder lens: explain how the information affects what to build, buy, avoid, or verify this week.
7. Explicitly filter noise and explain why it is not worth attention.
8. Keep the report under {max_lines} lines of Markdown. Information density matters more than coverage.

## Execution Flow

### Phase 1: Broad Research and Fact Collection

Use Tavily to search major AI developments from {date_str} back {days_desc}. Cover frontier models, chips and infrastructure, agent tooling, safety events, regulation, and industry conflicts. Prioritize OpenAI, Anthropic, Google DeepMind, DeepSeek, NVIDIA, Meta, Groq, and adjacent ecosystem players. Classify evidence tier immediately when collecting each item.

### Phase 2: Number Verification and Cross-Checks

Verify key numbers one by one: revenue, funding, valuation, benchmark scores, users, adoption, and product claims. Prefer official filings, release posts, docs, or primary sources. Do not label third-party summaries as [Official].

### Phase 3: Builder-Lens Filtering

Include at most 2-3 builder-lens issues. A topic qualifies if it directly affects build decisions, has quantitative support, or creates useful tension with the axiom system. Exclude pure narratives, product announcements without a testable product or date, funding news without technical substance, and generic AGI forecasts.

### Phase 4: Write the Report

Use this structure exactly:

```markdown
# [{report_title}] YYYY-MM-DD

**Coverage period**: ...

## 1. {period_desc} Fact Table

## 2. Builder Lens

## 3. Quantitative Anchors

## 4. Watchlist

## 5. Not Worth Attention
```

### Phase 5: Self-Review

Output self-review results in the chat response, not in the Markdown file. Fix the saved file if you find unsupported numbers, mixed facts and judgments, excessive length, an empty noise-filtering section, or unit/order-of-magnitude errors.

{delivery_instruction}

## Style

Write in English. Preserve technical terms. Be calm and evidence-driven. Do not use grand claims, emoji, star ratings, or vague importance language; let evidence tiers and numbers carry the weight.

Start now.
"""
    print(f"Triggering {mode} news survey in OpenCode (Session: {session_id})...")
    print(f"Using model: {model_id}")
    if publish_to_kit:
        print("Publish mode: Kit subscribers")
    
    result = client.send_message(session_id, prompt, model_id=model_id)

    if not result:
        print("No immediate response from server. Sending continuation ping...")
        result = client.send_message(session_id, "Continue", model_id=model_id)
    
    if result:
        client.wait_for_session_complete(session_id)
        messages = client.get_session_messages(session_id) or []
        assistants = [m for m in messages if (m.get("info") or {}).get("role") == "assistant"]
        if assistants:
            last_info = assistants[-1].get("info") or {}
            print(f"Resolved model: {last_info.get('providerID')}/{last_info.get('modelID')}")
        print(f"{report_title} complete.")
    else:
        print("Failed to start survey session.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run AI news survey (daily or weekly)")
    parser.add_argument("--mode", "-m", choices=["daily", "weekly"], default="weekly",
                        help="Survey mode: 'daily' (1 day) or 'weekly' (7 days, default)")
    parser.add_argument("--model", "-M", default="anthropic/claude-opus-4-6",
                        help="OpenCode model ID (default: anthropic/claude-opus-4-6)")
    parser.add_argument("--publish-to-kit", "-k", action="store_true",
                        help="Publish newsletter to Kit subscribers instead of personal email")
    args = parser.parse_args()
    
    print(f"Starting AI News Survey ({args.mode})...")
    run_ai_news_survey(mode=args.mode, model_id=args.model, publish_to_kit=args.publish_to_kit)
    print("Survey process finished.")
