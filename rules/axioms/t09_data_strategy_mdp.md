---
id: axiom_t9_data_strategy_mdp_2026
category: technical
created: 2026-03-01
updated: 2026-03-01
---

# T9. Data Strategy and MDP

## 1. Core Axiom

In AI products, data capture itself is the first-stage product (MDP = Minimum Data Product). Data sovereignty and local accumulation create durable competitive advantage.

## 2. Deep Reasoning

**The Paradigm Shift of the MDP Concept**

Traditional product thinking: product first, data as a byproduct. MDP thinking: data capture itself is the product. This means that before functionality is complete, you first establish a data-collection loop -- even if it is only simple records of user interactions, it becomes a foundation for iteration.

**Breaking the Data Flywheel's Static Point**

When early data is scarce, a VLM (vision-language model) can serve as an initial harvesting tool, quickly generating annotations or features. Human feedback is then introduced to form a loop and gradually improve model quality. This process is not one-off; it is continuous iteration, with each round of feedback strengthening the next round's data quality.

**Architectural Choice for Data Sovereignty**

Local Agents preserve data control, while cloud solutions mean data flows outward. This is not only a technical choice, but also a strategic one. Data accumulated locally becomes an asset that cannot be copied, while cloud dependency creates risks of vendor lock-in and data leakage.

**Entropy Increase in Data Labeling**

As labeling scale grows, quality often declines; this is entropy increase in the labeling process. Sampling audits and continuous quality monitoring are needed to counter this trend and ensure dataset usability.

## 3. Application Criteria

Apply this axiom in the following scenarios:
- When building AI features or ML models, prioritize data-collection mechanisms.
- When choosing cloud versus local architecture, evaluate the cost of data sovereignty.
- When designing personalized systems, establish a loop for local data accumulation.

## 4. Relationship to Other Axioms

- **T04 Data Over Opinion**: Establishes data-first thinking at a higher level.
- **M01 Closed-Loop Calibration**: A data flywheel is essentially a calibration loop that continuously approaches truth through feedback.

**See also**: [Knowledge Flywheel Design Pattern](../skills/workflow_knowledge_flywheel.md) -- brute-force iteration in knowledge engineering
