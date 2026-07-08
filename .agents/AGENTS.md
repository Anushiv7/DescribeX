# DescribeX — Agent Rules (Source of Truth)

> Derived from `docs/PRD.md`, `docs/ARCHITECTURE.md`, and `docs/SCAFFOLDING.md`.
> These rules govern ALL work on this repository.

---

## 1. What Is DescribeX

DescribeX is an **open-source, AI-powered multi-style video captioning platform** built for the **AMD Developer Hackathon: ACT II (Track 2 – Video Captioning)**.

It lets creators upload short-form videos (≤ 2 minutes), generate captions in multiple expressive styles, edit them, and export to formats compatible with major content platforms.

---

## 2. Core Beliefs

- Accessibility should never be a premium feature.
- Creators own and export their captions freely.
- AI accelerates creativity; humans make final decisions.
- The project is and will remain open source.

---

## 3. The Golden Rule

> **The Engine Wins.**

The **caption engine** (`engine/`) is the primary product. The web app is a *client* of the engine. When time or priorities conflict, the engine takes precedence.

---

## 4. Repository Structure (Stable — Do NOT Rename)

```
DescribeX/
├── apps/web/          # Next.js creator-facing web app
├── components/        # Shared React components
├── docker/            # AMD Hackathon Docker submission files
├── docs/              # PRD, Architecture, Scaffolding docs
├── engine/            # ⭐ Core caption generation engine (Python)
│   ├── core/          # Pipeline orchestration
│   ├── formatting/    # JSON formatting, output normalization
│   ├── models/        # AI provider integrations (Fireworks/Gemma)
│   ├── preprocessing/ # Video validation, frame extraction, sampling
│   ├── prompting/     # Prompt templates & construction
│   ├── tests/         # Unit & integration tests
│   └── utils/         # Shared helpers, config, logging
├── hooks/             # React hooks
├── lib/               # Shared library code
├── public/            # Static assets
├── styles/            # CSS / styling
├── supabase/          # Supabase config & migrations
└── types/             # Shared TypeScript types
```

---

## 5. Technology Stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Frontend       | Next.js, TypeScript, Tailwind CSS, shadcn/ui |
| Backend/Engine | Python, FastAPI                     |
| Database       | Supabase PostgreSQL                 |
| Auth           | Supabase Auth + Google OAuth        |
| Storage        | Supabase Storage                    |
| AI             | Fireworks AI + Gemma models         |
| Deployment     | Vercel (prod), Local (dev), AMD Cloud (hackathon) |

---

## 6. Caption Engine Pipeline

The engine processes videos through seven sequential stages:

1. **Video Validation** — format, duration, readability, corruption checks.
2. **Frame Extraction** — FFmpeg decodes video into frames.
3. **Smart Frame Sampling** — selects ≤ ~60 representative frames.
4. **Canonical Prompt Construction** — builds a multimodal prompt from sampled frames.
5. **Canonical Scene Description** — Fireworks AI (Gemma Vision) produces a neutral factual understanding (subjects, environment, actions, mood). Internal only.
6. **Multi-style Caption Generation** — a single Fireworks AI (Gemma) call generates all requested styles from the scene description.
7. **Caption Formatting** — output validation, JSON formatting, whitespace cleanup.

### Caption Styles (MVP)

- Formal
- Sarcastic
- Humorous (Tech)
- Humorous (Non-Tech)

### Output Format

```json
{
    "formal": "...",
    "sarcastic": "...",
    "humorous_tech": "...",
    "humorous_non_tech": "..."
}
```

---

## 7. Architecture Rules

### Engine Independence
- The engine SHALL remain independent of the web application.
- Business logic MUST NOT exist inside Next.js pages, React components, FastAPI routes, or the Docker wrapper.
- The engine contains ALL AI-related logic.

### AI Provider Isolation
- Provider-specific code stays inside `engine/models/`.
- Provider layer handles: auth, request construction, API communication, response parsing, error handling, retries.
- Prompt generation is OUTSIDE the provider layer.
- Future providers (Gemini, OpenAI, Anthropic, local inference) must integrate without changing the core pipeline.

### Prompt Separation
- Prompt templates stay in `engine/prompting/`.
- Prompt strings MUST NOT be hardcoded in provider implementations.
- Prompts evolve independently from application code.

