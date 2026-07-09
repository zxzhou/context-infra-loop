# Practical Guide to AI CLI Agents

## Metadata
- Type: API Guide
- Applicable scenarios: building automation pipelines with CLI Agents, AI calling AI
- Last updated: 2026-03-10

---

## When to Use a CLI Agent Instead of the Raw API

Directly calling an LLM API has shortcomings when handling complex tasks. The core advantages of using a CLI Agent as an intermediate layer:

1. **Counteracts "model laziness"**: APIs are prone to truncated output on large tasks, while agents naturally support looped execution and self-correction
2. **Native file context**: Agents automatically handle file reading, encoding, and writing, decoupling reasoning from IO
3. **Inherited toolchain**: Built-in MCP plugins can invoke Tavily search, execute scripts, and more at any time
4. **Optimized context management**: Automatically handles context-window consumption and long-conversation compaction

---

## Tool Quick Reference

| Dimension | Claude Code | Codex CLI | OpenCode |
|------|-------------|-----------|----------|
| **Open source** | No | No | Yes, 100% |
| **Model binding** | Claude only | OpenAI only | Provider-agnostic (xAI, Anthropic, OpenAI, Google, etc.) |
| **Noninteractive CLI** | `claude --print` | `codex exec` | `opencode serve` + `opencode run --attach` (two steps) |
| **Web API** | No | No | Yes, complete |
| **Recommended scenarios** | Deep reasoning | Automation | Multi-model comparison, automation + visualization |

---

## File-Response Pattern (Core Design Principle)

**Principle**: In production, all input and output should go through files. Do not use pipe mode for core logic.

**Why**:
- **Determinism**: When AI "edits files," its mental model is "finish the work and save it," making truncation less likely
- **Auditability**: Filesystem changes before and after the task (`git diff`) are the single source of truth
- **Capacity**: Avoid command-line argument length limits

**Implementation points**:
- **Input**: The prompt must first be written to a local file, then read by the program
- **Output**: CLI output must be written to a local file, then read and parsed by the program
- **JSON output**: Explicitly require "output only JSON" in the prompt

**Python example**:
```python
import subprocess
from pathlib import Path

# 1. Write prompt to file
Path("prompt.txt").write_text("Your task here...")

# 2. Construct driver prompt
driver_prompt = (
    f"Read the full prompt from {Path('prompt.txt').resolve()}\n"
    f"Write ONLY a JSON object to {Path('output.json').resolve()}\n"
    "Do not include Markdown or extra text."
)

# 3. Execute (Claude Code example)
subprocess.run([
    "claude", "--print", "--output-format", "json",
    "--model", "claude-sonnet-4-6-20260217",
    driver_prompt.replace('\0', '')  # Clean null bytes
])
```

---

## Claude Code Quick Reference

**Basic command**: `claude --print "prompt"`

**Key parameters**:
- `--model`: `claude-sonnet-4-6-20260217` (recommended) or `claude-opus-4-6-20260205` (deep reasoning)
- `--output-format`: `text` / `json` / `stream-json`
- `--permission-mode`: `acceptEdits` / `bypassPermissions`
- `--json-schema`: force output to conform to a JSON Schema

**Recommendation**: Sonnet 4.6 performs close to Opus at only 1/5 the price

---

## Codex CLI Quick Reference

**Basic command**: `codex exec [options] "prompt"`

**Key parameters**:
- `-m, --model`: `gpt-5.2` (recommended)
- `-c model_reasoning_effort`: `low` (translation) / `medium` (general) / `high` (deep refactoring)
- `--full-auto`: automatically accept all operations
- `--json`: JSON output format

**Recommendation**: Use `low` for simple tasks and `high` for complex tasks

---

## OpenCode Quick Reference

OpenCode has two noninteractive invocation methods: CLI (`opencode run`) and the Web Server API.

### Method A: CLI (serve + run --attach)

Running `opencode run` by itself fails with "Session not found" because the built-in server fails to start. The **correct usage** is to start the headless server first, then attach to it:

```bash
# 1. Start a headless server (persistent background process; port is configurable)
opencode serve --port 14097 &

# 2. Send the task (attach to the existing server)
opencode run \
  --attach "http://localhost:14097" \
  -m "xai/grok-4.20-experimental-beta-0304-non-reasoning" \
  --dir "/path/to/project" \
  "your prompt"
```

**Key parameters**:
- `--attach`: connect to an already-running server (required)
- `-m, --model`: `provider/model` format, such as `xai/grok-4.20-experimental-beta-0304-non-reasoning`
- `--dir`: specify the agent's working directory (server-side path)
- `--format json`: JSON event-stream output, suitable for programmatic parsing
- `--agent`: specify the agent (default: build)
- `--variant`: reasoning effort, such as `high`, `max`, `minimal` (provider-specific)

**View available models**: `opencode models | grep xai`

**Server management**:
- The server is bound to a working directory. Start it from a fixed directory to unify session management
- After startup, one server can handle multiple `run --attach` requests
- Stop it with `kill` or `Ctrl+C`

### Method B: Web Server API (Python Programmatic Calls)

Suitable for scenarios that require fine-grained control over the session lifecycle.

**Start server**: `opencode web --port 4096` (or `opencode serve --port 4096`)

**Python client**: `periodic_jobs/ai_heartbeat/src/v0/opencode_client.py` already implements common API wrappers
- `create_session()` / `send_message()` / `get_session_messages()` / `wait_for_session_complete()`

