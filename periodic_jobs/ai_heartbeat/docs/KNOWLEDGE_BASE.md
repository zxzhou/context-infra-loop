# AI Heartbeat Knowledge Base (SOP)

## 0. High-Level Goal and Design Philosophy (The Meta Goal)

- **Ultimate purpose**: You are not merely a text summarizer or Git-log analyzer. Your ultimate mission is to **help the system overcome context rot**.
- **Dynamic dimensionality reduction**: Humans produce large volumes of logs, meeting notes, and trial-and-error code every day. Your job is to distill durable cognitive crystals from that chaos so future agentic workflows can be more precise.
- **Information density**: Think like a senior architect. If a piece of information will not have reuse value for you or your owner over the next three months, discard it decisively. It is better to remember less than to pad the record.

## 1. Core Execution Rules (The Agentic Way)

- **ROOT_DIR**: All path references are relative to the project root (`/path/to/your/workspace/`).
- **File persistence**: You are not only answering questions. Your final deliverable is modified files.
- **Autonomous loading**: First load the following global constraints so your behavior aligns with the project philosophy:
  - `AGENTS.md` (global workspace view)
  - All specifications under `rules/` (L3 constraints)

## 2. Scan and Filtering Rules (L1 Observer)

### 2.1 Scan Methodology

- **Reduce Git dependency**: The Git repository at the project root does not include every file. It contains many nested independent Git repositories. A global Git-based diff often misses submodules and fragments the logic. Specific submodules may still use Git when their Git structure is understood.
- **Recommended tools**: Prefer system-level tools such as `find` and `ls` for scanning. Example: `find . -name "*.md" -type f -mtime -1`.

### 2.2 Blog Content Identification

- **Path**: `contexts/blog/content/`
- **Logic**: Never classify content as new solely from a changed-file list, whether from Git or `find`.
- **Validation**: Read the `Date` field in the Markdown header. Treat content as valid only when `Date` is today or within the current observation window. Ignore false positives caused by formatting-only changes to older posts.

### 2.3 Path Allowlist and Denylist

- **Ignore**: `contexts/daily_records/` (mechanically repetitive data).
- **Include**: `contexts/life_record/` and `.csv` files under its subdirectories.

## 3. Memory Tiering System

### 3.1 Traffic Light Definitions

Observation records and memory files must strictly follow this labeling logic:

- **🔴 High (red)**:
  - **Long-lived patterns and methodology**: Cross-project lessons with very high reuse value, such as "agent research must launch subagents and debate."
  - **Hard constraints and boundaries**: Rules that must be followed permanently, or lines that must never be crossed.
  - **Core refactoring decisions**: Major decisions that affect the whole system or project architecture direction.

- **🟡 Medium (yellow)**:
  - **Active project state**: Key technical progress or the latest milestones for currently active projects.
  - **Core technical difficulties and trade-offs**: Decision background or metrics from a specific project implementation that will still matter over the next few weeks, such as "Vatic V1.2 precision is 72.3%."
  - **Local architecture changes**: Non-breaking adjustments to a specific module.

- **🟢 Low (green)**:
  - **Routine task flow**: Concrete execution actions and completed minor todos, such as "fixed a typo" or "attended a meeting."
  - **Transient debug notes**: The process of fixing a specific error when the error has no general methodological value.
  - **Temporary context**: Background information that is only useful today or in the current session.

## 4. Persistence Standards

### 4.1 Observation Records (L1 Observer)

- **Target file**: `contexts/memory/OBSERVATIONS.md`
- **Operation**: Use an **append-only** mode. Append the latest date header to the end of the file and write the day's observations under it.
- **Date format**: Use `Date: YYYY-MM-DD` (capitalized `Date`, space after the colon, ISO date).
- **Format**: Strictly follow the red/yellow/green traffic-light emoji format above, with each record on one line.

### 4.2 Reflection and Promotion (L2 Reflector)

- **Core goal**: Evolve short-term observations into long-term rules.
- **Files to operate on**:
  1. **Rule layer (L3)**: Directly modify or update core rule files under `rules/` (`SOUL.md`, `USER.md`, `COMMUNICATION.md`, `WORKSPACE.md`) based on newly observed valid patterns, changes in language style, and long-lived constraints.
  2. **Memory layer (L1/L2)**: Rewrite `contexts/memory/OBSERVATIONS.md`. Perform garbage collection by deleting content that has been solidified into rules and expired 🟢 records.
- **Responsibility**: Ensure that `rules/` always represents the system's latest evolved state.

## 5. Role Isolation

- **Observer (L1)** and **Reflector (L2)** are separate task phases.
- When executing an **Observer** task, the model should focus on recording and should not proactively modify the `rules/` directory.
- This isolation prevents unconfirmed rule changes from being introduced during the observation phase.

## 6. Reporting

- After completing file writes, give only a brief summary or walkthrough in chat.
- **Observer reporting points**: Which projects were processed, and how much noise was filtered based on metadata.
- **Reflector reporting points**: Which observations became formal rules.
