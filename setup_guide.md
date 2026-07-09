# Setup Guide: Context Infrastructure

This is an AI-guided setup guide. Follow it step by step; each completed step should make the workspace feel more useful immediately.

---

## Step 1: Fill In Identity Files (Required, 5 Minutes)

**Value**: After this step, AI behavior becomes personalized immediately. This is the highest-ROI setup step.

### 1a. Fill In `USER.md`

Open `rules/USER.md` and replace the template content with your own information.

At minimum, fill in:

- **Name or preferred form of address**: how you want AI to refer to you
- **Time zone**: prevents time confusion
- **Background**: who you are and what you do
- **Technical interests**: the more specific, the better
- **Things that annoy you**: helps AI avoid communication styles you dislike

**Verification**: After filling it in, ask the AI: "Tell me what you know about me." Check whether it describes you accurately.

### 1b. Customize `SOUL.md` (Optional but Recommended)

Open `rules/SOUL.md` and adjust the AI's core behavioral tone.

The default content is already a good general foundation: direct, opinionated, and low-noise. If you have special preferences, add them to the identity and core operating principles.

---

## Step 2: Explore and Extend Skills (Recommended, 15 Minutes)

**Value**: Understand the skill format and start accumulating your own reusable workflows.

### 2a. Browse Existing Skills

Open `rules/skills/INDEX.md` and quickly scan the existing skill categories:

- **BestPractice**: usable immediately and independent of your tools or projects
- **Workflow**: research, slide creation, cognitive profile extraction, and other workflows that may need adaptation
- **API Guide**: ⚙️ entries need configuration; ✅ entries can usually be used directly

### 2b. Create Your First Skill

Pick something you do often, such as calling an API, processing a type of data, or executing a repeatable workflow. Create `rules/skills/<category>_<name>.md` with this shape:

```markdown
# Skill: Name

## When to Use
When this skill should trigger

## Prerequisites
Tools or configuration required

## Steps
1. Step one
2. Step two

## Example
Concrete command or code
```

Add the new skill to the appropriate category in `rules/skills/INDEX.md`.

### 2c. Install an External Public Skill Repo

The contents of `rules/skills/` are a starter set. You do not need to copy every capability into this repository. For more complete capabilities, start with [`docs/SKILL_ECOSYSTEM.md`](docs/SKILL_ECOSYSTEM.md). It lists independently maintained public skill repos such as Tavily, Google Docs, Outlook, Resend, OpenCode, Process Launcher, PPTX, Typefully, and Stripe.

To install one, give the target repo URL to your AI agent. Tell it to start from the current workspace's `AGENTS.md` / `WORKSPACE.md` and expose exactly one root skill. Keep the generic technical contract in the public repo; keep contact aliases, local paths, endpoints, tokens, and business context in a local overlay.

### 2d. About Axioms

`rules/axioms/` contains 43 decision principles distilled from real experience. They represent the original author's viewpoint and cognitive patterns. They are useful references, but they should not replace your own axioms.

Recommended approach:

- Browse `rules/axioms/INDEX.md` to understand categories and core meanings
- Mark axioms that resonate with you
- Over time, accumulate your own axioms from your own project experience, using the same general format

---

## Step 3: Configure the Memory System (Optional, 30 Minutes)

**Value**: Let AI automatically accumulate your work experience and become more context-aware over time.

### 3a. Understand the Three-Layer Architecture

```text
L3 (global constraints): all files under rules/ -> passively loaded each session
L1/L2 (dynamic memory): contexts/memory/OBSERVATIONS.md -> actively retrieved by agents
```

L3 is configured in Step 1. L1/L2 requires scheduled loops if you want it to run automatically.

### 3b. Configure the OpenCode Server

Scripts under `periodic_jobs/ai_heartbeat/` depend on the OpenCode Server API.

1. Confirm that your local OpenCode Server is running or configure the connection.
2. Set environment variables in `periodic_jobs/ai_heartbeat/.env` or the legacy `periodic_jobs/ai_heartbeat/src/.env` path:
   - `OPENCODE_BASE_URL`, default `http://localhost:4096`
   - `OPENCODE_USERNAME`, default `opencode`
   - `OPENCODE_PASSWORD`, required
   - `OPENCODE_DEFAULT_MODEL`, optional, default `anthropic/claude-opus-4-6`
   - `OPENCODE_MESSAGE_TIMEOUT`, optional, default `3600`
3. Test the command surface:

```bash
python3 periodic_jobs/ai_heartbeat/src/v0/observer.py --help
python3 periodic_jobs/ai_heartbeat/src/v0/reflector.py --help
```

### 3c. Loop Guide: Observer and Reflector

The heartbeat system is intentionally defined as loops, not just scripts. Each loop has a trigger, goal, context inputs, allowed reads and writes, verification rules, terminal states, and trace artifacts.

| Loop | Purpose | Spec | Manual command | Typical schedule |
|---|---|---|---|---|
| Observer | Scan recent workspace activity and append useful observations to durable memory | `periodic_jobs/ai_heartbeat/loop_specs/heartbeat_observer.json` | `python3 periodic_jobs/ai_heartbeat/src/v0/observer.py YYYY-MM-DD` | Daily |
| Reflector | Review accumulated observations, promote durable lessons into rules, and remove low-value memory | `periodic_jobs/ai_heartbeat/loop_specs/heartbeat_reflector.json` | `python3 periodic_jobs/ai_heartbeat/src/v0/reflector.py` | Weekly |

Observer writes only to:

- `contexts/memory/OBSERVATIONS.md`
- `contexts/loop_runs/ai_heartbeat/heartbeat_observer/*.json`

Reflector may write to:

