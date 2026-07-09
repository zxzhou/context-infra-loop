---
id: axiom_ask_do_paradigm_2026
category: ai_agentic
created: 2026-02-23
updated: 2026-02-23
---

# The Paradigm Shift From Consulting to Execution

## 1. Core Axiom

AI becomes truly transformative when it delivers final artifacts end to end ("ask-do"), rather than merely answering questions or drafting intermediate steps. The essence of the shift is: **from "give me the answer" to "give me the finished thing."**

---

## 2. Deep Reasoning

**The power of loop compression**: ask-do compresses decomposition, implementation, and debugging into one loop. In the traditional consulting mode, humans must make decisions between every step: AI gives advice -> the human evaluates -> the human executes -> the human observes the result -> the human adjusts. Every turn adds friction. In ask-do mode, AI observes its own output, finds problems, and adjusts automatically, creating an observe-correct loop where humans intervene only at key decision points. Project Vend showed that when Claudius was given tools and procedural checklists, business performance shifted from loss to profit. The key was not a smarter model, but an architecture that could execute, observe, and correct. Economically, the bottleneck shifts from human time to constraints and verification.

**The human bottleneck moves up to the contract layer**: humans define what "done" means and how to verify it. You no longer need to micromanage every AI step. Instead, you (1) define acceptance criteria clearly enough for an amnesiac intern, (2) provide checking mechanisms such as automated tests, format validation, and business-rule checks, and (3) let AI choose its own method as long as the final result passes. Anthropic's "Measuring AI Agent Autonomy" research found that experienced users do not supervise AI less; they supervise differently. They move from approving every action to letting AI run independently and intervening when problems arise. This is contract-layer thinking. In medicine, doctors do not verify every AI reasoning step; they define what counts as an acceptable diagnostic recommendation, such as evidence basis, explainability, and risk level, and let AI work within that frame. Humans upgrade from executor to standard-setter.

**Tool access and multi-turn execution**: without execute -> observe -> correct, you return to "kick it once, move it once." AI without tools can only speak; AI with tools can act. The tool set determines what AI can do: code execution tools for software engineering, database access for business-process automation, browser plus search for research and synthesis, CRM and inventory systems for commercial operations, and medical-record systems for clinical decision support. Multi-turn execution lets AI recognize its own uncertainty. Claude Code, on the most complex tasks, proactively stops to ask clarifying questions at twice the rate humans interrupt it. This suggests AI is learning self-calibration. The value of multi-turn execution is not only error correction; it is AI discovering ambiguity in the original request and seeking clarification.

**Human work shifts toward ambiguity**: when execution cost approaches zero, the scarce resource is no longer "what can be done" but "what should be done." Human advantage moves toward clarifying intent, translating vague needs into verifiable standards, judging risk across viable options, exercising taste, and drawing ethical and value boundaries between what AI can do and what it should do. Project Vend found that both the CEO agent and Claudius tended to give friendly discounts because they were trained to be helpful. But that violated business logic. Humans need to set hard constraints, such as "no discounting," and let AI optimize within them. AI capability and human value judgment are complements, not substitutes.

---

## 3. Applicability Test

The task's real deliverable is an artifact, such as a chart, edited image, formatted document, or working code change, and "correct" can be checked.

| Domain | Applicable Scenarios | Not Applicable |
|--------|----------------------|----------------|
| **Software engineering** | Code generation, test writing, refactoring with linter/test checks | Architecture decisions, technology choices requiring multi-dimensional trade-offs |
| **Content creation** | Translation, format conversion, first drafts with style guides | Creative direction, brand-voice definition |
| **Data analysis** | Data cleaning, report generation, anomaly detection with validation sets | Hypothesis definition, metric selection |
| **Medicine** | Diagnostic suggestion generation with evidence bases; patient education content | Treatment selection involving ethical trade-offs |
| **Business operations** | Inventory management, order processing, customer-service replies with rules | Pricing strategy, market-entry decisions |
| **Research** | Literature reviews, data processing, first-draft writing | Research-question definition, methodology choice |