**Model format**: `provider/model` (such as `xai/grok-4.20-experimental-beta-0304-non-reasoning`, `anthropic/claude-sonnet-4-20250514`)

### Choosing a Method

| Scenario | Recommended method |
|------|----------|
| One-off tasks, quick experiments | CLI (serve + run --attach) |
| Batch experiments, need programmatic session control | Web Server API |
| AI calling AI (file-response pattern) | CLI (simpler) or API (more controllable) |

### Common Model Quick Reference

| Provider | Model ID | Characteristics |
|----------|----------|------|
| xai | `grok-4.20-experimental-beta-0304-non-reasoning` | Grok 4.20 non-reasoning, fast |
| xai | `grok-4.20-experimental-beta-0304-reasoning` | Grok 4.20 reasoning version |
| xai | `grok-4-1-fast-non-reasoning` | Grok 4.1 non-reasoning, $0.20/1M input |
| anthropic | `claude-opus-4-6` | Claude deep reasoning |
| anthropic | `claude-sonnet-4-6` | Claude general-purpose, cost-effective |
| openai | `gpt-5.4` | GPT-5.4 (requires Codex plugin) |

---

## AI Calling AI Pattern

If you are writing an agent that calls these CLIs, provide the following meta-instructions:

> "When facing large-scale text processing or filesystem operations, call the underlying CLI Agent:
> 1. Prefer the file-response pattern: first store the content to be processed in a local temporary file
> 2. Use streaming mode (`--json`) and parse events in real time to monitor progress
> 3. Set a reasonable reasoning effort (for example, `low` for translation)
> 4. Clean null characters before passing the prompt (`.replace('\0', '')`)
> 5. For OpenCode, prefer the Web Server API"

---

## Minimalist Design Philosophy (pi-mono)

Core principle from the pi-mono project: **"What's missing matters more than what's included"**

**Core ideas**:
- **Context Engineering is Paramount**: context engineering matters more than tool count
- **Full Observability**: fully observable, with no hidden state
- **External State**: write files instead of maintaining internal state
- **Builder's Mindset**: design for builders, not consumers

**Implication**: In complex tasks, adding features is often a way to avoid the problem. The truly hard decision is: **what should not exist**.

---

## Model Selection Quick Reference

| Task type | Claude Code | Codex | OpenCode |
|---------|-------------|-------|----------|
| **Translation / format conversion** | Sonnet 4.6 | gpt-5.2 + low | *(your lightweight model)* |
| **General development** | Sonnet 4.6 | gpt-5.2 + medium | *(your standard model)* |
| **Deep reasoning / refactoring** | Opus 4.6 | gpt-5.2 + high | *(your reasoning model)* |

---

## OpenCode Production Experience (Quantitative Trading Experiment Summary)

The following comes from hands-on experience running backtesting experiments with OpenCode + Grok 4.20 in a quantitative-trading experiment project.

### Permission Model: Files Must Be Under the Project Root

The OpenCode agent **cannot access paths outside the project root**, including `/tmp/`. All file IO, including prompt input files and JSON output files, must be placed under the working directory used when the server started.

```python
# Wrong: /tmp will be denied by the agent
prompt_path = Path("/tmp/opencode_prompt.txt")

# Correct: place it in the run directory or a local project directory
prompt_path = run_dir / "opencode_prompts" / f"{invocation_id}.txt"
# Or fall back to the project root
prompt_path = Path(".opencode_tmp") / f"{invocation_id}.txt"
```

### Reliability: stdout JSON Fallback

Even if the prompt explicitly asks the agent to "write to a file," the agent may sometimes output JSON directly to stdout without writing the file, or write an empty file. **Production systems must implement stdout JSON extraction as a fallback**:

```python
import re

def _extract_json_from_text(text: str) -> dict | None:
    """Extract a JSON object from stdout (fallback)."""
    # Prefer matching a ```json code block
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    # Fallback: find the largest {...} block
    candidates = re.findall(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text)
    for c in sorted(candidates, key=len, reverse=True):
        try:
            return json.loads(c)
        except json.JSONDecodeError:
            continue
    return None
```

### Concurrency

One `opencode serve` process can handle multiple concurrent `run --attach` requests. Each request creates an independent session. In tests, concurrency of 2 was stable; higher concurrency depends on the LLM provider's rate limits.

### Parameters Unsupported by Grok 4.20

`xai/grok-4.20-experimental-beta-0304-non-reasoning` does not support the `presence_penalty`, `frequency_penalty`, or `stop` parameters. If OpenCode forwards these parameters, the API will error.

### Typical Invocation Flow (File-Response Pattern)

```
1. Write prompt -> run_dir/opencode_prompts/XXXX.txt
2. Construct driver prompt: "Read from {prompt_path}, write JSON to {response_path}"
3. opencode run --attach http://localhost:14097 -m model "driver_prompt"
4. Read run_dir/opencode_responses/XXXX.json
5. If the file is empty -> extract JSON from stdout (fallback)
6. If it still fails -> retry (up to 3 times)
```

### Key Data

- Smoke test: 7/7 successful (zero retries), about 3 minutes wall clock (six 30-minute intervals)
- Average time per decision: ~20-30 seconds (Grok 4.20 non-reasoning)
- Server startup command: `opencode serve --port 14097` (started from the <your-project> directory)

---

## References

- [Claude Code official documentation](https://docs.anthropic.com)
- [OpenAI Codex documentation](https://platform.openai.com/docs)
- [OpenCode official documentation](https://opencode.ai/docs)
