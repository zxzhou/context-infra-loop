# Context Infrastructure

A file-based operating system for AI-assisted work.

This repository stores the durable context that makes AI agents useful across sessions: rules, user preferences, reusable skills, axioms, memory, local tools, scheduled jobs, research notes, publishing utilities, and loop traces.

It is based on [grapeot/context-infrastructure](https://github.com/grapeot/context-infrastructure), with additional loop-engineering and agent-harness modifications focused on making recurring AI work more explicit, auditable, and reusable.

## Why This Exists

Most AI workflows start as conversations. Conversations are useful, but they are weak infrastructure:

- context disappears between sessions
- repeated preferences have to be re-explained
- agent mistakes do not automatically become better systems
- long-running work is hard to resume
- automation fails silently unless traces are designed upfront

This repository treats AI work as an environment-design problem. The model matters, but the harness around the model often determines whether the work becomes repeatable.

In this repo, the harness is made of plain files:

- `AGENTS.md` tells agents how to enter the workspace.
- `rules/` stores durable operating context.
- `rules/skills/` stores reusable workflows.
- `rules/axioms/` stores decision principles.
- `contexts/` stores task evidence, memory, research sessions, and loop traces.
- `tools/` stores local utilities that agents can call.
- `periodic_jobs/` stores scheduled agent workflows.

The goal is not to build a large framework. The goal is to make the working environment legible enough that humans and agents can cooperate without rediscovering the same context every time.

## What This Repository Can Do

You can use this repo as:

- **An agent workspace**: give Codex, Claude Code, OpenCode, or another coding agent a stable home with clear instructions.
- **A personal knowledge harness**: keep reusable preferences, principles, workflows, and context in versioned files.
- **A skill library**: turn repeated workflows into concise operating procedures under `rules/skills/`.
- **A research system**: collect research sessions, source notes, and generated reports under `contexts/survey_sessions/`.
- **A local automation hub**: keep scripts for email, metrics, semantic search, publishing, and recurring jobs.
- **A loop-engineering sandbox**: define recurring agent loops with specs, terminal states, and compact run traces.

## The Harness View

My working model is:

> A useful agent is not just a model. It is a model inside a harness.

A harness includes the pieces that turn model capability into dependable work:

- context construction
- workspace routing
- tool access
- permissions
- durable memory
- verification
- traces
- stop conditions
- handoff artifacts
- human review boundaries

Prompt quality still matters, but prompts alone are not enough. A strong harness makes the task inspectable before, during, and after execution.

For recurring work, this repository uses a loop-oriented frame:

```text
trigger -> context -> action -> verification -> terminal state -> trace -> improvement
```

A good loop should answer:

- What starts the work?
- What goal is the agent responsible for?
- Which files and tools are in scope?
- What is the agent allowed to read or write?
- What counts as done?
- What are the possible terminal states?
- Where is the run trace stored?
- How does a failure become a future improvement?

This is the main loop-engineering extension in this fork: recurring agent work should leave behind enough structure to be debugged, replayed, and improved.

## Repository Layout

```text
.
├── AGENTS.md                  # Entry guide for agents
├── setup_guide.md             # Local setup checklist
├── rules/                     # Durable instructions and reusable context
│   ├── SOUL.md                # Agent posture and operating identity
│   ├── USER.example.md        # User-context template
│   ├── WORKSPACE.md           # Directory routing table
│   ├── COMMUNICATION.md       # Communication preferences
│   ├── axioms/                # Durable decision principles
│   └── skills/                # Reusable workflows and best practices
├── contexts/                  # Working memory and task artifacts
│   ├── memory/                # Optional observation memory
│   ├── loop_runs/             # Compact traces from recurring agent loops
│   └── survey_sessions/       # Research notes and generated reports
├── tools/                     # Local scripts and utilities
├── periodic_jobs/             # Scheduled automation and agent loops
└── adhoc_jobs/                # One-off experiments and standalone tools
```

## Core Files

Agents should start with:

1. `AGENTS.md`
2. `rules/SOUL.md`
3. `rules/USER.md` if present, otherwise `rules/USER.example.md`
4. `rules/WORKSPACE.md`
5. `rules/COMMUNICATION.md`
6. `rules/skills/INDEX.md`

The key habit is simple: read the routing map before searching, read the relevant skill before inventing a workflow, and verify work before reporting completion.

## Skills

Skills are reusable operating procedures. They sit between high-level principles and one-off task notes.

Examples:

- `rules/skills/workflow_deep_research_survey.md`
- `rules/skills/workflow_parallel_subagents.md`
- `rules/skills/workflow_knowledge_flywheel.md`
- `rules/skills/bestpractice_ai_debugging_diagnosis.md`
- `rules/skills/bestpractice_ai_programming_mindset.md`
- `rules/skills/tavily.md`

Each skill should define when to use it, what steps to follow, what quality bar to meet, and what pitfalls to avoid.

When adding a new reusable capability:

1. Create or update a file under `rules/skills/`.
2. Keep it operational and concise.
3. Add it to `rules/skills/INDEX.md`.
4. Prefer examples, commands, and verification steps over abstract advice.

## Axioms

Axioms are decision principles used to frame ambiguous work. They are not rules that must always be applied. They are lenses.

Examples:

- `A04. Reliability Management`
- `A05. Documentation Is Long-Term Memory`
- `A06. Framework Choice Is Worldview Lock-In`
- `T01. Infrastructure Over Components`
- `V02. Verifiability`
- `X02. Systematic Debugging and Hypothesis Testing`

Start from `rules/axioms/INDEX.md`, then load only the few axiom files relevant to the task.

## Agent Loops

The repo currently includes an AI Heartbeat system as a concrete loop example.

The AI Heartbeat has two conceptual loops:

- **L1 Observer**: scans recent workspace activity and appends useful observations.
- **L2 Reflector**: reviews observations and promotes durable lessons into rules, skills, or axioms.

Loop contracts live in:

```text
periodic_jobs/ai_heartbeat/loop_specs/
```

Runtime traces live in:

```text
contexts/loop_runs/
```

A loop trace records metadata such as:

- loop name
- spec path
- run ID
- timestamps
- model/provider, when applicable
- prompt hash
- input parameters
- expected artifacts
- session ID
- terminal state
- startup/runtime error

The trace intentionally avoids full transcripts and secrets. It should be useful for debugging without becoming a data leak.

## Example: AI Heartbeat Loop Specs

Current loop specs:

```text
periodic_jobs/ai_heartbeat/loop_specs/heartbeat_observer.json
periodic_jobs/ai_heartbeat/loop_specs/heartbeat_reflector.json
```

Possible terminal states include:

- `SKIPPED_EXISTING_DATE`
- `WRITTEN`
- `NO_SIGNAL`
- `PROMOTED`
- `NO_PROMOTION`
- `FAILED_TIMEOUT`
- `FAILED_NEEDS_HUMAN`

This is the practical harness idea: a recurring agent should not just "finish." It should finish in a named, inspectable state.

## Setup

1. Clone the repository.
2. Copy `.env.example` to `.env`.
3. Fill in only the credentials needed for the tools you actually plan to use.
4. Read `setup_guide.md`.
5. Run individual tools manually before enabling scheduled jobs.
6. Review `docs/CRONTAB.md` before installing cron jobs.

Example:

```bash
cp .env.example .env
python3 -m py_compile periodic_jobs/ai_heartbeat/src/v0/opencode_client.py
```

Some tools depend on external services such as Tavily, Gmail SMTP, Kit, Typefully, GA4, OpenCode, or a local OpenAI-compatible embedding endpoint. Those are optional. The core repository structure works as a plain file-based context system.

## How To Use This In Your Own Workflow

Start small:

1. Edit `rules/USER.example.md` into your own `rules/USER.md`.
2. Update `rules/WORKSPACE.md` to match your actual directories.
3. Keep only the skills you expect to use.
4. Add one or two personal axioms that actually shape decisions.
5. Use `contexts/survey_sessions/` for research outputs.
6. Add loop specs only after a workflow repeats.

Do not turn every note into permanent memory. The point is not to preserve everything. The point is to preserve what improves future work.

## Design Principles

### 1. Files beat hidden state

Agents should be able to inspect the workspace without depending on invisible application memory. Important context belongs in named files with paths and history.

### 2. Routing beats search

The first move should be reading the routing table, not searching the whole repo. A good workspace tells agents where to look.

### 3. Skills beat repeated prompting

If you explain a workflow more than once, promote it into a skill.

### 4. Verification beats confidence

The system should prefer tests, logs, sources, screenshots, traces, and reproducible commands over fluent claims.

### 5. Loops beat one-off automations

Recurring agent work should have a spec, a trace, terminal states, and a path for improvement.

### 6. Harnesses should stay inspectable

Do not hide too much in frameworks. Plain files, small scripts, and explicit contracts are easier to debug and easier for agents to use.

## Safety And Privacy

This repository is designed to hold personal operating context. Treat it carefully before publishing.

Before pushing your own fork to GitHub:

- remove real API keys and secrets
- review `.env`, logs, generated reports, and memory files
- replace private personal details with examples
- check `contexts/` for sensitive research notes or transcripts
- avoid committing full agent transcripts unless they are intentionally public
- prefer prompt hashes and compact traces over raw conversation dumps

The repository includes `.env.example` for configuration shape. Real credentials should stay in `.env` or an external secret manager.

## What To Customize

Most people should customize these first:

- `rules/USER.md`
- `rules/WORKSPACE.md`
- `rules/COMMUNICATION.md`
- `rules/skills/INDEX.md`
- selected files under `rules/skills/`
- selected files under `rules/axioms/`

Then add tools and loops only when a workflow has repeated value.

## Relationship To Upstream

This repository is based on [grapeot/context-infrastructure](https://github.com/grapeot/context-infrastructure).

The main additions in this version are:

- stronger Codex-oriented workspace instructions
- explicit agent loop and harness concepts
- loop specs for recurring automation
- compact run traces under `contexts/loop_runs/`
- clearer separation between durable rules, task evidence, tools, scheduled jobs, and experiments

The spirit is the same: make AI collaboration better by giving agents durable, inspectable context. The extension here is to treat recurring AI work as engineered loops with observable terminal states.

## Status

This is a living personal infrastructure repo. It is intentionally simple, file-first, and easy to fork. Expect to adapt it to your own agents, tools, privacy boundaries, and working style.
