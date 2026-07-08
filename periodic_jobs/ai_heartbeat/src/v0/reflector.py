#!/usr/bin/env python3
"""
L2 Reflector Agent (Trigger Script)
Instructs OpenCode-Builder to perform memory garbage collection directly on the file.
"""
import os
from opencode_client import OpenCodeClient, WORKSPACE_ROOT
from datetime import datetime

DEFAULT_MODEL = os.getenv("OPENCODE_DEFAULT_MODEL", "anthropic/claude-opus-4-6")
LOOP_NAME = "heartbeat_reflector"
SPEC_PATH = "periodic_jobs/ai_heartbeat/loop_specs/heartbeat_reflector.json"
KNOWLEDGE_BASE = WORKSPACE_ROOT / "periodic_jobs" / "ai_heartbeat" / "docs" / "KNOWLEDGE_BASE.md"
OBSERVATIONS_PATH = WORKSPACE_ROOT / "contexts" / "memory" / "OBSERVATIONS.md"

PROMPT_TEMPLATE = """
Perform the memory-system reflection and promotion task.

SOP: {kb_path}

Steps:
1. Read `{observations_path}` and analyze High entries plus important Medium entries.
2. Promote reusable content into `rules/`, respecting ownership boundaries:
   - `SOUL.md`: agent identity and core values.
   - `USER.md`: user profile and life philosophy.
   - `COMMUNICATION.md`: communication style only, not technical knowledge.
   - `WORKSPACE.md`: directory routing.
   - `skills/`: technical methods, workflows, and best practices.
3. Garbage collect OBSERVATIONS.md by removing promoted entries and expired Low entries.

Promotion threshold: cross-project relevance, repeated validation, and a clear usage scenario. Reply with a concise promotion report when complete.
End with exactly one terminal state line: `Terminal state: PROMOTED`, `Terminal state: NO_PROMOTION`, or `Terminal state: FAILED_NEEDS_HUMAN`.
"""

def main():
    import argparse
    parser = argparse.ArgumentParser(description='L2 Reflector Agent')
    parser.add_argument('--model', default=DEFAULT_MODEL,
                        help='Model ID to use')
    parser.add_argument('--delete-session', action='store_true',
                        help='Delete the OpenCode session after completion')
    args = parser.parse_args()
    
    model_id = args.model
    target_date = datetime.now().strftime("%Y-%m-%d")

    print(f"Triggering Fully Agentic Reflector using model: {model_id}...")
    client = OpenCodeClient()

    prompt = PROMPT_TEMPLATE.format(
        kb_path=KNOWLEDGE_BASE,
        observations_path=OBSERVATIONS_PATH,
    )
    trace = client.run_agent_loop(
        loop_name=LOOP_NAME,
        session_title=f"Heartbeat L2 Reflector - {target_date}",
        prompt=prompt,
        model_id=model_id,
        spec_path=SPEC_PATH,
        inputs={"target_date": target_date},
        expected_artifacts=[
            str(OBSERVATIONS_PATH.relative_to(WORKSPACE_ROOT)),
            "rules/",
        ],
        delete_after=args.delete_session,
    )
    print(f"Task complete ({trace['terminal_state']}, Session: {trace.get('session_id')}).")

if __name__ == "__main__":
    main()
