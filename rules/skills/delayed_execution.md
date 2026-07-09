# Skill: Delayed Execution

Use this to execute a task after a specified delay. It supports two modes: command-line tasks and intelligent tasks.

## When to Use
- You need to perform an action after a period of time, such as checking DNS propagation or sending a reminder
- You need a scheduled task but do not want to use crontab

## Mode 1: Delayed Command-Line Task

Suitable for simple command-line operations, using `sleep` + background execution:

```bash
# Syntax: (sleep <seconds> && <command>) &
# Note: wrap the whole command in parentheses and put it in the background to avoid timeout

# Example: check DNS and send an email after 2 hours
(sleep 7200 && python3 tools/<your-notify-script>.py "DNS Check Result" "$(dig TXT <your-domain> +short)") &

# Example: run a script after 1 hour
(sleep 3600 && /path/to/script.sh) &

# View background jobs
jobs

# Note: background jobs terminate when the shell closes; use nohup for persistence
nohup bash -c "sleep 7200 && python3 tools/<your-notify-script>.py 'Subject' 'Body'" &
```

## Mode 2: Intelligent Delayed Task (OpenCode Agent)

Suitable for complex tasks that require AI judgment, submitted through the OpenCode API:

```bash
# Use --no-wait to run the task asynchronously
# Explicitly state "execute after X time" in the prompt (requires external triggering)

# Actual delay should be triggered together with Mode 1:
(sleep 7200 && python3 tools/opencode_job.py "Check whether the DNS records for <your-domain> and <your-domain> have fully propagated. If complete, send an email notification to <your-email>" --title "DNS Check & Notify" --no-wait) &
```

## Time Conversion

| Time | Seconds |
|------|---------|
| 1 minute | 60 |
| 5 minutes | 300 |
| 10 minutes | 600 |
| 30 minutes | 1800 |
| 1 hour | 3600 |
| 2 hours | 7200 |
| 24 hours | 86400 |

## Best Practices

### Always Redirect Logs

**Critical**: delayed tasks must redirect output to a log file; otherwise issues cannot be debugged.

```bash
# Standard format: nohup + disown + log redirection
nohup bash -c 'sleep 7200 && cd /path/to/your/workspace && python3 tools/opencode_job.py "Task description" --title "Task Name" --no-wait' > /tmp/delayed_task.log 2>&1 &
disown

# Explanation:
# - nohup: ignore SIGHUP so the process does not terminate when the shell closes
# - > /tmp/xxx.log 2>&1: redirect both stdout and stderr to the log
# - &: run in the background
# - disown: remove from the shell job list so it is fully independent
```

### Log File Naming Convention

```bash
# Recommended format: /tmp/delayed_<task_name>.log
/tmp/dns_check_task.log
/tmp/email_notify.log
/tmp/cleanup_job.log
```

### Check Task Status and Logs

```bash
# Check whether the task is running
ps aux | grep "sleep" | grep -v grep

# View logs in real time
tail -f /tmp/delayed_task.log

# View complete logs
cat /tmp/delayed_task.log
```

### Cancel a Delayed Task

```bash
# Find the process PID
ps aux | grep "sleep 7200" | grep -v grep

# Kill the process
kill <PID>
```

## Notes
- You **must** use `nohup` + `disown` to ensure process persistence
- You **must** redirect output to a log file for debugging
- For long-running tasks (>1 day), prefer crontab
- OpenCode tasks are suitable for complex scenarios that require AI judgment
