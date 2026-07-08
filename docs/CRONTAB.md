# Crontab Configuration Guide

This document describes scheduled jobs used by the context infrastructure system.

## Recommended Jobs

- AI Heartbeat Observer: scans workspace changes and appends useful observations to `contexts/memory/OBSERVATIONS.md`.
- AI Heartbeat Reflector: periodically promotes durable observations into rules, skills, or axioms.
- Crontab Monitor: audits scheduled jobs and sends an alert email when failures are detected.
- AI News Survey: generates a daily or weekly AI industry report.

Agentic jobs should write compact loop traces under `contexts/loop_runs/` so failures can be diagnosed from a stable artifact instead of only from cron output.

## Example Schedule

```cron
# AI Heartbeat Observer, daily at 08:00.
# Writes traces under contexts/loop_runs/ai_heartbeat/heartbeat_observer/.
0 8 * * * cd /path/to/your/workspace && python3 periodic_jobs/ai_heartbeat/src/v0/observer.py

# AI Heartbeat Reflector, weekly on Sunday at 09:00.
# Writes traces under contexts/loop_runs/ai_heartbeat/heartbeat_reflector/.
0 9 * * 0 cd /path/to/your/workspace && python3 periodic_jobs/ai_heartbeat/src/v0/reflector.py

# Crontab Monitor, daily at 09:00
0 9 * * * cd /path/to/your/workspace && python3 periodic_jobs/ai_heartbeat/src/v0/jobs/crontab_monitor.py

# AI News Survey, weekday morning
0 8 * * 1-5 cd /path/to/your/workspace && python3 periodic_jobs/ai_heartbeat/src/v0/jobs/ai_news_survey.py --mode daily
```

## Notes

Replace `/path/to/your/workspace` with the real absolute path. Cron does not automatically load interactive shell configuration, so make environment variables explicit or load `.env` inside scripts. Keep logs in a persistent location when the job matters.
