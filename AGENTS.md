# AGENTS.md - Your Workspace

> **First time here?** Start with `setup_guide.md`. It should get you oriented in under an hour.

This folder is home. Treat it that way: read the local context, preserve the operating system, and leave the workspace easier to use than you found it.

## Every Session

Before doing anything else:

1. Read `rules/SOUL.md` - this is who you are.
2. Read local `rules/USER.md` if it exists; otherwise read `rules/USER.example.md` - this is who you are helping.
3. Read `rules/WORKSPACE.md` - this is the file routing table. Check it before broad file searches.
4. Read `rules/COMMUNICATION.md` - this is how to think and communicate, especially for non-coding tasks.
5. Read `rules/skills/INDEX.md` - this is the reusable skill map.

Do not ask permission for this orientation pass. Just do it.

## Default Flow

1. Orient with the core files above.
2. Load the smallest relevant set of rules, axioms, and skills.
3. Work in the directory indicated by `rules/WORKSPACE.md`.
4. Verify changes with commands, tests, source checks, screenshots, or citations as appropriate.
5. Record durable observations only when they are reusable beyond the current task.

Prefer concrete execution over abstract proposals when the task is clear. If the task is ambiguous, ask the smallest clarifying question that materially changes the work.

## File Routing

**When looking for files, check `rules/WORKSPACE.md` before searching.**

`rules/WORKSPACE.md` is the workspace directory index. In most cases it tells you where a class of content belongs, so you do not need a full-repo glob or grep. If you discover a new durable directory or project that is not represented there, update `rules/WORKSPACE.md` as part of the same change.

Routing defaults:

- Stable reusable guidance belongs in `rules/`.
- Task evidence, research sessions, loop traces, and working context belong in `contexts/`.
- Reusable local utilities belong in `tools/`.
- Scheduled automation belongs in `periodic_jobs/`.
- One-off experiments belong in `adhoc_jobs/`.

## Skills

**Skills** are reusable AI capabilities: workflows, API guides, best practices, and operating procedures.

**Important: when the task is "how to do X", check workspace skills before system tools.**

Search order:

1. The quick-reference table below.
2. `rules/skills/INDEX.md`.
3. Available system tools and plugins.

Task routing:

- **Need to execute a repeatable task**: read `rules/skills/INDEX.md`, then open the relevant skill before acting.
- **Want to add a new capability**: follow the existing skill format and update `rules/skills/INDEX.md`.
- **Need web search, current information, or URL extraction**: read `rules/skills/tavily.md` and use the local Tavily skill when available.

### Common Skill Quick Reference

Use `rules/skills/INDEX.md` as the source of truth.

- **Deep research task**: `rules/skills/workflow_deep_research_survey.md`
  - Flow: initial scan, split dimensions, parallel agents, cross-check, report.
  - Output: `contexts/survey_sessions/`.
- **Background agents / parallel subagents**: `rules/skills/workflow_parallel_subagents.md`
  - Read this before using background or parallel agents.
  - Split only independent scopes, collect complete outputs, and synthesize explicitly.
- **Web search / URL extraction**: `rules/skills/tavily.md`
  - Tavily search/extract CLI outputs stable JSON.
  - Installed under `adhoc_jobs/tavily_skill/`.
  - Requires `TAVILY_API_KEY` in local `.env`.
- **Knowledge flywheel / durable memory**: `rules/skills/workflow_knowledge_flywheel.md`
  - Convert work traces into observations, observations into rules, and rules back into better work.
- **AI debugging**: `rules/skills/bestpractice_ai_debugging_diagnosis.md`
  - Separate context gaps, tool failures, spec ambiguity, model limitations, and verification weaknesses.

## Axioms

Axioms are durable decision principles distilled from prior experience. Use them to frame judgment, especially for strategic, ambiguous, or multi-step work.

Start at `rules/axioms/INDEX.md`. Choose only the 2-5 relevant axiom files for the current task. Do not load the full axiom set by default.

## Agent Loops and Harnesses

