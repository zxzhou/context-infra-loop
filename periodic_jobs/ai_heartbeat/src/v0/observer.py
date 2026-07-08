#!/usr/bin/env python3
"""
L1 Observer Agent (Trigger Script)
Instructs OpenCode-Builder to autonomously scan, filter, and write to memory.
"""
import os
import json
import uuid
from datetime import datetime, timezone
from opencode_client import DEFAULT_LOOP_RUN_DIR, OpenCodeClient, WORKSPACE_ROOT

DEFAULT_MODEL = os.getenv("OPENCODE_DEFAULT_MODEL", "anthropic/claude-opus-4-6")
LOOP_NAME = "heartbeat_observer"
SPEC_PATH = "periodic_jobs/ai_heartbeat/loop_specs/heartbeat_observer.json"
KNOWLEDGE_BASE = WORKSPACE_ROOT / "periodic_jobs" / "ai_heartbeat" / "docs" / "KNOWLEDGE_BASE.md"
OBSERVATIONS_PATH = WORKSPACE_ROOT / "contexts" / "memory" / "OBSERVATIONS.md"

PROMPT_TEMPLATE = """
Goal: extract observation memory and persist it directly to disk.
Baseline date: {target_date}

Idempotency constraint: before writing anything, read OBSERVATIONS.md and check whether an entry for `Date: {target_date}` already exists. If it exists, do not modify any file; reply `Entry for {target_date} already exists, skipping`.

SOP path:
{kb_path}

Tasks:
1. Read the SOP above and the L3 constraint files referenced by it.
2. Check idempotency in OBSERVATIONS.md.
3. Scan changes under `{workspace_root}`.
4. Append observations for {target_date} to `{observations_path}` using High, Medium, and Low priority entries. Prefer command-line append over whole-file editing for this large file.
5. Scope constraint: perform only the L1 Observer task. Do not perform L2 Reflector work, do not edit files under `rules/`, and do not promote or garbage-collect rules.
6. Format: the date header must be exactly `Date: YYYY-MM-DD`. Any referenced file or directory must use a full path relative to the workspace root.
7. End with exactly one terminal state line: `Terminal state: WRITTEN`, `Terminal state: NO_SIGNAL`, or `Terminal state: FAILED_NEEDS_HUMAN`.
8. When complete, reply with a short walkthrough.
"""

def write_skip_trace(target_date):
    started_at = datetime.now(timezone.utc)
    run_id = f"{started_at.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    run_dir = DEFAULT_LOOP_RUN_DIR / LOOP_NAME
    run_dir.mkdir(parents=True, exist_ok=True)
    trace_path = run_dir / f"{run_id}.json"
    trace = {
        "run_id": run_id,
        "loop_name": LOOP_NAME,
        "spec_path": SPEC_PATH,
        "inputs": {"target_date": target_date},
        "expected_artifacts": [str(OBSERVATIONS_PATH.relative_to(WORKSPACE_ROOT))],
        "started_at": started_at.isoformat(),
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "duration_seconds": 0,
        "session_id": None,
        "terminal_state": "SKIPPED_EXISTING_DATE",
        "error": None,
    }
    with open(trace_path, "w", encoding="utf-8") as f:
        json.dump(trace, f, indent=2, ensure_ascii=False, sort_keys=True)
    return trace_path

def main():
    import argparse
    parser = argparse.ArgumentParser(description='L1 Observer Agent')
    parser.add_argument('date', nargs='?', default=datetime.now().strftime("%Y-%m-%d"),
                        help='Target date (YYYY-MM-DD)')
    parser.add_argument('--model', default=DEFAULT_MODEL,
                        help='Model ID to use')
    parser.add_argument('--no-delete', action='store_true',
                        help='Keep session after completion (default: delete)')
    args = parser.parse_args()

    target_date = args.date
    model_id = args.model
    delete_after = not args.no_delete

    # Idempotency: skip if entry for target_date already exists
    if OBSERVATIONS_PATH.exists():
        with open(OBSERVATIONS_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        if f"Date: {target_date}" in content:
            print(f"Idempotent skip: entry for {target_date} already exists in OBSERVATIONS.md")
            trace_path = write_skip_trace(target_date)
            print(f"Trace: {trace_path.relative_to(WORKSPACE_ROOT)}")
            return

    print(f"Triggering Fully Agentic Observer for date: {target_date} using model: {model_id}...")
    client = OpenCodeClient()

    prompt = PROMPT_TEMPLATE.format(
        kb_path=KNOWLEDGE_BASE,
        observations_path=OBSERVATIONS_PATH,
        target_date=target_date,
        workspace_root=WORKSPACE_ROOT,
    )
    trace = client.run_agent_loop(
        loop_name=LOOP_NAME,
        session_title=f"Heartbeat L1 - Persistence Mode - {target_date}",
        prompt=prompt,
        model_id=model_id,
        spec_path=SPEC_PATH,
        inputs={"target_date": target_date},
        expected_artifacts=[str(OBSERVATIONS_PATH.relative_to(WORKSPACE_ROOT))],
        delete_after=delete_after,
    )
    print(f"Task complete ({trace['terminal_state']}, Session: {trace.get('session_id')}).")

if __name__ == "__main__":
    main()
