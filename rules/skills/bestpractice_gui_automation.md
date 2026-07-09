# GUI Automation Methodology

Make an API Out of Things That Don't Provide an API.

## Core Idea

Many systems do not provide APIs, but developer tools, bookmarklets, Playwright, and similar tools can turn API-less interfaces into programmable interfaces.

## Technical Paths

### 1. Dev Tools + HAR Export

HTML elements in dynamic pages, such as infinite-scroll pages, may be dynamically removed. The solution:

1. Open Dev Tools -> Network Tab
2. Perform the operation
3. Export HAR
4. Programmatically parse the HAR file

### 2. Bookmarklet + Vision API

Clicking a bookmark on any webpage image can invoke AI to describe the image contents: GUI injection that "hijacks the interface."

### 3. Playwright / Claude Computer Use

Use VM screenshots + pixel operations to implement GUI automation. This applies when no API exists at all.

### Breakpoints in the Human-AI Loop

When a human has to take and paste screenshots manually, the automation chain is broken. Solutions:

- Let AI take screenshots itself (Playwright)
- Use screenshot utilities for automatic capture
