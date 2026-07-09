# Project Scaffolding and Restructuring Skill

Organize a temporary directory, loose script directory, or structurally incomplete small project into a standard project shape that can be maintained long term.

**Trigger phrases**: "bootstrap a project", "scaffold a project", "organize this directory into a project", "fill in PRD/RFC/working", "create a separate git repo for this directory"

---

## 1. Applicable Scenarios

When a directory is no longer a one-off script and will be modified repeatedly, handed off across multiple AI sessions, tested, and committed frequently, it should be upgraded into a standard project structure.

Typical signals:

- The directory already contains 2 or more scripts/modules
- The user explicitly asks to add docs, add tests, or commit frequently
- The work will continue to iterate, not just serve one one-off task
- It needs independent git history and should not remain mixed into the workspace monorepo

---

## 2. Public/Private Repo Intake Gate

**Before changing the directory structure, you must first confirm one thing: whether this repo will eventually be published to public GitHub.**

Privacy handling, skill splitting, `.env.example` handling, and fake fixtures all depend on this answer. If scaffolding is already complete before you discover the repo is public, the cost of going back is much higher.

### How to Confirm

At the start of scaffolding, ask the user:

> Will this repo eventually be published to public GitHub, or will it only be used in your workspace/private Git?

Options: `public (will be open-sourced / published to GitHub)` / `private (local use only)`.

Do not skip this step. If the user has not said, ask.

### Mandatory Requirements for Public Repos

If the repo is confirmed public, the following items are mandatory and are not optional optimizations:

1. **`.gitignore` must block private files**. At minimum cover `.env`, `.env.*` (while preserving `!.env.example`), `__pycache__/`, `.pytest_cache/`, `*.pyc`, `dist/`, `build/`, `*.egg-info/`, local data directories, and log directories. For Python projects, add a `py.typed` marker.

2. **Create `.env.example`**. Use fake placeholders for all environment variables; do not leave them empty. Environment variables needed for live tests must be listed in `.env.example` with fake values in the same shape as the real `.env`, so copying it over is enough to start.

3. **Use fake handles/domains/keys in all public files**. `README.md`, docs, tests, fixtures, and scripts must not contain real emails, phone numbers, API keys, internal paths, server addresses, or 1Password vault references. Common fake placeholders:
   - Email: `alice@example.com`, `bob@example.net`
   - Phone: `+15555550123` (North American test range)
   - API key: `replace-with-your-real-key`
   - 1Password: `op://your-vault/your-item/your-field`
   - Domain: `example.com`, `example.org`

4. **README must state that it is publishable**. In the README Privacy section, write: `This repository is designed to be publishable with only fake examples.`

5. **If the project contains a skill, split it into two layers**. Put the technical implementation in the public repo (CLI, tests, API contract, skill workflow docs). Put private contacts, private routing, and private handles in the workspace global skill directory (such as `rules/skills/`) or private `.env`. The public repo's skill docs should clearly state where to find private aliases. Use `adhoc_jobs/resend_email_skill/` (public technical skill) and `rules/skills/imessage.md` (private contact routing) as the reference split.

   Public skill repos should assume loose Markdown-based installation, not vendor-specific skill packaging. The README must explain how a human can hand the GitHub URL to Codex, Claude Code, Cursor, OpenCode, or another coding agent and ask it to install the skill. The AI installer should start from the target workspace's `AGENTS.md` or `CLAUDE.md`, follow any routing file such as `WORKSPACE.md`, and then add the public repo's root skill to the workspace discovery chain. If the workspace has `rules/skills/INDEX.md` or `skills/INDEX.md`, update that index; otherwise add a short pointer in `AGENTS.md` or `CLAUDE.md`.

   If the public repo contains multiple skills, expose exactly one root/router skill to the global workspace level. Use that root skill to link to focused local files inside the repo. Do not symlink every focused skill globally; that makes discovery noisy and makes private/public overlays harder to reason about.

6. **Final privacy check**. During the final verification phase (Phase 4), run a privacy scan:

   ```bash
   rg -n "real email pattern|real phone range|internal path|op://" .
   ```

   It only passes with zero matches. If there are matches, fix them one by one and scan again.