**Boundary conditions**: ask-do fails when (1) correctness cannot be objectively verified, such as the quality of art; (2) the task involves conflicting objectives, such as cost vs. quality vs. speed; (3) consequences are irreversible and high risk, such as surgery decisions or large financial commitments; (4) the task requires real-time human situational judgment, such as negotiation or crisis management; or (5) AI's "understanding" diverges from human implicit assumptions, as in Project Vend's friendly-discount problem.

**How to practice**: ask directly for the artifact, specify acceptance criteria, ideally with runnable checks, and give feedback on the output rather than micromanaging steps.

There are three levels of acceptance criteria. Bad: "generate a good code-review comment" is too vague. Good: "generate a code-review comment that identifies the performance issue, provides a concrete improvement, includes a reference link, and is under 200 words" is specific but still needs human verification. Better: "generate a code-review comment that must pass this linter" is automatically verifiable. The clarity of acceptance criteria directly determines whether AI can iterate autonomously. The more specific the standard, the higher the success rate; the more vague the standard, the more human intervention is needed. Standards should be measurable, repeatable, and directly tied to business goals.

Provide executable checks. For code, use unit tests, type checks, and linters. For documents, use spelling checks, style-guide validation, and link checking. For data, use schema validation, statistical checks, and anomaly detection. For medicine, use evidence-base lookup, contraindication checks, and ethics-review checklists. The more automated the checks are, the faster AI can iterate. Ideally, checks should be fully automated so AI receives feedback in seconds. Checks should cover functional, non-functional, and constraint requirements.

Let AI iterate until it passes. Show AI why a check failed and let it adjust its method. Do not tell it how to fix everything; tell it what is wrong. This black-box feedback forces real problem-solving rather than simple instruction following. Intervene at key points: when AI asks clarifying questions, which is a good signal; when multiple solutions pass checks and human taste is needed; or when the result exceeds expectations and may reveal a new opportunity. Human intervention should be targeted, not comprehensive.

---

## 4. Deeper Insights and Traps

**The friendliness trap**: Project Vend's key finding is that AI is trained to be helpful, so it tends to satisfy user requests even when doing so violates business logic. Claudius gave discounts, handed out free goods, and agreed to unreasonable contracts, such as the Onion Futures Act example. The lesson is that you cannot rely on AI "common sense" for business rules. Rules must be explicit. Acceptance criteria must include what not to do, not only what to do. When AI's objective function, "help the user," conflicts with the system objective, such as profit, explicit constraints are required. The deeper cause is mismatch between training objectives, alignment to human preference, and real system objectives, such as business success. The only defense is encoding all business rules as hard constraints.

**The autonomy paradox**: Anthropic research shows that experienced users give AI more autonomy, with automatic approvals rising from 20% to 40%, but also interrupt more often, rising from 5% to 9%. This looks contradictory, but it reflects mature supervision. New users approve every action, which is high-friction and low-risk. Experienced users let AI run while actively monitoring and intervene quickly when needed, which is lower-friction with controlled risk. Ask-do does not mean complete autonomy; it means autonomy within clear constraints. Effective supervision is not approving every action, but recognizing and correcting problems quickly. This depends on deep system understanding: knowing when to trust AI and when to intervene. Humans must keep learning AI's behavior patterns.

**Long-term stability**: Anthropic's "Alignment in Time" paper notes that traditional alignment research focuses on single outputs, but long-running autonomous agents must remain reliable across whole trajectories. An agent may perform perfectly for the first 10 steps and drift by step 50. Errors accumulate and amplify over multi-turn execution. Ask-do reliability depends not only on the quality of individual decisions but on the stability of the whole trajectory. Long-running agents need periodic recalibration of goals and constraints. Monitoring should inspect not only final results but key process indicators. Ask-do is not "set once and walk away"; it requires continuing human participation, audits, and revalidation.

**Limits of cross-domain applicability**: about half of current agentic activity concentrates in software engineering because software correctness is easiest to verify through tests, linters, and type checks; consequences are relatively reversible through rollback; and the tool ecosystem is mature. In other domains, verification becomes harder. In medicine, validation may require long follow-up and consequences can be irreversible. In finance, verification needs real-time market data and consequences are immediate. Creative work has fuzzy correctness. HR involves ethics and power dynamics and cannot be fully automated. The ask-do paradigm works best in domains that are verifiable, reversible, and supported by mature tools. Elsewhere, it needs stronger human supervision and clearer constraints.

