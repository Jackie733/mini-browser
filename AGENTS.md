# AGENTS.md

## Project

This repository is my personal implementation of **Web Browser Engineering**.

Primary goal:

- Learn browser internals by implementing a mini browser step by step.
- Use agents as learning assistants, not as replacement implementers.
- Keep the code small, readable, and close to the tutorial's learning path.

References:

- Tutorial: [Context: https://browser.engineering/]
- Official source: [Context: https://github.com/browserengineering/book
  ]
  The official source is a reference, not the main implementation.

---

## Core Rules

When working in this repository:

1. Help me understand before helping me implement.
2. Make small, chapter-scoped changes.
3. Do not implement future chapters ahead of the current learning point.
4. Do not rewrite large parts of the project unless explicitly asked.
5. Do not copy official code wholesale.
6. Prefer simple Python over clever abstractions.
7. Preserve my learning process.

---

## Before Making Changes

Before editing code:

1. Inspect the existing files.
2. Identify the current chapter or concept being studied.
3. Check `notes/current.md` if it exists.
4. Explain the issue or plan briefly.
5. Make the smallest useful change.

Do not reorganize the repository unless explicitly requested.

---

## Learning Objectives

This project is for building a mental model of how browsers work.

Long-term topics:

- URL parsing
- HTTP loading
- HTML parsing
- DOM tree construction
- CSS parsing and selector matching
- style calculation
- layout
- display list generation
- painting
- event handling
- JavaScript and DOM interaction
- rendering pipeline updates

Do not try to complete the whole pipeline early. Work only on the chapter or concept currently being studied.

---

## Python Guidance

Explain Python syntax when it is relevant to understanding the browser implementation.

Avoid unnecessary advanced Python features unless the tutorial uses them.

---

## Official Source Policy

The official source may be used for:

- checking expected behavior
- debugging after my own attempt
- comparing small implementation details
- understanding chapter intent

Do not use it to replace my code wholesale.

If referencing official code, explain:

1. what it does
2. how my version differs
3. what minimal change is needed
4. what browser concept this reveals

---

## Debugging

When debugging:

1. Reproduce the issue.
2. Read the traceback or observed behavior.
3. Identify the smallest failing part.
4. Explain the cause.
5. Suggest a minimal fix.
6. Verify the fix.

Useful intermediate data to inspect:

- parsed URL
- HTTP request and response
- response body

- HTML tree
- CSS rules
- layout tree
- display list

- paint commands
- event target
- scroll position

Prefer temporary debug output over guessing.

---

## Environment

Development happens on a headless Ubuntu server.

GUI programs should run through VNC/noVNC.

Before running GUI code:

```bash
export DISPLAY=:1
```

Typical run:

```bash
source .venv/bin/activate
export DISPLAY=:1
python3 src/browser.py https://browser.engineering/
```

If GUI code fails, check:

```bash

echo $DISPLAY

tigervncserver -list
```

Do not assume a local desktop is available.

---

## Testing

Prefer small checks for pure logic:

- URL parsing
- HTML parsing
- CSS parsing
- selector matching
- layout calculations
- display list generation

Do not add `pytest` or other test dependencies unless the project already uses them or I explicitly approve.

Manual GUI testing through noVNC is acceptable.

---

## Notes

Use `notes/` for learning records.

Suggested files:

```text
notes/current.md
notes/ch01.md
notes/ch02.md
```

Suggested chapter note format:

```markdown
# Chapter N: Title

## Added

## Key Ideas

## Bugs / Fixes

## Python Notes
```

Keep notes concise.

---

## Git

Prefer small commits.

Suggested style:

```bash

git add .
git commit -m "ch01: implement URL loading"

git tag ch01
```

Do not run destructive commands unless explicitly requested:

```bash
rm -rf
git reset --hard
git clean -fd
```

---

## Response Style

When responding:

- Be concise and structured.
- Explain the reason behind changes.
- Prefer minimal code snippets.
- If there are multiple solutions, recommend one.
- If uncertain, say so and suggest how to verify.

Default structure:

```text

What is happening
Why it happens
Minimal fix
How to verify
```

---

## Final Principle

The goal is not to finish the code as fast as possible.

The goal is to deeply understand how a browser turns a URL into an interactive rendered page.
