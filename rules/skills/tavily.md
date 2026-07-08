# Tavily Web Search Skill

Use this skill when a task needs web search, recent information, structured search results, domain-filtered search, image search, or URL content extraction.

## Installed Location

The Tavily skill repo is vendored locally at:

```text
adhoc_jobs/tavily_skill/
```

The upstream skill instruction file is:

```text
adhoc_jobs/tavily_skill/skills/skill_tavily.md
```

Read that file for the full CLI contract before using Tavily.

## Runtime

Run commands from the workspace root with the skill-local Python:

```bash
adhoc_jobs/tavily_skill/.venv/bin/python -m tavily_skill search "latest AI news"
```

For one-shot consumption in the current turn:

```bash
adhoc_jobs/tavily_skill/.venv/bin/python -m tavily_skill search "latest AI news" --stdout
```

For URL extraction:

```bash
adhoc_jobs/tavily_skill/.venv/bin/python -m tavily_skill extract https://example.com --stdout
```

## Configuration

The CLI reads `TAVILY_API_KEY` from the environment or from the workspace `.env`.

Do not commit real keys. Keep them in `.env` or inject them through a secret manager.

## Agent Routing

Prefer Tavily for web search when:

- the user asks to search, look up, verify, or find recent information
- the question depends on current web content
- a deep research workflow needs reproducible JSON search results
- a URL should be extracted into Markdown/text for analysis

Use the built-in browser or other tools only when Tavily cannot satisfy the interaction, such as logging into a site, clicking through UI, taking screenshots, or testing a local web app.

## Troubleshooting

If the CLI fails with a DNS or host-resolution error such as `Failed to resolve 'api.tavily.com'`, separate the problem into two layers before editing the skill:

1. Confirm the API key exists in local `.env` or via `ONEPASSWORD_TAVILY_REFERENCE`.
2. Confirm the vendored virtualenv can start the CLI at all.
3. If the request still fails before any HTTP response, test `api.tavily.com` outside the sandbox.

In restricted Codex environments, Tavily may fail inside the sandbox even when the skill and API key are correct. A successful out-of-sandbox `curl https://api.tavily.com` means the root cause is environment network policy, not the skill implementation.