### Handling Private Repos

If the repo is confirmed private, fake fixtures and privacy splitting are not required. A normal `.env.example` and `.gitignore` are still recommended, but fake placeholders are not mandatory.

---

## 3. Target Structure

Minimum recommended structure:

```text
project_root/
├── AGENTS.md
├── .gitignore
├── .env.example        # required for public repos; recommended for private repos
├── docs/
│   ├── prd.md
│   ├── rfc.md
│   ├── working.md
│   └── test.md
├── src/
├── scripts/
├── tests/
└── <compat wrappers / entrypoints if needed>
```

### Responsibilities of Each Directory/File

- `docs/prd.md`: goals, users, requirements, success criteria
- `docs/rfc.md`: architecture, boundaries, key design decisions, migration strategy
- `docs/working.md`: two sections
  - `## Changelog`: one small heading per day, with simple bullets for what changed that day
  - `## Lessons Learned`: records pitfalls, constraints, and mistakes later agents should not repeat
- `docs/test.md`: testing strategy, specifying unit / integration / e2e coverage goals
- `src/`: reusable source code; prefer modules, not user-facing shell entrypoints
- `scripts/`: user-facing CLIs, shell entrypoints, operations scripts
- `tests/`: unit tests, integration tests, future e2e
- `AGENTS.md`: local project rules, especially reminders to update `working.md`, commit frequently, and respect environment requirements

### Recommended Frontend/Backend Scaffold in This Workspace

If the project is clearly a small-to-medium web application, and the goal is to **quickly produce a runnable product first, then evolve it gradually**, the current workspace defaults are:

- **Backend**: FastAPI
- **Frontend**: React + Vite + TypeScript
- **Local storage**: prefer SQLite unless the user explicitly asks for a heavier database
- **Production deployment**: first serve the frontend build artifacts directly through FastAPI

Recommended directory:

```text
project_root/
├── AGENTS.md
├── .gitignore
├── docs/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── scripts/
│   ├── start_backend.sh
│   ├── start_frontend.sh
│   └── build_frontend.sh
├── src/
│   └── <python package>
├── tests/
└── pyproject.toml
```

Additional notes:

1. Maintain `frontend/` as an independent React/Vite project
2. Put only the backend Python package in `src/`; do not stuff backend logic into root scripts
3. Provide stable entrypoints for humans and agents in `scripts/` so commands do not have to be guessed each time
4. In production mode, prefer "FastAPI serves the frontend build from the same origin" so auth, prefixes, and deployment paths remain easier to keep consistent

### Minimum 3 Scripts for Frontend/Backend Projects

For a FastAPI + React project, add these by default:

1. `scripts/start_backend.sh`
   - Activates `.venv`
   - Sets backend environment variables
   - Starts `uvicorn`
2. `scripts/start_frontend.sh`
   - Sets environment variables needed by frontend dev
   - Starts `npm run start_dev_server` or an equivalent command
3. `scripts/build_frontend.sh`
   - Sets build-time base path / token / api base variables
   - Runs `npm run build`

Do not leave these commands only in the README. The scripts themselves are the contract.

### Default Recommendation for URL Prefix / Root Path

If the project may eventually be mounted under a subpath, such as `/foo/bar`, configure a single source of truth during scaffolding.

Default recommendation:

- Drive everything from **one environment variable**, such as `APP_ROOT_PATH`
- Backend reads it and maps it to FastAPI `root_path`
- Frontend reads it and maps it to Vite `base` and React Router `basename`
- `scripts/start_backend.sh`, `scripts/start_frontend.sh`, and `scripts/build_frontend.sh` all derive their own configuration from this single variable

Do not let backend, frontend, and reverse proxy maintain three separate prefix strings. That will almost certainly break when deployed under a subpath.

---

## 4. Recommended Execution Order

### Phase 0: Confirm Public/Private

Run the intake gate in Section 2: ask the user whether this repo will eventually be published to public GitHub.

