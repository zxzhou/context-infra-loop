---
id: axiom_data_over_opinion_2026
category: tech_decisions
created: 2026-02-23
updated: 2026-02-23
---

# T4. Data Over Opinion in Decisions

## 1. Core Axiom

When measurement is available, support decisions with data and instrumentation rather than opinions and narratives. Data is a direct observation of reality; opinion is an indirect inference about reality. The former can be verified and repeated, while the latter is easily distorted by bias and memory.

## 2. Deep Reasoning

### Signal Quality Determines the Tightness of the Feedback Loop

In my own weight project, the weight signal had high noise and high latency, which rewarded guessing. Weight is affected by water, digestion, hormonal cycles, and many other factors, so a single measurement contains very little information. Even if you look at a weekly average, you must wait seven days to get one data point, which means you cannot quickly connect "what I did" with "what happened." In this high-latency, low-signal environment, the human brain automatically fills gaps with stories instead of evidence. After switching to a more sensitive proxy signal (blood glucose levels, one data point every five minutes), causal relationships became clear: how glucose responds after eating a certain food, how glucose falls after exercise. This tight feedback loop not only improved decision accuracy, but also greatly increased iteration speed and motivation, because the reward cycle shrank from seven days to five minutes. This pattern applies to product development, QA checks, and personal habit optimization: choosing a fast-response, strongly correlated metric often drives behavior change better than choosing the "final goal" metric.

### Data Turns Debate Into Experiment

In Labelbox relabeling checks, manual sampling was fast but low-resolution, and results depended on luck. Two people could look at the same 100 samples and reach completely opposite conclusions -- "labeling quality is good" versus "labeling quality is poor" -- because their samples happened to represent different distributions. After building a quick diff/visualization tool, the decision became full-coverage and reproducible: you could see every labeling error instead of guessing. This converts "I feel" debates into "the data shows" facts. In team decisions, this transformation has enormous value: the most persuasive person no longer needs to win; reality gets to speak. Data does not change because your title is high, and it is not distorted because your argument is elegant.

### Funnel Analysis Forces Priority Ranking

Funnel analysis works because it forces you to locate the largest drop-off before investing effort, avoiding blind micro-optimization. If your conversion funnel loses 80% of users at step two, improving the user experience at step five is a waste of time, even if the step-five optimization is technically more interesting. Data forces you to face reality: invest where the bottleneck is. This is tightly related to M3 (quantified priority), but goes further: not only should you quantify priority, you should also use actual drop-off data to validate your hypothesis. Many teams say "we should improve X," but once you pull out the funnel data, the real bottleneck is often somewhere else entirely.

### Low-Latency Metrics Improve Iteration Speed and Psychological Motivation

High-latency feedback not only reduces accuracy; it also destroys team motivation. If you make an improvement and must wait a month to see the result, you will keep doubting your decision during that month. But if you have a low-latency proxy metric (such as user click-through rate, API response time, or labeling error rate), you can see feedback within hours and adjust immediately. This ability to iterate quickly not only helps you find the optimal solution faster; it also gives the team real-time feedback that "we are making progress," preserving motivation. Psychologically, tight reward loops drive behavior change more effectively than distant large rewards.

## 3. Application Criteria

### When to Use

- **Product conversion decisions**: Use funnel analysis to locate the largest drop-off instead of guessing user pain points by feel.
- **QA/labeling checks**: Use full-coverage diff or visualization tools instead of manual sampling.
- **Debugging**: Use logs, metrics, and reproducible tests instead of "I tried it and it seems fine."
- **Personal habit optimization**: Choose low-latency proxy metrics (glucose, steps, focus time) rather than final goal metrics (weight, health, sense of achievement).
- **Bottleneck identification in multi-step processes**: Any system with multiple stages and an uncertain bottleneck should measure before optimizing.

### How to Practice

1. **Choose a metric**: Find a metric that responds quickly, is strongly correlated, and is easy to measure. It does not need to be the final goal, but it must relate to the final goal.
2. **Build an observation tool**: Create the smallest possible dashboard, diff tool, or visualization that makes the data obvious.
3. **Measure regularly**: Establish a regular measurement cadence (daily, weekly, every iteration) rather than occasional spot checks.
4. **Decompose with funnels**: For multi-step flows, draw the funnel and find the largest drop-off.
5. **Experiment and iterate**: Form hypotheses from data, design controlled experiments (see X2), observe results, and repeat.

## 4. Traps and Counterexamples

### Trap 1: Optimizing the Wrong Metric

Choosing a metric that is easy to measure but unrelated to the real goal leads to "data-driven wrong decisions." Examples include optimizing page load time while ignoring user retention, or optimizing labeling speed while ignoring labeling accuracy. Data itself is neutral, but metric choice reflects your values. Ensure your metric relates to the final goal, even if it is not the final goal itself.

### Trap 2: Over-Relying on Short-Term Metrics

Low-latency metrics are useful, but if you completely ignore long-term metrics, you may get stuck in a local optimum. For example, to increase daily active users, you might make decisions that harm long-term retention. Track metrics across multiple time scales rather than looking only at the fastest feedback signal.

### Trap 3: False Precision When Data Is Insufficient

When sample size is too small or the measurement method is biased, data creates a false sense of precision. Examples include drawing conclusions from only 10 samples, or using biased sampling methods. In this situation, admitting uncertainty is more honest than pretending to have data support.

### Trap 4: Ignoring the Cost Behind Data

Sometimes perfect data is too expensive to obtain. For example, building full-coverage labeling checks may require a complex tool. In that situation, weigh data quality against acquisition cost rather than blindly pursuing perfection.

## 5. Relationship to Other Axioms

- **M3 (Quantified Priority)**: Data is the foundation of quantification. Without data, prioritization becomes guessing.
- **X2 (Systematic Debugging)**: Debugging is experimental design, and experimental results are data. Data drives every step of debugging.
- **V2 (Verifiability)**: Data is the core of verifiability. If you cannot measure it, you cannot verify it; if you cannot verify it, you cannot trust it.
- **T02 (Results Certainty)**: Data is the source of certainty. Opinions may be vague, but data is clear.
- **T03 (Context Isolation)**: Measuring data in isolated contexts can eliminate confounding factors and improve signal quality.

---

**Final thought**: Data does not lie, but it can be misread. The key is choosing the right metric, measuring with the right method, and observing on the right time scale. When you do that, data becomes your most reliable advisor -- one that is not distorted by emotion, bias, or power relationships.
