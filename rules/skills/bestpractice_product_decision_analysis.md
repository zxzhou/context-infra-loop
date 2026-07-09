# Product / Technical Decision Reverse Engineering

When facing a new product, new feature, or competitor move, systematically break down its design decisions, target users, problem being solved, and trade-offs. Avoid stopping at a feature description; drill down into cost structure and strategic intent.

## When to Use

Trigger this skill in scenarios such as:
- "Analyze this new feature/product"
- "Company X released Y; what do you think?"
- "What is this thing actually doing?"
- Any scenario that requires deep evaluation of an external product or technology
- The analysis stage of a research report, after fact collection is complete

## Five-Step Breakdown Framework

### Step 1: Reconstruct the Design Space

Before analyzing "what it chose," first ask "what could it have chosen?"

- List the key decision points in front of this product, usually 2-4
- List the available paths for each decision point
- No need to be exhaustive; focus on paths with substantive differences

**Example** (Claude Interactive Visualizations):
- Output modality: image generation vs code generation vs preset templates
- Lifecycle: temporary vs persistent
- Presentation: inline vs sidebar vs new window
- Target users: developers vs all users

### Step 2: Identify the Choices

Which path did it choose at each decision point? This step is factual description, not judgment.

### Step 3: Infer the Constraints

Why did it choose this path? Each choice is usually driven by one or more constraints:

- **Capability constraint**: What are the team's/model's strengths? (Anthropic is strong at programming -> chooses code generation)
- **Market constraint**: Which position have competitors already occupied? (Google/OpenAI occupy image generation -> differentiate)
- **User constraint**: Where are the target users' capability boundaries? (Non-developers will not use Cursor -> needs zero barrier to entry)
- **Technical constraint**: What are the current feasibility boundaries? (Browser-side rendering -> cannot handle large datasets)
- **Business constraint**: Monetization model or user growth needs? (Open to all users -> expand user base)

**Key question**: Do the constraints conflict? If so, which constraint wins? This often reveals the real strategic priority.

### Step 4: Expose the Trade-Offs

Every choice has a cost. Ask two questions:

1. **What did this choice give up?** Not a hypothetical "what might it have given up," but specific, identifiable features, properties, or user groups.
2. **Who cares about what was given up?** This determines the product's real positioning: whom it serves and whom it does not serve.

**Inversion test**: If it had made the opposite choice, who would benefit and who would be harmed? This thought experiment quickly exposes the core trade-off.

### Step 5: Locate It in the Cost Structure

This is the most important step, and the one most easily skipped.

- **Which part of the cost structure does this product change?** What does it make cheap that used to be expensive?
- **Who gains an ability they did not previously have?** Who are the new beneficiaries?
- **Did this capability already exist?** If it already existed, just behind a higher barrier, then this is not a new capability; it is cost compression.
- **What is the cost of the compression?** Lowering the barrier usually comes with a loss of control, verifiability, or composability.

**Core judgment**: Is it creating a new possibility (0 -> 1), or lowering the barrier to an existing capability (expert -> mass market)? These two have completely different strategic meanings.

## Interface with the Axiom System

This framework is a way to use the axiom toolbox. Different steps naturally connect to different axioms:

| Step | Common Axioms | Trigger Condition |
|------|---------------|-------------------|
| Step 1: Reconstruct the design space | A06 (framework choice locks in worldview) | When the decision involves a framework/platform choice |
| Step 3: Infer constraints | A07 (design philosophy determines the ceiling) | When a choice reflects a deeper design philosophy |
| Step 4: Expose trade-offs | X03 (efficiency is determined by the bottleneck) | When a choice removes one bottleneck but exposes a new one |
| Step 4: Expose trade-offs | A09 (builder thinking is a moat) | When the trade-off involves the Builder vs Consumer divide |
| Step 5: Locate in cost structure | T05 (cognition is an asset, code is a consumable) | When a product changes the cost of "building tools" or "acquiring cognition" |
| Step 5: Locate in cost structure | A13 (three stages of technology adoption) | When judging whether a feature is in the Driver/Co-pilot/Architect stage |

## Output Format

An analysis report should include:

1. **Fact layer** (Steps 1-2): technical implementation, product positioning, known limitations, competitive landscape. Pure facts, without judgment.
2. **Analysis layer** (Steps 3-5): design constraints, trade-offs, cost-structure positioning. This is the core value of the report.
3. **Judgment layer**: conclusions based on the analysis. Give separate judgments for different roles (Builder / Consumer / competitor).

## Common Pitfalls

### Feature Description Trap

Stopping at the level of "what it can do" without asking "why did it do it this way" and "what did it give up." This kind of analysis does not help decisions.

### Isolated Evaluation Trap

Evaluating a new feature without reference to competitors and existing capabilities. You must ask "did this capability already exist?" If the answer is "Cursor could already do this," then the analysis should shift from "new capability" to "cost compression."

### Official Narrative Trap

Organizing the analysis around the official launch messaging. Official narrative is a marketing perspective, not an analytical perspective. Reorganize the facts through your own framework.

## Source

Distilled from the Claude Interactive Visualizations research process (2026-03-16). The key turning point was asking "isn't this just something Cursor could already do?", which lifted the analysis from the feature-description layer to the cost-structure layer.
