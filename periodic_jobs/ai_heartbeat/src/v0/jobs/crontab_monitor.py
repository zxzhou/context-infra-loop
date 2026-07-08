#!/usr/bin/env python3
import os
import time
from datetime import datetime
import sys
from pathlib import Path

# Add the parent directory to sys.path to import OpenCodeClient
sys.path.append(str(Path(__file__).parent.parent))
try:
    from opencode_client import OpenCodeClient
except ImportError:
    print("Error: Could not import OpenCodeClient. Ensure path is correct.")
    sys.exit(1)

def run_ai_analysis():
    """
    Delegates the entire crontab health check process to the OpenCode Agent.
    """
    client = OpenCodeClient()
    session_title = f"Autonomous Crontab Health Check {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    session_id = client.create_session(session_title)
    
    if not session_id:
        print("Failed to create OpenCode session.")
        return

    # Proactive and autonomous prompt
    prompt = f"""You are a systems operations expert responsible for maintaining the user's production environment.
Your task is to autonomously audit the health of all current crontab jobs.

### Core Tasks and Principles

1. **Collect data yourself**: run `crontab -l` to inspect all scheduled jobs. Do not rely on supplied data.
2. **Investigate logs deeply**:
   - Analyze each job's frequency.
   - Identify log file paths.
   - If a crontab line has no explicit redirection such as `>>`, do not assume there are no logs. Read the referenced script and check whether it redirects internally, for example with `exec >>`.
3. **Activity analysis**:
   - Check the last modified time of each log.
   - If a job runs every two minutes, the log should normally update within roughly two minutes.
   - If a log is missing or stale for more than two expected cycles, treat it as abnormal.
4. **Error audit**:
   - Read the tail of important logs and look for Python tracebacks, command-not-found errors, network failures, or DNS failures.
5. **Optional local checks**:
   - If the repository defines extra local health-check scripts under `contexts/` or `tools/`, run only the checks that are clearly documented and safe.
   - Skip undocumented private workflows. Do not infer personal data locations.

### Delivery Logic

- **All normal**: reply `All normal; no intervention needed` and do not call the email tool.
- **Any abnormality**: send an alert email with `python3 tools/send_email_to_myself.py`.
  - Subject: `[Alert] Crontab Job Health Audit Report`.
  - Body: use modern readable HTML. List affected jobs, actual log paths, error snapshots, optional local-check failures if any, and expert-level repair suggestions.

Start the audit now.
"""
    print(f"Triggering autonomous analysis in OpenCode (Session: {session_id})...")
    result = client.send_message(session_id, prompt, model_id="glm-5")
    
    if result:
        client.wait_for_session_complete(session_id)
        print("Autonomous AI Analysis complete.")
    else:
        print("Failed to start analysis session.")

if __name__ == "__main__":
    print("Starting Autonomous Crontab Auditor...")
    run_ai_analysis()
    print("Audit process finished.")