- `contexts/memory/OBSERVATIONS.md`
- `contexts/loop_runs/ai_heartbeat/heartbeat_reflector/*.json`
- selected files under `rules/`, when a durable lesson deserves promotion

Run traces are compact JSON records under `contexts/loop_runs/ai_heartbeat/`. They record metadata such as run ID, prompt hash, model, expected artifacts, session ID, terminal state, and error. They intentionally avoid copying full prompts or secret-bearing logs.

Terminal states matter. A healthy loop ends with a named state such as `WRITTEN`, `NO_SIGNAL`, `PROMOTED`, `NO_PROMOTION`, `SKIPPED_EXISTING_DATE`, `FAILED_TIMEOUT`, or `FAILED_NEEDS_HUMAN`. Use these states when debugging automation rather than reading only the chat transcript.

Recommended first-run sequence:

1. Read `periodic_jobs/ai_heartbeat/docs/KNOWLEDGE_BASE.md`.
2. Run the observer manually for a test date:

```bash
python3 periodic_jobs/ai_heartbeat/src/v0/observer.py 2024-01-15 --no-delete
```

3. Check `contexts/memory/OBSERVATIONS.md` for a `Date: 2024-01-15` entry.
4. Check `contexts/loop_runs/ai_heartbeat/heartbeat_observer/` for a trace file.
5. Run the same observer command again. It should skip because the date already exists and record `SKIPPED_EXISTING_DATE`.
6. Run the reflector manually only after you have enough observations to promote:

```bash
python3 periodic_jobs/ai_heartbeat/src/v0/reflector.py --delete-session
```

7. Review any `rules/` changes before committing.

### 3d. Configure Cron

Add scheduled jobs only after manual runs work. See [`docs/CRONTAB.md`](docs/CRONTAB.md) for the full guide.

Example:

```bash
# Run observer daily at 8:00 AM
0 8 * * * cd /path/to/your/workspace && python3 periodic_jobs/ai_heartbeat/src/v0/observer.py >> /tmp/observer.log 2>&1

# Run reflector every Monday at 9:00 AM
0 9 * * 1 cd /path/to/your/workspace && python3 periodic_jobs/ai_heartbeat/src/v0/reflector.py >> /tmp/reflector.log 2>&1
```

Adjust paths and times to your actual environment.

### 3e. Verification

Use these checks after a manual or cron-triggered run:

```bash
tail -n 80 contexts/memory/OBSERVATIONS.md
find contexts/loop_runs/ai_heartbeat -type f | sort | tail
python3 -m json.tool periodic_jobs/ai_heartbeat/loop_specs/heartbeat_observer.json >/dev/null
python3 -m json.tool periodic_jobs/ai_heartbeat/loop_specs/heartbeat_reflector.json >/dev/null
```

If a loop fails, inspect the latest trace first. Then inspect the OpenCode session if the trace has a `session_id`.

---

## Step 4: Extend Tier 2 Components (As Needed, 30-60 Minutes)

The following components work independently. Configure them as needed; leaving them unconfigured does not affect core functionality.

### Semantic Search (⚙️)

After your `contexts/` directory accumulates enough content, semantic search lets you retrieve history by meaning rather than keywords.

**Requires**: LLM Studio locally or an OpenAI API key

**Configuration**: See `rules/skills/semantic_search.md`

### Share Reports to the Web (⚙️)

Convert research reports to HTML and publish them to your own server.

**Requires**: a server with SSH access

**Configuration**: See `rules/skills/share_report.md`, replacing `<your-domain>` and `<your-server>`

### Email Notifications (⚙️)

Let AI send you an email notification after completing a task.

**Requires**: Gmail App Password

**Configuration**: See `rules/skills/send_email.md`

---

## When the System Starts Feeling Valuable

**After filling in `USER.md` (immediately)**: AI answers become more targeted and less generic.

**After 2-3 weeks of use**: `contexts/` starts accumulating your working record, and AI can cite local context.

**After 1-2 months of memory loops**: Observer starts identifying your work patterns, and Reflector promotes high-value lessons into skills or axioms.

**After 6+ months of accumulation**: The system starts to understand your judgment and decision patterns. AI recommendations begin to feel closer to decisions you would have made yourself.

---

## FAQ

**Q: Can I use the existing axioms directly?**

A: Yes, for understanding the system structure. The actual content represents the original author's perspective. Your own axioms should be distilled from your own experience. See `rules/skills/workflow_cognitive_profile_extraction.md` for an extraction method.

**Q: Can I use the existing skills directly?**

A: ✅ entries can usually be used directly. ⚙️ entries require configuration such as endpoints, API keys, or domains. BestPractice entries are generally usable immediately. More complete tool-oriented capabilities live in standalone public repos; see [`docs/SKILL_ECOSYSTEM.md`](docs/SKILL_ECOSYSTEM.md).

**Q: What does `observer.py` require?**

A: It requires the OpenCode client wrapper in `periodic_jobs/ai_heartbeat/src/v0/opencode_client.py`, an accessible OpenCode Server, and `OPENCODE_PASSWORD` in the environment.

**Q: Can I use another AI agent instead of OpenCode?**

A: Yes. The core logic of `observer.py` is to construct a prompt, call an AI agent, and persist a trace. You can replace `opencode_client` with Claude API, OpenAI API, Codex, or any long-context agent interface that can read files, write files, and return a terminal state.

**Q: Should I run Reflector automatically from day one?**

A: Usually no. Start with manual Reflector runs. Promote memory into `rules/` only when the lesson is reusable beyond the current task, has repeated evidence, and has a clear future trigger.

---

## Next Step

After the system is set up, the real accumulation begins. Keep your work inside this workspace and let AI participate in daily work. Over time, the system becomes more useful because it has more of your real context to learn from.
