---
id: axiom_dependency_topology_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T6. Dependency Topology Over Task Count

## 1. Core Axiom

Choose architecture according to the dependency graph (parallelism, critical path, coupling), not according to how many tasks you can list. Task count is a vanity metric; the real enemies are serial constraints and tight coupling in the topology.

## 2. Deep Reasoning

### The Task Count Trap

Being able to list ten tasks sounds organized, but it hides the real question: what are the dependencies among those ten tasks? If they form one long chain (Task 1 -> Task 2 -> ... -> Task 10), then no matter how many Agents you use, the critical path length determines the final duration. Multi-agent coordination overhead may actually slow the whole system down. Conversely, if those ten tasks can be divided into five groups, with high coupling inside each group but independence between groups, a five-Agent architecture can fully exploit parallelism. Task count itself carries no information; topology does.

### Three Key Dimensions of a Dependency Graph

**Parallelizability**: The maximum number of tasks that can be executed simultaneously at any moment. This directly determines the upper bound of multi-agent value. If parallelism is only 2, no matter how many Agents you add, only two can work at the same time; the rest either wait or do useless work. According to empirical research, when parallelism <= 2, a single Agent is better; at 3-5, an Orchestrator-Worker architecture starts to pay off; only above 5 is it worth considering Hierarchical or Decentralized architectures.

**Critical Path Length**: The longest dependency chain from start to finish. This quantifies serial constraints. Even with high parallelism, if the critical path is long, the entire system is still dragged down by that chain. For example, in educational video generation, the Solution Agent must finish first before Illustration and Narration can proceed in parallel; the Solution -> {Illustration, Narration} chain determines the minimum duration. Shortening the critical path is often more effective than increasing parallelism.

**Coupling Coefficient**: The dependency density between tasks. High coupling means a change in one task's output cascades into multiple downstream tasks, amplifying error propagation. In multi-agent systems, high coupling causes frequent synchronization and recomputation, offsetting the gains from parallelism. Low-coupling systems let each Agent work relatively independently and interact only through clearly defined interfaces.

### Topology-Driven Architecture Choice

These three dimensions jointly determine the optimal architecture. A single Agent fits high-coupling, low-parallelism tasks because it avoids multi-agent coordination overhead. Orchestrator-Worker architecture fits tasks with moderate parallelism (3-5) and clear dependencies; the central coordinator handles task decomposition and scheduling, while Workers execute independently. Hierarchical architecture fits tasks with high parallelism but long critical paths, managing complexity through multi-level recursive decomposition. Decentralized architecture fits low-coupling, high-parallelism tasks where Agents communicate peer-to-peer without a central coordinator.

The key insight is that architecture is not determined by how many Agents you want; it is determined by the task topology. If you first decide "I want to use five Agents" and then force the task into five pieces, you create artificial dependencies and synchronization points, reducing efficiency. The right approach is to draw the DAG first, analyze the topology, and then choose the simplest architecture that matches it.

### Interface Design Over Task Titles

The right design granularity is not task titles ("data cleaning," "feature engineering," "model training"), but the interfaces between tasks: data contracts and handoff artifacts. The interface between two Agents defines their degree of coupling. If the interface is a clear, small, verifiable data structure (such as a JSON schema), then the two Agents can work relatively independently. If the interface is vague, large, or requires frequent negotiation, coupling is high and multi-agent gains are small.

This was clear in the 2026-02-16 "4+4+1" multi-agent real estate research experiment. Four comprehensive Agents each covered the complete document set, but their responsibilities overlapped by 50%; that overlap region was the interface. It was at this interface that the fifth cross-checking Agent found inconsistencies (such as contradictions about garage-conversion feasibility and different interpretations of the 750-square-foot threshold). These inconsistencies were not bugs; they were real contradictions in the information, exposed only through a designed interface and verification mechanism.

### Architecture Must Change When Topology Changes

Architectural decisions can be tested and iterated. If you change the topology (for example, by decomposing tasks differently to reduce coupling or shorten the critical path), the optimal architecture changes too. This means architecture is not a one-time decision; it is tightly coupled to task design. During planning, consider both "what is the optimal architecture under this topology" and "can I simplify the architecture by changing the topology." Sometimes it is more cost-effective to spend time redesigning task boundaries so coupling drops than to add more Agents directly.

## 3. Application Criteria

**When to use**:
- Choosing between single-agent, orchestrator-worker, and hierarchical approaches.
- Planning multi-Agent research, analysis, or delivery work.
- Evaluating the optimal granularity when decomposing large deliverables.
- Diagnosing whether underperformance is a topology problem rather than an Agent capability problem.

**How to practice**:
1. First draw a DAG listing all tasks and their dependencies.
2. Estimate maximum parallelism (number of tasks executable simultaneously) and critical path length (longest dependency chain).
3. Analyze coupling: which tasks' outputs affect multiple downstream tasks? How strong are those effects?
4. Cluster nodes by shared state and data flow, identifying natural Agent boundaries.
5. Choose the simplest architecture that matches the topology (prefer single-Agent first, then consider Orchestrator-Worker, and only then Hierarchical).
6. Define clear interfaces (data contracts, handoff formats, verification standards).
7. Re-measure the topology during execution; if the critical path or coupling changes, re-evaluate the architecture.

**Traps**:
- Being misled by task count and ignoring topology.
- Creating artificial dependencies just to use multi-Agent systems.
- Designing vague interfaces, causing frequent negotiation and synchronization among Agents.
- Ignoring the critical path and wasting optimization effort on non-bottleneck tasks (see X3 Efficiency Is Determined by Bottlenecks).

## 4. Related Axioms

- **T3 Context Isolation Is Multi-Agent Value**: The granularity of isolation should be determined by information dependencies in the topology.
- **T2 Results Certainty Over Process Certainty**: Verify interface outputs instead of enforcing a particular decomposition method.
- **X3 Efficiency Is Determined by Bottlenecks**: The critical path is the system bottleneck; optimization elsewhere does not matter.
- **T05 Cognition Is the Asset, Code Is Consumable**: Understanding topology is more valuable than listing tasks.
