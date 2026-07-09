---
title: Markdown to HTML Best Practices
category: BestPractice
tags: [markdown, html, pandoc, document-conversion]
difficulty: Easy
related_projects: []
created: 2025-02-12
updated: 2025-02-12
---

# Markdown to HTML Best Practices and Lessons Learned

When converting carefully written Markdown documents to HTML, especially with tools such as Pandoc, we have distilled the following core lessons to ensure accurate and professional formatting.

## 1. Strict Requirements for List Formatting

### Leave a Blank Line
Markdown converters, such as Pandoc, usually require one **complete blank line** between a list, whether unordered or ordered, and the paragraph above it.

- **Incorrect**:
  ```markdown
  Applications of physiognomic language in marriage and dating:
  * Strength matching
  * Fortune matching
  ```
  *Result: the list may be recognized as plain text, so bullet symbols may not appear in the HTML.*

- **Correct**:
  ```markdown
  Applications of physiognomic language in marriage and dating:

  * Strength matching
  * Fortune matching
  ```

## 2. Structural Integrity When Merging Sections

### Newlines Between Sections
When merging multiple Markdown files into one large document, insert **at least two newline characters** between files, meaning one blank line.

- **Reason**: If the previous file ends with text and the next file starts with a `#` heading with no blank line between them, the parser may confuse the heading logic.
- **Best practice**: Explicitly add `\n\n` when merging with `cat` or scripts.

## 3. Logical Reorganization of Headings and Introductions

### Remove Redundant Headings
In ebooks or long tutorials, having a separate `## Introduction` heading in every chapter increases table-of-contents burden and creates visual breaks.

- **Improvement**: Remove the literal `## Introduction` heading and place the introductory text directly after the chapter heading (`#`). This makes the reading experience smoother and better aligned with modern book typography.

## 4. CSS Details for Mobile Adaptation

### Spacing Management
Ensure the HTML `body` or main container has sufficient `padding` (24px or more is recommended) to prevent text from pressing against screen edges on mobile devices.

## 5. Normalizing Symbols and Brackets

### Clean Headings
In the final consolidated document, remove unnecessary brackets or special symbols from headings, such as `## [Chapter Summary]`, whenever possible. A concise `## Chapter Summary` looks more professional and also makes the automatically generated table of contents (TOC) cleaner.
