---
id: axiom_a06_framework_worldview_2026
category: ai_agentic
created: 2026-02-23
updated: 2026-02-23
---

# A6. Framework Choice Is Worldview Lock-In

## 1. Core Axiom

Choosing an AI framework in a fast-evolving field is not a technical decision; it is a philosophical bet on future adaptability. Every framework is more than a collection of tools. It is a complete worldview about how agents should think, collaborate, and execute. Choosing a framework means seeing the world through its author's assumptions, which can severely limit your depth of understanding and adaptability before the field's foundations have settled.

---

## 2. Deep Reasoning

### 2.1 Every Framework Is a Worldview

Mainstream agentic AI frameworks each encode a different understanding of what agents are. AutoGen believes asynchronous multi-agent collaboration is the key to solving complex problems, so its architecture revolves around message passing and dialogue among agents. LangGraph believes workflows are directed graphs, with state moving between nodes and conditional edges deciding execution paths; that worldview leads to complex persistence, event systems, and async mechanisms. SmolAgents takes a different philosophy: code is the clearest intermediate medium, and agents should generate and execute code directly rather than route everything through abstract tool interfaces. All three can work technically, but their design philosophies are incompatible.

Locking into a framework means your thinking will be shaped by the framework designer's assumptions. If you later develop a different way of thinking, whether from your own practice or a field breakthrough, switching frameworks may be more complex than starting over. Migrating from SmolAgents to LangGraph is not only a code rewrite; it is a whole change in thought pattern because their foundational assumptions do not match.

### 2.2 The Cost of Premature Lock-In in a Fast-Moving Field

Agentic AI is still changing rapidly, and a breakthrough understanding could arrive at any time. AutoGen's move from v0.3 to v0.4 was essentially a rewrite, showing that even mature frameworks may face fundamental rethinking. Premature lock-in creates technical debt and limits your ability to understand the field broadly. When a framework's abstractions bind you, you cannot see the underlying mechanisms clearly. When new understanding appears, you may already be too invested to pivot.

This problem does not exist in the same way in iOS development because GUI programming has had stable foundations for decades. MVC works because it sits on proven foundations that are unlikely to change. Agentic AI's foundations are still fluid. High-level framework abstractions are fragile because they rest on unsettled assumptions.

### 2.3 The Practical Value of Frameworks Is Limited

In the short term, existing frameworks provide much less value than advertised. A complete agent system, LLM plus tool protocol plus multi-turn orchestration, can be built in five minutes. That system contains every core element of agentic AI: a language model that can call tools, a protocol defining tool interfaces, and a loop managing multi-turn conversation. Frameworks do not save much effort. They often add complexity when customization is needed.

Worse, many frameworks over-abstract. When you need to connect existing interfaces or customize behavior, common in enterprise settings, you may have to trace through eight layers of abstraction to find the place to modify. LangChain is infamous for this: a simple change can trap you in a deep inheritance tree where each layer adds another abstraction. This is a typical failure mode in fast-moving fields. High-level abstractions replace builder intuition and become obstacles.

### 2.4 The Fundamental Difference Between Framework and Library

One distinction is critical: not every agentic AI tool is a "framework." pi-mono is an illuminating contrast. It is a library, not a framework. It provides only four basic tools: read, write, edit, and bash. Its system prompt is under 1,000 tokens. Its design philosophy is that what is missing matters more than what is included. The author explicitly rejects popular features such as MCP support, sub-agents, and plan mode because they add context overhead or black boxes.

A framework imposes a worldview; a library provides tools. A framework says, "This is how you should think about the problem." A library says, "Here are tools you can use; how you use them is up to you." LangGraph is a framework. pi-mono is a library. This distinction matters because libraries preserve choice, while frameworks constrain it.

---

## 3. Applicability Test

### 3.1 When to Use a Framework vs. a Library

| Scenario | Use a Framework | Use a Library |
|----------|-----------------|---------------|
| **Domain maturity** | Foundations are stable, such as iOS GUI | Field is still evolving rapidly, such as agentic AI |
| **Team size** | Large teams need a shared way of thinking | Small teams or personal projects |
| **Customization need** | Low; framework defaults are enough | High; frequent lower-level changes are needed |
| **Learning curve** | Willing to learn framework concepts | Want quick start and gradual depth |
| **Long-term stability** | Major framework versions will not change much | Can tolerate lower-level implementation changes |
| **Integration complexity** | Integrations inside the framework are simple | Need to connect many external systems |

### 3.2 Decision Criteria

Before choosing a framework, ask:

