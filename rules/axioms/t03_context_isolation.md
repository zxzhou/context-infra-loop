---
id: axiom_context_isolation_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T3. Context Isolation: The Source of Multi-Agent Value

## 1. Core Axiom

The leverage of multi-agent systems comes from information-domain isolation (independent contexts + a shared scratchpad), not from imitating organizational charts. The purpose of isolation is not division of labor, but enabling each agent to make better decisions in a clean information environment.

## 2. Deep Reasoning

### Cognitive Load and Context Competition

Cursor falls into loops (fixing Bug A, then reintroducing it while fixing Bug B) because planning and execution details compete for attention in the same context window. When one model carries both high-level planning and low-level implementation, it must first filter a messy pile of information down to what is actually useful for planning before it can make decisions. That imposes enormous cognitive load on the model. The reverse is also true: if the model buries itself in execution first, it can easily forget what the planner said while drowning in implementation details, or lose its focus. The result is poor planning and poor execution, satisfying neither side. This is not a lack of model capability; it is a failure of information architecture -- mixing things that should not be mixed.

Splitting Planner and Executor immediately reduces cognitive load and error rate, even without switching to a stronger model. The Planner can focus on global decisions, verification, and reflection; the Executor can focus on low-level implementation and debugging. This simple layering lets each role work in a relatively clean information environment and therefore make better decisions. The key is that isolation is not about imitating an org chart; it is about making information flow manageable.

### Persistent State and the Amnesia Problem

But splitting roles is not enough. If Planner and Executor still communicate through conversation, they face a fatal problem: once the context window grows long or gets truncated, the Planner's instructions are completely lost. For example, the Planner may say earlier, "remember to run a version compatibility test." After the Executor debugs for a few rounds and Cursor truncates the context window, that sentence disappears. Because it is not in the Executor's context window, the Executor will completely forget it next time. It is like a company where management and execution teams are both busy working hard, but nobody does the small job of writing documentation. As a result, the execution layer cannot track progress and relies entirely on the boss's reminders. The boss also does not remember the technical details and comes back every day asking the same questions.

The solution is to require a shared Scratchpad document. Any thought analysis, test result, bug encountered, and final conclusion goes into that file. Then the Planner can always check the document for current difficulties and progress, and can also leave new task instructions. When the Executor finishes a feature or hits a problem, it updates the document with results and feedback; once the Planner reads it, the information is not forgotten. By turning the conversation pipe into a persistent notebook, we largely solve the LLM context-loss problem. Even if the conversation refreshes temporarily, referencing the document again is enough. The probability of amnesia and stepping into the same hole drops immediately. This is not merely an engineering trick; it turns fragile chat into a persistent state machine.

### Over-Engineering and the Need for Constraints

A stronger Planner (such as o1) brings deeper thinking, but also increases the risk of over-engineering. An experienced senior engineer validates on small-scale data before deploying to large-scale data, saving a great deal of debugging time. But an insufficiently restrained Planner often jumps straight into debugging on the final large-scale dataset, or designs a small program as a Concurrent Large-Scale Platform, making the workflow extremely bloated. It is like hiring a famous consulting firm for a human team: to prove how capable they are, the consultants often produce especially refined, large, and bloated proposals. The people underneath work hard for a long time, but it does not actually help the final business goal and may not improve efficiency.

Therefore isolation must be paired with constraints and explicit verification. Prompt the Planner toward a Founder Mindset: do not always try to build the most impressive platform in the industry in one step; keep a Bias for Action and capture opportunities as they appear. Build a simple prototype first, verify feasibility, then add more functionality step by step. In particular, require the Planner, when assigning tasks to the Executor, to explain why each breakdown is necessary and how it will be verified. Also let the Executor raise questions in the document's feedback area. If the plan seems too complex, the Executor can challenge the Planner to review whether it is truly necessary or break it down further. Use this interaction and acceptance mechanism to control the Planner's reasoning.

### Cross-Checking and Abstract Thinking

Only when contexts remain clean can a multi-agent system perform real cross-checking and abstract thinking instead of drowning in mutual noise. A clean Planner context means it can see the global decision history and verification results rather than being buried by execution details. A clean Executor context means it can focus on the current task rather than being distracted by past planning discussions. This isolation lets the two agents make high-quality decisions in their own information domains, then coordinate effectively through the shared Scratchpad. The result is a system that can both plan thoughtfully and execute precisely, instead of compromising both.

## 3. Application Criteria

**When to use**:
- The task requires both macro-level planning and low-level editing/debugging.
- An agent starts looping/regressing because of context overload.
- A long-running task must span multiple context-window truncations.
- Planning and execution have different failure modes (planning fails by choosing the wrong direction; execution fails in details).

**How to practice**:
1. Define roles by information domain (Planner, Executor, optional Evaluator), not by organizational structure.
2. Give each role an independent context and specify what information each should see.
3. Require a shared scratchpad to record goals, decisions, test results, and next actions.
4. Design clear handoff artifacts: the Planner outputs verification standards and decomposition plans; the Executor outputs execution results and feedback.
5. Periodically perform explicit acceptance checks in the scratchpad rather than relying on implicit understanding.

## 4. Traps

**Trap 1: Isolation becomes silos**. If Planner and Executor contexts are completely isolated without an effective communication mechanism, they become two independent systems acting on their own. The Scratchpad must be alive and updated regularly, not a dead document.

**Trap 2: Over-designing handoffs**. Trying to guarantee perfect communication through complicated handoff protocols instead increases system complexity. The best handoff artifacts are simple, verifiable, and human-readable.

**Trap 3: Isolation becomes evasion of responsibility**. The Executor cannot use "that is not in my context" as an excuse to ignore obvious problems. Isolation is for efficiency, not blame avoidance.

**Trap 4: Ignoring the cost of isolation**. The coordination overhead of multi-agent systems is real. Isolation only pays off when task complexity is high enough, or when a single agent's context has genuinely become the bottleneck.

## 5. Related Axioms

- **T2 Results Certainty Over Process Certainty**: The purpose of isolation is to let each Agent better verify its own output, not to guarantee correctness through micromanagement.
- **T5 Cognition Is the Asset, Code Is the Commodity**: Isolation lets the Planner focus on capturing cognition (understanding, verification standards, decision rationale) instead of drowning in execution details.
- **T6 Dependency Topology Over Task Count**: The granularity of isolation should be determined by information dependencies, not arbitrary task splitting.
- **T7 Isolation-Processing-Verification Loop**: Context isolation is the foundation of this loop: the Planner collects facts and plans in isolation, the Executor processes in isolation, and the shared Scratchpad is the verification interface.
