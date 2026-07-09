# Time-Sensitive Information Verification

## Background

AI models have knowledge cutoff dates and may miss new versions, features, or products released afterward. When information may be time-sensitive, do not judge from training data alone; actively verify it.

## Triggers

Use this when the following types of information may conflict with your knowledge:

- Model names/version numbers (such as Gemini, Claude, GPT)
- Software versions (frameworks, libraries, tools)
- API endpoints or parameters
- Feature updates for known products

## Procedure

1. **Do not directly reject it**: the version number in the user's code may really exist
2. **Use Tavily search to verify**: check whether a new version has been released
3. **Provide accurate information**: include the full version number and release date if available

## Case

### Gemini Model Name (2026-02)

The code contained `gemini-3.0-flash`, which initially looked like an invalid model name.

**After verification**: Gemini 3.0 Flash had indeed been released, but the user had omitted the `-preview` suffix. The correct name was `gemini-3.0-flash-preview`.

**Lesson**: If a model name looks "too new," search first to confirm whether it has been released instead of assuming the user is wrong.

## Search Templates

```
{product name} {version number} release date
{product name} {version number} official announcement
```

Use Tavily search with `search_depth="advanced"` and `max_results=5`.

## Physical Anchor Check

### Principle

In numerical logic, use physical common sense as the final defense for checking complex logic. AI output may look plausible, but if it violates physical laws, it should be questioned.

### Use Cases

- AI-generated technical parameters, such as satellite altitude or device specifications
- Numerical calculation results, including whether the order of magnitude is reasonable
- Causal reasoning, including whether it violates physical laws

### Case

AI gave orbital parameters for a geostationary satellite, but the relationship between altitude and declination did not satisfy Kepler's laws. Physical common sense (a geostationary satellite must be above the equator at about 35,786 km) exposed the hallucination.

### Execution

1. Identify the parts of the output involving physical quantities
2. Do a quick check using known physical common sense, such as unit conversion, order of magnitude, and laws
3. If an anomaly appears, ask the AI to explain again or verify through search
