# Crontab Configuration Guide

This document describes the scheduled jobs needed by the context infrastructure system.

---

## Current Local Installation State

The following entries were read from the current user's real `crontab -l` on 2026-07-06. This section records the cron jobs actually running on this machine. The later "Example crontab configuration" section is the recommended context infrastructure template and may not currently be installed.

### Environment

```cron
PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
```

### YouTube Summary Email Agent

- **Time**: Every hour on the hour
- **Project path**: `/Users/davidzhou/Desktop/vibe/vibeG/AutoYoutubeSummaryEmailAgent`
- **Command**: Run `main.py` with the project's `venv/bin/python3`
- **Log**: `/tmp/yt-summarizer.log`
- **Status note**: As of the 2026-07-06 check, the log showed that this job was still running hourly.

```cron
0 * * * * cd /Users/davidzhou/Desktop/vibe/vibeG/AutoYoutubeSummaryEmailAgent && /Users/davidzhou/Desktop/vibe/vibeG/AutoYoutubeSummaryEmailAgent/venv/bin/python3 main.py >> /tmp/yt-summarizer.log 2>&1
```

### Daily Git Activity

- **Time**: Every day at 19:00, 20:00, 21:00, 22:00, and 23:00
- **Project path**: `/Users/davidzhou/Desktop/ai-builder/scripts`
- **Command**: Run `daily-git-activity.sh`
- **Log**: No explicit redirection; output follows cron's default delivery path.
- **Status note**: The script uses `.daily-activity-last-run` internally to prevent duplicate commits on the same day.

```cron
0 19-23 * * * cd /Users/davidzhou/Desktop/ai-builder/scripts && bash daily-git-activity.sh
```

### Market Scout Premarket Email

- **Time**: Monday through Friday at 06:30
- **Project path**: `/Users/davidzhou/Documents/Market scount demo`
- **Command**: Run `tools/send_premarket_briefing_email.sh` with Homebrew Python 3.12
- **Log**: `/Users/davidzhou/Documents/Market scount demo/logs/premarket_email_cron.log`
- **Status note**: The send script depends on the same-day `reports/premarket_briefing_YYYY-MM-DD.md` already existing. As of the 2026-07-06 check, the 06:30 send failed because the report was not generated until 09:44.

```cron
# MARKET_SCOUT_PREMARKET_EMAIL_START
30 6 * * 1-5 cd "/Users/davidzhou/Documents/Market scount demo" && PYTHON_BIN="/opt/homebrew/opt/python@3.12/libexec/bin/python3" /bin/bash tools/send_premarket_briefing_email.sh >> "/Users/davidzhou/Documents/Market scount demo/logs/premarket_email_cron.log" 2>&1
# MARKET_SCOUT_PREMARKET_EMAIL_END
```

### Market Scout Postclose Email

- **Time**: Monday through Friday at 13:45
- **Project path**: `/Users/davidzhou/Documents/Market scount demo`
- **Command**: Run `tools/send_postclose_summary_email.sh` with Homebrew Python 3.12
- **Log**: `/Users/davidzhou/Documents/Market scount demo/logs/postclose_email_cron.log`
- **Status note**: The send script depends on the same-day `reports/summary_YYYY-MM-DD.md` already existing. If it does not exist, it also checks the older `reports/summary-YYYY-MM-DD.md` format.

```cron
# MARKET_SCOUT_POSTCLOSE_EMAIL_START
45 13 * * 1-5 cd "/Users/davidzhou/Documents/Market scount demo" && PYTHON_BIN="/opt/homebrew/opt/python@3.12/libexec/bin/python3" /bin/bash tools/send_postclose_summary_email.sh >> "/Users/davidzhou/Documents/Market scount demo/logs/postclose_email_cron.log" 2>&1
# MARKET_SCOUT_POSTCLOSE_EMAIL_END
```

### Context-Infra Example Jobs Not Currently Installed

`AI Heartbeat Observer`, `AI Heartbeat Reflector`, `Crontab Monitor`, and `AI News Survey` currently appear only in this document's examples. They do not appear in the current user's `crontab -l` output. To enable them, use the example configuration below and replace the paths with real paths.

---

## Timeline Overview

