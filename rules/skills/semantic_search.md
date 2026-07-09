# Semantic Search Skill
## 1. Skill Overview

`semantic-search` is a **general-purpose semantic search tool** that can index arbitrary local text files and answer natural-language queries. It goes beyond keyword matching by understanding semantic relationships, and is suitable for any situation where content must be retrieved from a large body of text by meaning rather than literal wording.

The most typical use case is searching the user's personal knowledge base (blogs, logs, research reports), but the tool itself is not limited to that. `--file-list` can point to any collection of text files: chat logs, third-party documentation, research materials, code comments, and more.

**For the user's knowledge base, this is the core tool for retrieving deep preferences and personal philosophy, and it is key infrastructure for AI Heartbeat Step 2 (Reflection Layer).**

### 1.1 When to Use

**Scenario A: Search the user's knowledge base (most common)**
 **Deep background mining**: understand how the user's long-term views on a topic (such as "Agentic AI" or "astrophotography") have evolved.
 **Associative thinking**: find historical experiments, essays, or reflections related to the current task, even when keywords do not match exactly.
 **Decision support**: retrieve past retrospectives or design discussions to inform current architecture decisions.
 **Disambiguation**: when the user mentions a vague concept, find the most relevant historical definition.
 **Build an Axiom / Digital Twin**: when distilling axioms or deep reflections, you **must** run semantic search first to align with historical cognition.

**Scenario B: Analyze any text collection**
 **Third-party content analysis**: retrieve by theme from chat logs, interview transcripts, or meeting notes (for example, "find all discussions where someone talks about AI").
 **Research material mining**: run semantic retrieval across a batch of downloaded documents/reports to find relevant passages that keyword search misses.
 **Cognitive profile extraction**: extract patterns from a large volume of conversation data by dimension, such as technical views, values, and methodology.
 **Cross-document topic discovery**: find semantically related content with different wording across heterogeneous text collections.

### 1.2 Trigger Guidance

**Active triggers (must execute)**:
 When building axiom documents under `rules/axioms/`
 When a task involves the user's core values, methodology, or philosophy system
 When you need to understand the user's "history of thought evolution" in a domain
 When doing reflection-layer work, such as distilling axioms or deep retrospectives
 When you need to extract information from a large text set by theme or semantic dimension, whether or not it is the user's own content

**Passive triggers (explicit user request)**:
 "Search what I previously thought about X"
 "See whether there is any relevant background material"
 "Help me summarize my thinking on topic Y"
 "How did I solve similar problems before?"
 "Find content related to X in this batch of chat logs/documents"
 "Analyze someone's views on topic Y"

---

## 2. Usage

### 2.1 Core Command
```bash
python tools/semantic_search/main.py \
    --file-list tmp/search_files.txt \
    --query "<natural-language query>" \
    --top-k 10 \
    --cache-dir .knowledge_cache
```

### 2.2 Parameter Specification
- `--file-list`: required. Points to a text file containing the list of file paths to search. Recommended location: `tmp/`.
- `--query`: required. A complete, descriptive sentence. For example, "the user's latest thinking on the core contradiction of Agentic AI" is better than "Agentic AI".
- `--top-k`: optional. Number of relevant snippets to return. Default is 5; set to 10 for broader context.
- `--cache-dir`: **must be set to `.knowledge_cache`** (under the repo root) to reuse precomputed embeddings and greatly improve response speed.

---

## 3. Standard Workflow

1.  **Prepare the file list**: filter the knowledge-base areas according to the need (refer to `rules/WORKSPACE.md`).
    ```bash
    mkdir -p tmp
    # Example: search blogs and research reports
    find contexts/blog/content contexts/survey_sessions -name "*.md" > tmp/search_files.txt
    ```
2.  **Run semantic search**:
    ```bash
    source .venv/bin/activate
    export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)
    python tools/semantic_search/main.py --file-list tmp/search_files.txt --query "..." --top-k 10 --cache-dir .knowledge_cache
    ```
3.  **Analyze and synthesize**: read the search results, which usually include score, source_file, and text, then synthesize with metadata such as date and category.
4.  **Clean up**: delete `tmp/search_files.txt` after the task is complete.

---

## 4. Common Search Paths

When searching the user's knowledge base, prioritize these paths:
- `contexts/blog/content/`: deep technical articles and core thinking.
- `contexts/daily_records/`: daily logs that record the most authentic evolution of thought.
- `contexts/survey_sessions/`: deep research conclusions.
- `contexts/life_record/data/`: life audio transcriptions, including daily life summaries and meeting records.
  - 2026 data: `contexts/life_record/data/<YYYYMMDD>/`
  - 2025 data: `contexts/life_record/data/2025/<YYYYMMDD>/`
  - Both daily summary `.md` files and raw transcript `.csv` files can be searched
- `rules/skills/`: distilled methodology.

The above are common shortcut paths. `--file-list` can point to any text-file collection, for example:
```bash
# Search life transcripts (including 2025 and 2026)
find contexts/life_record/data -name "*.md" -not -path "*/.venv/*" > tmp/search_files.txt

# Search WeChat chat logs
find contexts/wechat -name "*.csv" > tmp/search_files.txt

# Search all materials for a research project
find contexts/<your-project> -name "*.md" > tmp/search_files.txt

# Search arbitrary temporary documents
ls adhoc_jobs/some_project/*.txt > tmp/search_files.txt
```

---
**Version**: 1.2.0
**Last Updated**: 2026-03-15
