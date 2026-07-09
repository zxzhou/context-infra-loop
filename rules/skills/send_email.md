# Skill: Send Email via Gmail

This skill allows the AI to send email notifications using a Gmail app-specific password.

## When to Use
- Send report notifications
- Send task-completion reminders
- Send summaries of important information

## Prerequisites
- A `.env` file in the root directory containing:
  - `GMAIL_USERNAME`: The Gmail address used to send the email.
  - `GMAIL_APP_PASSWORD`: A Gmail app-specific password.
  - `GMAIL_RECIPIENTS`: The default recipient address (e.g., `<your-email>`).

## Gmail App Password Setup

1. Go to [Google Account](https://myaccount.google.com/) -> Security -> 2-Step Verification
2. At the bottom: App passwords -> Generate a new app password
3. Add to `.env`:
   ```
   GMAIL_USERNAME=your.gmail@gmail.com
   GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
   GMAIL_RECIPIENTS=<your-email>
   ```

## Usage

### Basic usage (plain text)
```bash
python3 tools/send_email_to_myself.py "Subject Here" "Body Here"
```

### Send to a specific address
```bash
python3 tools/send_email_to_myself.py "Subject Here" "Body Here" --to <recipient-email>
```

### Send HTML content
```bash
python3 tools/send_email_to_myself.py "Subject Here" "<h1>HTML Body</h1>" --html
```

### Send from file (Markdown auto-converted to HTML)
```bash
python3 tools/send_email_to_myself.py "Report Title" "" --file path/to/report.md
```

### Send from file with custom CSS
```bash
python3 tools/send_email_to_myself.py "Report Title" "" --file path/to/report.md --css path/to/styles.css
```

## Markdown to HTML Conversion

When using the `--file` parameter to specify a `.md` file, the script automatically converts Markdown to HTML:
- Headings (`#`, `##`, `###`) -> h1, h2, h3
- **Bold**, *italic*
- [Links](url)
- Lists (`-` and `1.`)
- Tables (`| ... |`)
- Code (`code`)
- Dividers (`---`)

Built-in GitHub-style CSS is included and can be customized with the `--css` parameter.

## Example

Send a markdown report as styled HTML email:
```bash
python3 tools/send_email_to_myself.py "Weekly AI Report" "" --file contexts/survey_sessions/ai_news_weekly.md
```
