# AI Heartbeat: Product Requirements Document for a Progressive-Disclosure Memory System

## 1. Product Overview

### 1.1 Vision

Build an **agentic, globally unified, progressively disclosed observation memory system**. Move away from the low-level pattern where external scripts stitch together prompts and feed them to AI. Instead, let the AI engine (OpenCode-Builder) receive a simple "paths and goal" input, then autonomously explore the filesystem, allocate subtasks, and distill observations. The system follows the principle of **Progressive Disclosure**: the memory pool is global, but the context received by the agent remains sparse and high-density.

### 1.2 Core Value Proposition

- **Agentic autonomous exploration**: Scripts only trigger tasks and provide clues, such as file paths. AI is responsible for reading, filtering, such as excluding blog posts with formatting-only changes, and summarizing.
- **Progressive Disclosure**: Detailed memory is not loaded by default. The agent actively retrieves relevant L1/L2 observations based on the current task logic.
- **Global tiered architecture**:
  - **L3**: Global hard constraints, stored in `rules/` and passively loaded globally.
  - **L1/L2**: Dynamic observation logs, stored in the global memory pool and actively retrieved by the agent.
- **Noise-resistant design**: Use AI's semantic understanding to identify genuinely new content. For example, when 300+ blog posts changed only because of formatting, AI should inspect metadata creation dates to identify truly new articles.

### 1.3 Target Users

- **OpenCode-Builder**: The producer and primary consumer of memory.
- **Developer**: The definer of system boundaries and final auditor of memory logs.

---

## 2. Core Design Principles (The Agentic Way)

### 2.1 Reject Push Mode, Embrace Pull Mode

Traditional systems try to push all context to the model. This system requires the agent to develop a pull-oriented mindset. The script tells the agent: "These files changed. Go learn the valuable lessons from them." The agent should decide what to read and how much to read.

### 2.2 Sparse Context Assumption

We assume that for any given task, only a very small subset of memory is truly relevant. Therefore, the global memory pool (`OBSERVATIONS.md`) may keep growing, but the agent must be able to load local subsets efficiently through tags or keywords.

### 2.3 Zero-Friction Assetization

The memory log uses plain-text append mode. It is both the agent's runtime state machine and the developer's knowledge asset.

---

## 3. Functional Requirements: Three-Tier System

### 3.1 L3: Global Constraints and Philosophy

- **Content**: Stored in `rules/SOUL.md` and `rules/USER.md`.
- **Hard constraints**: Must include language-style constraints, such as no grandiose wording, no marketing language, no quotation marks, and avoiding negative "not" constructions where possible, plus response strategies.
- **Loading method**: Passively and globally loaded when a session starts.

### 3.2 L1: Daily Observation and Heartbeat

- **Content**: Key events, technical decisions, and real error-fix experience from the past 24 hours.
- **Labeling format**: `🔴 High (methodology/constraint)`, `🟡 Medium (project state/decision)`, `🟢 Low (task flow)`.
- **Generation method**: The script only provides the set of file paths found by a `find` command, then hands it to OpenCode-Builder. The agent processes autonomously, including calling subagents to read files and inspect metadata.

### 3.3 L2: Memory Distillation and Reflection

- **Responsibility**: Garbage collection.
- **Logic**: Runs weekly. AI autonomously reads the L1 memory pool, deletes expired 🟢 items, merges 🟡 items on the same topic, and promotes general lessons to 🔴.

---

## 4. Key Business Flow (User Story)

### 4.1 Spontaneous Agent Heartbeat Task

1. **Trigger**: The system cron job triggers the script.
2. **Input**: The script runs `find -mtime -1` and obtains a long list of paths, potentially including 300+ changed blog posts.
3. **Allocation**: The script starts an OpenCode-Builder session.
4. **Instruction**: "This is the list of files changed in the past 24 hours. Your goal is to generate observation records. Note: for articles under the blog/ directory, check the `Date` field in their metadata and process only content genuinely created today. Ignore formatting-only changes."
5. **Execution**: After seeing the task, the agent autonomously launches subagents such as librarian/explore workers to read files in parallel, then synthesizes the output.
6. **Output**: Append the result to global `contexts/memory/OBSERVATIONS.md`.

---

## 5. Technical Constraints and Integration

- **Execution engine**: Local OpenCode Server (`localhost:<your-port>`).
- **Core model**: `<your-model>`.
- **Agent identity**: `<your-agent>`.
- **Memory storage**: Markdown files with Git version control support.
