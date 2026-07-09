---
title: API Key Management and Invocation Best Practices (1Password CLI)
category: BestPractice
tags: [security, api-key, 1password, op-cli, environment-variables]
difficulty: Medium
related_projects: [dotfiles, debianinit]
created: 2026-02-13
updated: 2026-02-13
---

# API Key Management and Invocation Best Practices (1Password CLI)

This document summarizes how to use the 1Password CLI (`op`) to securely manage and inject API keys in local development and production environments, avoiding plaintext leakage and long-lived key residency.

## 1. Core Principles

1. Do not store plaintext keys in `.zshrc`, repository files, or script arguments.
2. For local development, use `op run --env-file ... -- <command>` to inject keys on demand.
3. In production, use machine identities (Service Accounts); do not rely on desktop-app fingerprint prompts.
4. Keep keys least-privileged, rotatable, and revocable; rotate first after a leak.

## 2. Recommended Pattern for Local Development (Mac)

### 2.1 Use Secret References Instead of Plaintext

Store references in the local file `~/.config/op/env.secrets`:

```dotenv
OPENAI_API_KEY=op://dev/dev-api-keys/openai_api_key
TAVILY_API_KEY=op://dev/dev-api-keys/tavily_api_key
GEMINI_API_KEY=op://dev/dev-api-keys/gemini_api_key
```

This file contains no plaintext keys and can be safely kept on the local machine (permission `600` is recommended).

### 2.2 Command-Level Injection

```bash
op run --env-file ~/.config/op/env.secrets -- python app.py
op run --env-file ~/.config/op/env.secrets -- nvim
```

Advantage: only the target process receives the variables; the current shell's global environment is not polluted.

### 2.3 Fingerprint/Password Authorization

Seeing a 1Password authorization prompt locally is normal security behavior. It is usually triggered only when 1Password is locked, not on every command. The frequency is determined by the auto-lock policy.

## 3. Recommended Pattern for Production (Noninteractive)

The production goal is automatic restart and unattended operation, so it should not depend on desktop authorization.

Recommended approach:

1. Create a 1Password Service Account (read-only, limited to a specific vault).
2. Store `OP_SERVICE_ACCOUNT_TOKEN` securely on the server, such as in a systemd EnvironmentFile.
3. In the startup script, use `op read` to fetch keys, then start the process manager, such as PM2.

Example:

```bash
export OPENAI_API_KEY="$(op read 'op://dev/dev-api-keys/openai_api_key')"
pm2 start ecosystem.config.js --env production --update-env
pm2 save
```

## 4. Anti-Patterns to Avoid

1. Plaintext `export API_KEY=...` in `.zshrc`.
2. Passing keys directly in command-line arguments, where they land in history and can be inspected through processes.
3. Reusing the same keys across dev/staging/prod.
4. Only "importing" keys without rotating them, allowing historical leaks to remain valid long-term.

## 5. Minimal Implementation Checklist

1. Remove plaintext keys from dotfiles.
2. Create a `dev-api-keys` item and standardize field names in snake_case.
3. Use `~/.config/op/env.secrets` + `op run`.
4. Configure the Service Account token injection chain for production.
5. Establish a regular key-rotation process and an emergency leakage response process.

## 6. Calling API Keys in Code

In Python/Node scripts, do not hardcode keys or read .env files. Instead, fetch them with `op read`:

```python
import subprocess
import os

def get_api_key(service: str) -> str:
    """Get an API key from 1Password.

    Args:
        service: e.g. 'tavily_api_key', 'openai_api_key'
    """
    # Prefer environment variables (CI/CD scenarios)
    env_key = os.environ.get(service.upper())
    if env_key:
        return env_key

    # Read from 1Password
    result = subprocess.run(
        ["op", "read", f"op://dev/dev-api-keys/{service}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()

# Usage
api_key = get_api_key("tavily_api_key")
```

**Key points**:
1. Check environment variables first (compatible with CI/CD)
2. Use `op read` for local development
3. Standardize the vault path as `op://dev/dev-api-keys/<service>`