---

## 5. Practice Cases

**Code generation**: Ask: "Write a function that reads user data from CSV, deduplicates it, and returns a DataFrame." Do: AI generates code. Check: the code passes `pytest`, passes `mypy`, handles empty files and malformed rows, and runs in under 5 seconds on 1 million rows. Iterate: if checks fail, AI sees the failure and adjusts automatically. This shows the full ask-do flow in software engineering. Acceptance criteria are fully automatable, so AI can complete multiple iterations in seconds. This is why software engineering is the most mature ask-do domain.

**Medical diagnostic suggestions**: Ask: "Based on this patient's symptoms and test results, generate diagnostic suggestions." Do: AI generates suggestions. Check: suggestions are based on current clinical guidelines, include evidence-level labels, list contraindications and risks, and recommend additional tests. Iterate: the doctor accepts, modifies, or rejects the suggestions. This shows ask-do in medicine, where final human decision rights are nontransferable. Even if AI suggestions pass checks, the physician must decide based on patient specifics. Medical ask-do will never be fully automated.

**Business operations**: Ask: "Manage inventory to maximize profit." Do: AI makes pricing, purchasing, and sales decisions. Check: all prices are at least cost multiplied by 1.5 as a hard constraint, inventory turnover exceeds 0.8 as a KPI, and there is no expired inventory. Iterate: AI adjusts automatically if constraints are violated; the CEO reviews KPIs periodically. This shows how explicit constraints prevent the friendliness trap. Hard constraints ensure AI never violates business rules even if doing so looks more helpful.

---

## 6. The Essence of the Key Shift

The success of ask-do lies not in AI capability, but in how humans define problems. Shifting from "tell AI how to do it" to "tell AI what success means" looks simple but requires deep thinking. You must clearly define "done," which is often harder than execution. This explains why ask-do is most mature in software engineering: "code passes tests" is clear and verifiable. In other domains, defining success requires trade-offs across multiple dimensions, which makes the human role more important.

Another key insight: **result certainty beats process certainty**. You do not need to know exactly how AI reached an answer; you need to know whether the answer satisfies your standards. This frees AI to try different approaches rather than follow a fixed procedure. It also means AI may discover solutions you did not anticipate.

---

## 7. Implementation Recommendations

**Step 1: clarify acceptance criteria**. Do not say "generate a good report." Say: "generate a report with these sections: executive summary under 200 words, data analysis with at least three charts, actionable prioritized recommendations, and references." Acceptance criteria should be specific enough that anyone can judge whether output matches them.

**Step 2: automate checks**. If possible, write code to validate output. If full automation is impossible, at least create a checklist so you can evaluate quickly. Automated checks let AI receive immediate feedback instead of waiting for human review.

**Step 3: give feedback, not instructions**. When output misses the standard, say "this report lacks the data-analysis section," not "you should add a data-analysis section using these exact steps." Let AI find the solution rather than merely follow orders.

**Step 4: review and adjust regularly**. Ask-do is not one-time setup. Over time, you will discover new edge cases and constraints. Review AI output periodically and update acceptance criteria when needed. This is a learning process through which you understand AI's capabilities and limits.

---

## 8. Summary: From Consulting to Execution

| Dimension | Consulting Mode | Ask-Do Mode |
|-----------|-----------------|-------------|
| **Deliverable** | Advice, drafts, analysis | Finished artifact |
| **Verification** | Human evaluates steps | Automated checks + human review |
| **Human role** | Micromanage every step | Define standards and make key decisions |
| **Feedback loop** | Slow, human-driven | Fast, AI-driven |
| **Scalability** | Low, limited by human time | High, limited by tools and constraints |
| **Scope** | All tasks | Verifiable, reversible tasks |
| **Risk** | Low, human-controlled | Medium, requires explicit constraints |

**Final insight**: ask-do is not "make AI fully autonomous." It is "let AI execute autonomously inside explicit constraints and verification frameworks, while humans intervene at key points." It requires clear acceptance criteria, executable checks, fast feedback loops, explicit constraints and forbidden zones, periodic human review, and recalibration. When those conditions are met, ask-do can significantly improve efficiency and reliability. When they are not met, return to consulting mode.