If the user answers public, carry the public-repo constraints through the entire scaffolding process (`.env.example` fake values, `.gitignore` blocks private files, all public files use fake handles, skill split into two layers). Do not finish and then go back to retrofit them.

### Phase 1: Confirm Project Boundaries

First determine three things:

1. Whether this directory is already worth becoming an independent project
2. Whether the user permits restructuring the directory layout
3. Whether it needs a separate nested git repo

If the user has not authorized restructuring an existing project layout, do not perform a large move on your own.

### Phase 2: Build the Skeleton Before Moving Code

Recommended order:

1. Create `docs/ / src/ / scripts/ / tests/`
2. Write `AGENTS.md`, `.gitignore`, `.env.example`
3. Write `prd.md` / `rfc.md` / `test.md` first
4. Then move code into `src/` and executable entrypoints into `scripts/`
5. Fill in `working.md` last

Do not heavily modify code while improvising the directory structure. Establish the skeleton first so later changes are steadier.

### Phase 3: Preserve Compatibility Entrypoints

If external cron jobs, scripts, or user habits already depend on old paths, do not cut them off first. Prefer compatibility wrappers:

- Keep old paths as thin wrappers
- Put new logic in `src/` / `scripts/`

This lets the refactor complete first and caller migration happen gradually.

### Phase 4: Verification and Privacy Check

After all code and tests are complete, run verification in a fixed order:

1. Lint, if the project has a linter configured.
2. Tests: run default offline tests first, then opt-in integration tests if they exist.
3. Public repos must run a privacy scan:

   ```bash
   rg -n "real email|real phone|internal server|op://|private key pattern" .
   ```

   It only passes with zero matches. If there are matches, fix them one by one and scan again.

4. Write verification results into that day's changelog in `docs/working.md`, recording xxx passed / xxx skipped / xxx found and fixed.

Scaffolding is not delivered until all of Phase 4 has passed.

---

## 5. Git Strategy

If the directory needs long-term maintenance and its history is unrelated to the workspace monorepo, prefer a separate `git init`.

Recommended commit split:

1. **scaffold commit**
   - docs/AGENTS/.gitignore/basic directories
2. **implementation commit**
   - actual code migration, modularization, tests
3. **validation commit**
   - `working.md` records, test results, backfilled or manual verification results

Do not put a large refactor, documentation fill-in, test fixes, and historical backfill into one commit.

---

## 6. Minimum Content for AGENTS.md

The local project `AGENTS.md` should cover at least:

1. Project structure
2. Requirement to update `working.md`
3. Requirement to commit frequently
4. Python / Node / shell environment constraints for this project
5. Any compatibility constraints that must not be broken

If this file is missing, later agents can easily turn the project back into a loose pile of temporary scripts.

---

## 7. working.md Maintenance Requirements

### Changelog

- One date heading per day
- Each bullet describes exactly one change
- Do not use nested bullet points
- Do not write empty phrases such as "made some optimizations"

### Lessons Learned

Only record content that will truly help later agents avoid mistakes, such as:

- Which files are compatibility wrappers and must not be deleted directly
- Which output formats are external dependency contracts
- Which local data sources look like primary sources but are actually auxiliary indexes

---

## 8. What test.md Should Include

At minimum, explain:

- Which pure logic is covered by unit tests
- Which local data or services integration tests depend on
- Whether e2e exists; if it does not yet exist, explain why
- Which artifacts manual verification should inspect

The value of `test.md` is not repeating pytest commands; it is letting later agents know "what counts as verification complete."

---

## 9. Hard Rules When Restructuring an Existing Project

1. Do not perform large directory moves without user permission
2. Build the skeleton before moving code
3. Preserve compatibility before deleting old entrypoints
4. Update `working.md` after each phase completes
5. Every phase must leave the project runnable or verifiable

---

## 10. One-Sentence Judgment Standard

If a directory will continue to be modified in the future, and different AIs/humans should be able to take it over cheaply, it should not remain a "loose script directory"; it should be upgraded to the project skeleton above as soon as possible.

If this repo will eventually be published to public GitHub, Phase 0 must ask the user, and the Phase 4 privacy scan must not be skipped.