```text
3:05 AM   -> Situation Awareness: daily summary + camera cache refresh
4:00 AM   -> Session Sync: export AI session archive
6:30 AM   -> WeChat DB Parser: export daily messages to CSV, if applicable
7:00 AM   -> Daily Briefing: generate personal morning briefing -> email
8:00 AM   -> AI Heartbeat Observer: scan file changes and write observations to OBSERVATIONS.md
Every 2m  -> Situation Awareness: snapshot collection for traffic, cameras, and alerts
Every 12h -> Situation Awareness: wind alert check
Weekly    -> AI Heartbeat Reflector: merge, promote, and clean memory
Daily     -> Crontab Monitor: health audit, send alert email on anomaly
```

---

## Core Job Descriptions

### AI Heartbeat Observer (Daily)

Scans workspace file changes and extracts valuable observations into `contexts/memory/OBSERVATIONS.md`. This is the input side of the three-tier memory system.

- **Script**: `periodic_jobs/ai_heartbeat/src/v0/observer.py`
- **Dependency**: OpenCode Server API (`OPENCODE_API_URL`)
- **Recommended time**: Daily at 8:00 AM, after daily briefing

### AI Heartbeat Reflector (Weekly)

Merges, promotes, and cleans accumulated observations in `OBSERVATIONS.md`, distilling them into higher-level cognition.

- **Script**: `periodic_jobs/ai_heartbeat/src/v0/reflector.py`
- **Dependency**: OpenCode Server API (`OPENCODE_API_URL`)
- **Recommended time**: Sundays at 9:00 AM

### Crontab Monitor (Daily)

Autonomously audits the health of all crontab jobs and sends alert email when anomalies are found.

- **Script**: `periodic_jobs/ai_heartbeat/src/v0/jobs/crontab_monitor.py`
- **Dependencies**: OpenCode Server API and Gmail (`GMAIL_USERNAME` / `GMAIL_APP_PASSWORD`)
- **Recommended time**: Daily at 9:00 AM

### AI News Survey (Daily/Weekly)

Invokes an AI agent to generate an AI industry daily or weekly report, which can be published to Kit subscribers or sent as personal email.

- **Script**: `periodic_jobs/ai_heartbeat/src/v0/jobs/ai_news_survey.py`
- **Dependencies**: OpenCode Server API, Gmail, or Kit API
- **Recommended time**: Daily at 8:00 AM for the daily report, or Mondays at 8:00 AM for the weekly report

---

## Example Crontab Configuration

Add the following content with `crontab -e`. **Before use, replace `/path/to/your/workspace` with the real path.**

```cron
# -- Time zone note -----------------------------------------------------------
# All times below are local time. To specify a time zone, add this at the top
# of the crontab:
# TZ=America/Los_Angeles

# AI Heartbeat Observer - daily 8:00 AM
0 8 * * * cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/observer.py >> /tmp/observer.log 2>&1

# AI Heartbeat Reflector - Sundays 9:00 AM
0 9 * * 0 cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/reflector.py >> /tmp/reflector.log 2>&1

# Crontab Monitor - daily 9:00 AM
0 9 * * * cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/jobs/crontab_monitor.py >> /tmp/crontab_monitor.log 2>&1

# AI News Survey daily report - daily 8:00 AM, send personal email
0 8 * * * cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/jobs/ai_news_survey.py --mode daily >> /tmp/ai_news_survey.log 2>&1

# AI News Survey weekly report - Mondays 8:00 AM, publish to Kit subscribers
0 8 * * 1 cd /path/to/your/workspace && /path/to/your/workspace/.venv/bin/python periodic_jobs/ai_heartbeat/src/v0/jobs/ai_news_survey.py --mode weekly --publish-to-kit >> /tmp/ai_news_weekly.log 2>&1
```

---

## Notes

1. **Path replacement**: Every `/path/to/your/workspace` must be replaced with your actual absolute path.
2. **Virtual environment**: The scripts depend on Python packages in `.venv`. Make sure to run `uv pip install -r requirements.txt` first, if applicable.
3. **Environment variables**: The cron environment does not automatically load `.env`. Explicitly load it in scripts, or inject it in crontab with `env $(cat .env | xargs)`.
4. **Time zone**: macOS cron uses the system time zone by default. On Linux servers, set `TZ=` explicitly at the top of the crontab.
5. **Logs**: The examples write logs under `/tmp/`. In production, prefer a persistent path such as `logs/`.
6. **Dependency order**: Observer depends on same-day file changes. Run it after daily briefing and news survey, preferably after 8:30 AM.
