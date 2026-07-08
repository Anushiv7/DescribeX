# DescribeX Scaffolding Guide

> **Version:** 1.0
>
> **Status:** Active
>
> This document defines the engineering rules for contributors to DescribeX.
>
> Human contributors and AI coding agents (Gemini CLI, Antigravity, Codex, Claude Code, etc.) SHALL follow these guidelines unless explicitly instructed otherwise by the repository owner.

---

# 1. Purpose

DescribeX is an **engine-first** project built for the **AMD Developer Hackathon: ACT II**.

The primary objective is to build a robust, reusable caption generation engine.

The web application exists to demonstrate and consume the engine—not replace it.

Whenever implementation priorities conflict, the engine takes precedence.

---

# 2. Engineering Principles

## Rule 1 — The Engine Wins

The caption engine is the primary product.

If time is limited, prioritize improving the engine over polishing the UI.

---

## Rule 2 — Ship Over Perfect

Prefer a complete, working implementation over an unfinished perfect architecture.

---

## Rule 3 — Readability Over Cleverness

Code should be understandable by another contributor within minutes.

Avoid unnecessary abstraction.

---

## Rule 4 — Every Dependency Needs a Reason

Every external dependency must solve a real problem.

Avoid introducing libraries that duplicate existing functionality.

---

## Rule 5 — Simplicity First

When multiple valid implementations exist, choose the simplest one that satisfies the requirements.

---

# 3. Repository Rules

The repository structure is considered stable.

Contributors SHOULD NOT rename or reorganize top-level directories without explicit approval.

Current structure:

```text
apps/
components/
docker/
docs/
engine/
hooks/
lib/
public/
styles/
supabase/
types/
```

Business logic belongs inside `engine/`.

---

# 4. Engine Rules

The engine SHALL remain independent of the web application.

Business logic MUST NOT exist inside:

- Next.js pages
- React components
- FastAPI routes
- Docker wrapper

The engine is responsible for:

- Video validation
- Frame extraction
- Smart sampling
- Prompt construction
- AI inference
- Caption formatting
- JSON generation

---

# 5. Prompt Rules

Prompt templates SHALL remain inside:

```text
engine/prompting/
```

Prompt strings MUST NOT be hardcoded inside provider implementations.

Prompt engineering should evolve independently from application code.

---

# 6. AI Provider Rules

Provider-specific code SHALL remain isolated.

The MVP implementation uses:

- Fireworks AI
- Gemma

Future providers (Gemini, OpenAI, Anthropic, etc.) should integrate without requiring changes to the core pipeline.

---

# 7. Docker Rules

The Docker container is a thin wrapper around the engine.

Its responsibilities are limited to:

- Reading `tasks.json`
- Calling the engine
- Writing `results.json`

Caption generation logic MUST NOT be duplicated inside Docker.

---

# 8. Coding Standards

Every module should have a single responsibility.

Prefer descriptive function names.

Keep functions focused and reasonably small.

Avoid unnecessary nesting.

Document non-obvious decisions with comments.

---

# 9. MVP Boundary

The following features are considered MVP.

✅ Frame extraction

✅ Smart frame sampling

✅ Canonical scene description

✅ Multi-style caption generation

✅ FastAPI wrapper

✅ Docker compatibility

The following are intentionally deferred.

❌ Authentication

❌ Analytics

❌ Team workspaces

❌ Payments

❌ Mobile applications

❌ Batch processing

❌ Plugin systems

These features belong to future iterations and should not be implemented during the hackathon unless explicitly approved.

---

# 10. AI Contributor Checklist

Before implementing a feature:

- Read `ARCHITECTURE.md`.
- Preserve existing module boundaries.
- Reuse existing code whenever possible.
- Avoid unnecessary refactoring.
- Do not introduce new dependencies without justification.
- Respect the MVP Boundary.

---

# 11. Decision Framework

Before adding a feature, ask:

Does it improve:

- Caption quality?
- Maintainability?
- Hackathon compliance?

If the answer is **no**, defer it to the roadmap.

---

# 12. Final Principle

DescribeX is intentionally an MVP.

The goal is **not** to build the largest project.

The goal is to build the cleanest, most reliable caption generation engine possible within the hackathon timeline.

When in doubt:

> **The Engine Wins.**