# Interview Evaluation Framework in the AI Era

Interview evaluation shifts from assessing Skill to assessing Trait, while also identifying AI-assisted cheating.

## Core Principles

### Roles Are Defined by Trait, Not Skill

Skills depreciate quickly in the AI era. Interviews should assess:
- business sensitivity
- motivation to solve problems
- stress tolerance
- storytelling and persuasiveness

rather than programming ability or framework familiarity alone.

### Senior Interview Strategy Shift

Stop asking "what did you do" and dig into "why" (rationale):
- Why did you choose this solution?
- What alternatives existed? Why did you abandon them?
- What would you do differently if you started over?

Be wary of candidates who use accuracy on imbalanced datasets.

## Identifying AI-Assisted Cheating

### Visual Signals

- Eyes fixed on a narrow area (screen)
- No filler words (normal people pause and hesitate)
- Overly rigorous structure (a typical feature of AI output)

### Logical Signals

- Hallucinations that sound too complete
- Smooth answers even about nonexistent content
- Inability to recognize nonstandard pronunciation of words (AI reads directly instead of recognizing)

### Probe Tactics

1. **Knowledge-cutoff bait**: Invent a nonexistent model/framework/version and observe the candidate's response
2. **Reverse follow-up**: Ask for specific details about something they "just mentioned"
3. **Pronunciation trap**: Use nonstandard pronunciation of a term and observe whether they can recognize it correctly

## Probing Technical Depth

### Auto-Labeling Pipeline Background

For candidates with experience in automated labeling pipelines:
1. **Systematic recall-bias identification**: Does the training data contain systematic bias?
2. **Evaluation blind-spot probing**: Do the evaluation metrics cover all failure modes?

### Edge vs Cloud Decision Framework

Decide across three dimensions:
1. **Latency requirements**: High real-time requirements -> Edge
2. **Criticality**: Severe failure consequences -> Edge + redundancy
3. **Technical feasibility**: Model size vs device compute

In Magic Leap practice, ORB features outperformed frontier approaches such as SuperGlue: classic algorithms can still be valuable in specific scenarios.
