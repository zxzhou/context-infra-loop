# Core AI Programming Methodology

## Metadata

- **Type**: BestPractice
- **Applicable scenarios**: AI-assisted programming, agent system design
- **Created**: 2026-02-21
- **Source**: Synthesis of multiple AI programming practices
- **Last updated**: 2026-03-01

---

## Foundational Axioms (see axioms for details)

The methodology in this file is built on the following axioms, which are not repeated here:
- **T05**: Cognition is an asset; code is a consumable
- **T02**: Result determinism is better than process determinism
---

## Diagnosing and Solving the "70% Problem"

### Nature of the Problem

The common "70% problem" in AI programming, where AI can complete 70% but the last 30% keeps producing problems, is fundamentally caused by a **broken self-iteration feedback loop**:

1. **AI cannot perceive whether the output meets expectations**: it has no "eyes" on the result
2. **Success criteria are too subjective**: without a clear definition of "good," AI does not know which direction to iterate toward

### Solutions

1. **Open perception channels for AI**:
   - Let AI see runtime results (screenshots, logs, test output)
   - Provide visual feedback when UI is involved
   - Return complete output after commands are executed

2. **Establish clear success criteria**:
   - Define "what good means" (not only "it runs")
   - Quantitative metrics are better than subjective descriptions
   - Provide reference cases or expected output

---

## Relationship Between Reasoning Models and Agentic Workflow

### Complementary, Not Substitutes

- **Reasoning Model**: good at deep analysis, complex reasoning, and planning
- **Agentic Workflow**: good at coordinated execution, tool calls, and state management

### Limitation of Reasoning Models

A reasoning model's "reflection" is stateless: it cannot perceive changes in the external world. By the time thinking ends, the world has already changed.

### Recommended Architecture

Use a **hybrid architecture** in production:
- Reasoning Model handles deep analysis and planning
- Agentic Workflow handles coordinated execution and state management
- External orchestration controls the overall process

---

## Boundaries of Cognitive Outsourcing

As AI becomes more capable and less expensive, it is important to distinguish which tasks can be outsourced and which must be retained:

### Can Be Outsourced

- Finding gaps: information collection and formatting
- Mechanical execution: repetitive coding and document generation
- Rapid prototypes: exploratory implementation

### Must Be Retained

- Forming your own viewpoint
- Defining the problem and success criteria
- Value judgments for key decisions
- Final review of output quality

---

## The Inflection Point Where "Intuition" Beats "Program"

For complex semantic tasks, an LLM's "black-box intuition" may be more resilient and efficient than explicit logic code.

When a task involves:
- complex semantic understanding
- multi-factor trade-offs
- judgments with fuzzy boundaries

LLM end-to-end handling may be more robust than explicit rules. This is a paradigm shift from "program thinking" to "intuition thinking."

---

## The Filesystem as a Natural State Machine

Core design principles for local agent mode:
- The filesystem itself is the most reliable state persistence layer
- State changes = file operations, naturally auditable and reversible
- Avoid the complexity of "in-memory state + manual persistence"

---

## Three Archetypes of Data Scientists in the AI Era

Skills are depreciating, but traits and personality matter more and more. Three roles:

1. **Architect**: defines problems, designs systems, orchestrates capability boundaries
2. **Auditor**: evaluates quality, discovers patterns, cross-validates
3. **Full-stack builder**: delivers end to end, prototypes quickly, verifies integration

Core insight: the same person can play different roles, but making the current role explicit prevents cognitive confusion.

## Notes

- **Productivity trap**: Sacrificing developer mental bandwidth and flow state to save tiny token costs is premature optimization
- **Physical anchor**: The final line of defense for complex logic checks is physical common sense (see `bestpractice_temporal_info_verification.md`)
- **Context rot**: Periodically reflect on and solidify methodology to prevent context from being lost between sessions

---

## Core Decisions for AI Adoption

Distilled from "Key Decisions in AI Adoption Through a Simple Task":

### 1. Use a Local Coding Agent Instead of ChatGPT

- Reduce friction in context transfer and implementation
- The agent operates directly on the codebase instead of copy-pasting
- ChatGPT is suitable for quick Q&A, not system development

### 2. Define Success Criteria Before Starting

- Establish tests as the feedback loop
- Define "what good means," not only "it runs"
- Tests are navigation signals for AI

### 3. Let the Agent Handle Corner Cases Itself

- Result determinism vs process determinism
- Do not prescribe every step in exhaustive detail; let AI decide the implementation path
- Focus on whether the output meets expectations, not whether the implementation process is "correct"

### 4. Divide and Conquer to Handle Context Window Saturation

- 8 subagents process in parallel
- Each subagent has a single responsibility
- Summarize at the end instead of stuffing all information into one context window

### 5. Prompt Bootstrapping and Result Orientation

- Let AI iterate and improve itself
- Do not specify how to do every step
- Use 2 minutes to leverage 45 minutes of AI work: AI is leverage

---

**Last updated**: 2026-03-01