This workspace treats reliable agent work as a loop and harness problem, not just a prompt problem.

Use a loop when work is recurring, scheduled, long-running, or expected to improve from traces. A loop should define:

- trigger: what starts the work
- goal: what result the agent is responsible for
- context inputs: which files, rules, data, or sources matter
- allowed reads and writes: where the agent may inspect or modify
- tools and permissions: what capabilities may be used
- verification: how the result is checked
- terminal states: the named ways the loop can end
- artifacts: files, reports, logs, diffs, or messages produced
- trace: compact run metadata for debugging and replay

Loop specs should live near the automation they describe. For AI Heartbeat, specs live in `periodic_jobs/ai_heartbeat/loop_specs/`.

Runtime traces should live under `contexts/loop_runs/`. A trace should record enough to debug the run without dumping secrets or full transcripts:

- loop name and spec path
- run ID and timestamps
- model/provider when applicable
- prompt hash, not necessarily the full prompt
- input parameters
- expected artifacts
- session ID or external run ID
- terminal state
- startup/runtime error if any

Every recurring agent loop should end with a named terminal state, such as `WRITTEN`, `NO_SIGNAL`, `PROMOTED`, `NO_PROMOTION`, `SKIPPED_EXISTING_DATE`, `FAILED_TIMEOUT`, or `FAILED_NEEDS_HUMAN`.

When improving a loop, prefer changes that make failure easier to diagnose: clearer specs, smaller context, stronger verification, better traces, replayable inputs, and explicit stop conditions.

## Codex CLI Working Style

This workspace is primarily operated through Codex CLI. Do not depend on opencode model routing, model categories, or assumptions like Gemini/Sonnet/Haiku/Opus being available through an external router.

Codex principles:

- Read this file and the relevant `rules/` files before acting.
- Reuse workspace skills before inventing a new workflow.
- Finish work inside the current Codex session when feasible.
- Use current Codex tools and plugins for parallelism, GitHub, browser checks, documents, spreadsheets, images, or local execution when available.
- If a needed tool is not available, state the limitation and provide the best executable alternative.

Creative work such as brainstorming, article structure, and viewpoint exploration should still be active and multi-angle. Do not hard-code an external model route. If the user explicitly asks for a specific external model or tool, first check whether the current Codex environment exposes it; use it if available, otherwise explain that it is unavailable here.

## Context Discipline

The context window is valuable. Long documents, logs, search results, and generated traces should be read selectively and summarized. The current Codex session owns final judgment, synthesis, writing, and quality control.

Prefer maps over manuals:

- Read indexes before opening many files.
- Search targeted paths before whole-repo search.
- Pull only the skill, axiom, or source files needed for the decision.
- Keep final answers grounded in verified artifacts, not vibes from a long transcript.

## Memory System

Default memory mode is conservative.

- **L3 global constraints**: `rules/` files are the main durable memory and should be used every session.
- **Task evidence**: put research notes, loop traces, and temporary working context under `contexts/`.
- **Observation memory**: do not default to writing `contexts/memory/OBSERVATIONS.md`.

Only write durable observations when the lesson is reusable beyond the current task. Do not run or rely on `periodic_jobs/ai_heartbeat/` unless the user asks for memory maintenance, scheduled automation, or loop/harness work.

## Verification

A completed task should have an independent check when practical:

- code: tests, type checks, compile checks, lint, or focused execution
- writing: source checks, structure checks, and explicit assumptions
- research: current sources, dates, source tiers, and cross-checks
- UI: screenshots or browser verification
- automation: dry runs, logs, traces, terminal states, and replayable inputs

If a check was not run, say so and explain why.

## Safety

- Do not exfiltrate private data.
- Do not expose secrets, keys, tokens, private logs, or sensitive personal details.
- Do not run destructive commands without asking.
- Do not rewrite unrelated memory, rules, or user work.
- Do not treat generated text as verified fact.
- Preserve file paths and automation contracts unless the user requests a migration.
- When in doubt, ask.
