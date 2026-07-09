---
id: axiom_x6_big_picture_system_analysis_2026
category: cross_domain
created: 2026-03-01
updated: 2026-03-01
---

# X6. Big-Picture System Analysis

## 1. Core Axiom

When facing complex systems, missing documentation, and scattered logic, first find the largest decision points. Accumulate questions before seeking answers. Places that contradict your assumptions are the most valuable signals.

## 2. Deep Reasoning

### Methodology Steps

1. **Find the largest decision points first** -- Do not try to understand everything. Grab the main trunk first. Every system has one or several core decisions that determine its overall architecture and behavior. Finding them is more important than understanding the details.

2. **Keep asking and recording questions** -- Questions themselves are clues; do not rush to solve them. Each question points to a cognitive gap. Recording questions is the process of organizing thought.

3. **Aggregate questions to find points of cognitive confusion** -- Multiple seemingly independent questions often point to the same root cause. By aggregating questions, you can quickly locate the system's core confusion points.

4. **Focus on "places that contradict assumptions"** -- The least intuitive parts often hide the system's core or improvement opportunities. These places deserve deeper exploration.

### Relationship to Other Methods

This method complements progressive disclosure (from coarse to fine) and documentation-first work (understanding first, documentation follows). The "Data vs Opinion decision principle" from the source file is already covered by T04 (Data Over Opinion).

## 3. Application Criteria

Applicable scenarios:
- Facing an unfamiliar system or new domain.
- Working with a legacy codebase or complex architecture.
- Projects with missing or incomplete documentation.
- Needing to quickly establish a panoramic understanding of a system.

## 4. Relationship to Other Axioms

- **T04 Data Over Opinion** -- The decision principle from the source file is already covered by T04; this axiom focuses on methodology.
- **X02 Hypothesis-Driven Systematic Debugging** -- Both use hypothesis-driven methods, but X02 focuses on debugging while this axiom focuses on system analysis.
- **M02 Reverse Debugging Mindset** -- Both accelerate cognition by narrowing the possibility space.