### Docker Submission
- Docker container is a **thin wrapper** around the engine.
- Reads `/input/tasks.json` → invokes engine → writes `/output/results.json` → exits.
- Caption generation logic MUST NOT be duplicated in Docker.

### Configuration
- Runtime config is centralized (max duration, max frames, model, temperature, logging level, output format).
- No hardcoded values scattered through the codebase.

---

## 8. Web Application Features

### Functional Requirements (Priority: High unless noted)

| ID      | Feature              | Key Details |
|---------|----------------------|-------------|
| FR-001  | Authentication       | Google OAuth via Supabase; required before upload; privacy policy acceptance |
| FR-002  | Video Upload         | MP4 initially; progress indicator; validation errors |
| FR-003  | Style Selection      | Multiple styles selectable; ≥ 1 required |
| FR-004  | Caption Generation   | Progress visible; failures produce friendly messages; results editable |
| FR-005  | Caption Editing      | Inline editing; auto-save during session; original recoverable until export |
| FR-006  | Export               | SRT, VTT, TXT, burned-in video, clipboard, Google Drive |
| FR-007  | History (Medium)     | Stores metadata (title, date, styles, text, thumbnail, export history); original video deleted after processing |
| FR-008  | Settings (Low)       | Theme, connected account, delete history |

### Pages

- **Landing Page** — hero, demo video, features, GitHub link, open-source notice.
- **Dashboard** — upload card, recent jobs, storage usage, settings shortcut.
- **Caption Editor** — editable captions, copy, export, preview.
- **History** — search, filter, delete, re-export.

---

## 9. Non-Functional Requirements

- **Performance**: Immediate upload feedback; responsive exports.
- **Reliability**: Graceful recovery from failed uploads, AI failures, network issues.
- **Maintainability**: Modular codebase; business logic independent of UI.
- **Scalability**: Support future styles, providers, desktop/mobile apps, batch processing.
- **Accessibility**: Keyboard nav, screen readers, high-contrast themes, responsive layouts.

---

## 10. MVP Boundary

### ✅ In Scope (MVP)

- Frame extraction & smart sampling
- Canonical scene description
- Multi-style caption generation
- FastAPI wrapper
- Docker compatibility

### ❌ Out of Scope (Deferred)

- Video editing beyond captions / timeline editing
- Audio enhancement
- Full video production suite
- Team collaboration / workspaces
- Live streaming
- Long-form (> 2 min) video support
- Auto-publishing to social media
- Authentication (engine MVP)
- Analytics / payments
- Mobile / desktop apps
- Batch processing / plugin systems

---

## 11. Engineering Principles

1. **The Engine Wins** — caption engine is the primary product.
2. **Ship Over Perfect** — complete working implementation > unfinished perfect architecture.
3. **Readability Over Cleverness** — code understandable within minutes.
4. **Every Dependency Needs a Reason** — no unnecessary libraries.
5. **Simplicity First** — choose the simplest valid implementation.

---

## 12. Coding Standards

- Every module has a single responsibility.
- Prefer descriptive function names.
- Keep functions focused and reasonably small.
- Avoid unnecessary nesting.
- Document non-obvious decisions with comments.
- Preserve all existing comments and docstrings unrelated to changes.

---

## 13. Before Implementing Any Feature — Checklist

- [ ] Read `docs/ARCHITECTURE.md`.
- [ ] Preserve existing module boundaries.
- [ ] Reuse existing code whenever possible.
- [ ] Avoid unnecessary refactoring.
- [ ] Do not introduce new dependencies without justification.
- [ ] Respect the MVP Boundary (Section 10).
- [ ] Ask: Does it improve caption quality, maintainability, or hackathon compliance? If not, defer.

---

## 14. Security & Privacy

- Only authenticated users may upload.
- Uploaded videos are temporary and deleted after processing.
- Caption metadata is associated with the user.
- No unnecessary personal information collected.

---

## 15. Decision Framework

Before adding any feature, ask:

> Does it improve **caption quality**, **maintainability**, or **hackathon compliance**?

If **no** → defer to roadmap.

---

## 16. Source Documents

- [PRD.md](file:///c:/Users/Yello/Downloads/DescribeX/docs/PRD.md)
- [ARCHITECTURE.md](file:///c:/Users/Yello/Downloads/DescribeX/docs/ARCHITECTURE.md)
- [SCAFFOLDING.md](file:///c:/Users/Yello/Downloads/DescribeX/docs/SCAFFOLDING.md)
