---
title: PDF to Markdown
category: BestPractice
tags: [pdf, markdown, docling, document-conversion]
difficulty: Easy
created: 2026-04-27
---

# PDF to Markdown

When you need to convert PDFs to Markdown for feeding into an LLM, extracting content, or archiving source materials, **use Docling by default**.

## Why Docling

In the OpenDataLoader benchmark of 12 PDF-to-Markdown engines, Docling had the highest overall score (0.882), with the best fidelity for tables and headings. It uses the MIT license, is pure Python, runs on CPU (about 3 seconds/page), and is faster with a GPU.

Do not use the following counterexamples we have tested:

- **MarkItDown**: Built on pdfminer.six; heading-level preservation is 0%, and tables mostly collapse. Office documents are OK; PDFs are not.
- **PyMuPDF4LLM**: Fastest, but AGPL, which restricts commercial use.
- **Marker**: Quality is close to Docling, but it is GPL; commercial use requires payment.

If you want to keep engine-comparison research in your own workspace, put the research notes under project docs or `contexts/`, and link to your local report from this skill.

## How to Use

```bash
uv pip install --python .venv/bin/python docling
```

```python
from docling.document_converter import DocumentConverter

conv = DocumentConverter()
result = conv.convert("input.pdf")
md = result.document.export_to_markdown()
```

The first call downloads about 1 GB of model weights into the HuggingFace cache; later calls reuse them. One `DocumentConverter()` instance can convert multiple files in sequence, so do not create a new instance for every file.

## Acceptance Criteria

- Tables in the output Markdown are preserved with standard `| ... |` syntax and aligned columns
- Heading levels (`#`, `##`, `###`) match the visual hierarchy of the original PDF
- In size terms: text-only PDFs usually compress to Markdown by 5-10x; pure scanned documents will not shrink significantly

## Known Pitfalls

**Section headings can be swallowed**. When a heading in the PDF is emphasized text inside a table rather than a true layout heading, Docling may identify it as an ordinary cell. The symptom is two consecutive `## HOLDINGS` headings with no account name between them. Fix: use context, such as account number or beginning balance, to check the corresponding page in the original PDF, and manually add the section header if needed.

**Two PDFs have identical content but different filenames**. If two converted files have exactly the same character count, compare the original files with `md5` first. They were probably uploaded incorrectly. Docling does not dedupe automatically.

**pip does not exist inside the venv**. Venvs created with uv usually do not include pip, so `venv/bin/python -m pip install` reports `No module named pip`. Use `uv pip install --python .venv/bin/python <pkg>` instead.

## Applicability Boundaries

Not applicable to:

- Scanned / image PDFs: Docling includes OCR, but its accuracy is not as good as dedicated OCR. For pure scanned documents, evaluate Tesseract or a commercial API first
- Complex mathematical formulas: LaTeX can be exported, but fidelity is limited
- Archival scenarios that need to preserve page numbers, headers, and footers: Docling removes these by default