1. **Have the field's foundational concepts stabilized?** If not, the framework's high-level abstractions will age quickly.
2. **Do I understand the framework's core assumptions?** If you cannot explain the author's worldview, you are not ready to be locked into it.
3. **What is the migration cost if my thinking changes?** If migration cost is high, framework choice is risky.
4. **Does the framework provide AI-friendly documentation?** If tools like Cursor cannot understand and use the docs directly, the framework's value is reduced in the AI era.
5. **Can I quickly prototype without the framework?** If yes, the framework's value is limited.

---

## 4. Traps and Insights

### 4.1 The "Eight Layers of Abstraction" Nightmare

With an over-abstracted framework, a simple modification becomes a nightmare. You want to change a tool's behavior, but the tool is wrapped in a class, that class inherits from another class, and that class depends on a third class. Eventually you must understand eight layers of interfaces to locate the actual change point. This wastes time and fragments your understanding of the framework.

The problem is especially severe in fast-moving fields because framework designers cannot anticipate every use case. Their abstraction assumptions age quickly, while you remain trapped inside them. pi-mono's author criticizes this directly: over-abstraction is a failure pattern in fast-moving fields.

### 4.2 The Lesson of the Five-Minute Prototype

Building a basic agent system takes only five minutes. This fact matters because it shows that a framework's value is not mainly saving initial development time, but providing a template of "best practices." In a fast-evolving field like agentic AI, however, "best practices" are themselves uncertain. A framework author's best practice may be obsolete six months later.

Therefore, instead of relying on a framework's best practices, build from first principles. The extra cost is small because the basic system is simple. The benefit is large because you preserve flexibility and depth of understanding.

### 4.3 The Shift to Builder's Mindset

Frameworks encourage a passive tool-user mindset: learn the API, think the framework's way, accept its constraints. The agentic AI era needs a builder's mindset. When existing tools do not meet the need, you should be able to build your own quickly.

pi-mono embodies this: it provides a minimal tool set and encourages users to extend capability through Extensions, TypeScript modules, or Skills, markdown files. When the agent needs a new capability, it can read existing extension code, write a new extension, and make it work immediately. This is a shift from "using a framework" to "building your own tools."

### 4.4 Missing AI-Friendly Documentation

Existing agentic AI frameworks do not provide documentation specifically designed for AI. LangGraph, AutoGen, and SmolAgents docs are written for humans and contain natural-language ambiguity and hidden assumptions. When AI tools such as Cursor try to use these frameworks, they must do a lot of trial and error because the docs are not precise enough.

By contrast, pi-mono's tools are code, and the documentation is code comments plus README. AI can read and understand them directly. In the AI era, usability depends not only on whether humans understand a tool, but whether AI understands it.

---

## 5. Related Axioms

**A9. Builder's Mindset Is the Moat** - Framework choice should depend on whether you are willing and able to be a builder. Choosing a framework gives up builder flexibility; staying with libraries preserves builder power.

---

## 6. Practice Recommendations

### 6.1 How to Choose Frameworks in Agentic AI

1. **Start from first principles**: Do not jump directly to frameworks. Understand the core concepts: LLM, tools, and multi-turn orchestration. Build your own system gradually with agentic coding tools such as Cursor. The process itself is learning.

2. **Stay framework-neutral**: Before the field stabilizes, avoid deep dependency on any framework. If you must use one, choose library-like tools with minimal abstraction rather than worldview-imposing frameworks.

3. **Re-evaluate regularly**: Every three months, ask whether the current framework choice still makes sense, whether the field has new understanding, and whether the framework is constraining you.

4. **Invest in transferable knowledge**: Do not learn only framework APIs. Learn the foundations of agentic AI. Those transfer across frameworks; APIs keep changing.

5. **Embrace builder's mindset**: When the framework does not fit, build your own tool instead of forcing yourself into the framework. AI makes this easier by helping you prototype quickly.

### 6.2 When a Framework May Be Worth Considering

Only consider a framework when all of these are true:

- The field's foundations have been stable for at least two to three years
- Major framework versions are stable and do not rewrite frequently
- Your team is large enough to need a unified way of thinking
- The framework's best practices significantly accelerate development
- The framework documentation is clear enough for AI tools to understand

In agentic AI, these conditions are not currently satisfied. Now is not the time to commit to a framework.

---

## 7. Summary

Framework choice is a long-term commitment. It affects how you think, how you learn, and how you adapt. In a fast-moving field, that commitment is risky. Agentic AI is still evolving; its foundations are still forming. Any framework's worldview may soon prove incomplete or wrong.

The wisest approach is to stay framework-neutral, start from first principles, use libraries rather than frameworks, and embrace builder's mindset. The cost is low because basic systems are simple. The benefit is high because you preserve flexibility and understanding. When the field finally stabilizes, frameworks will become truly valuable. By then, you will have the knowledge and experience to choose wisely.
