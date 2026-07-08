# Software Architecture

# DescribeX

> Built for AMD Developer Hackathon: ACT II (Track 2 – Video Captioning)
>
> Version: 1.0.0
>
> Status: Architecture Design
>
> Author:
> - Anushiv Prakash

---

# Table of Contents

1. Overview
2. Architecture Principles
3. High-Level Architecture
4. Repository Structure
5. Core Components
6. Processing Pipeline
7. AI Provider Layer
8. Module Responsibilities
9. API Design
10. Docker Submission Architecture
11. Configuration
12. Logging
13. Future Extensibility
14. Architecture Decision Records
15. Appendix

---

# 1. Overview

DescribeX is designed around a simple principle:

> **Build the captioning engine first. Build everything else around it.**

Instead of tightly coupling AI logic with a web application, DescribeX separates the reusable caption generation engine from the interfaces that consume it.

This allows the same engine to power:

- The AMD Developer Hackathon Docker submission
- The DescribeX web application
- Future APIs
- Future SDKs
- Future desktop or mobile applications

The web application is therefore treated as a client of the engine rather than the core product itself.

---

# 2. Architecture Principles

The DescribeX architecture is guided by the following principles.

---

## Simplicity First

The primary objective is to build a robust Minimum Viable Product (MVP) suitable for the AMD Developer Hackathon.

Features that do not directly improve caption quality, maintainability, or hackathon compliance are intentionally deferred.

---

## Modular Design

Every component should have one clearly defined responsibility.

Instead of one large caption generation script, the engine is composed of independent modules responsible for validation, preprocessing, prompting, inference, formatting, and exporting.

---

## Reusability

The caption generation engine should remain independent of any specific user interface.

This enables multiple frontends to reuse the same implementation without duplicating business logic.

---

## Hackathon Compliance

The architecture is designed around the official AMD Developer Hackathon Track 2 specification.

This includes support for:

- Docker execution
- Fireworks AI
- Gemma models
- JSON-based outputs
- Short-form video processing

---

## Future Extensibility

While the MVP focuses on the hackathon requirements, the architecture intentionally leaves room for future growth.

Examples include:

- Additional AI providers
- More caption styles
- Desktop applications
- Mobile applications
- Batch processing

These capabilities should require minimal architectural changes.

---

# 3. High-Level Architecture

DescribeX consists of a reusable caption generation engine surrounded by lightweight clients.

```text
                         DescribeX

                  ┌─────────────────────┐
                  │   Caption Engine    │
                  └──────────┬──────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
 AMD Docker Agent      FastAPI Service     Future SDK/API
          │                  │
          │                  ▼
          │           DescribeX Web
          │          (Next.js Client)
          │
          ▼
 AMD Developer
 Hackathon Submission
```

The caption engine contains all AI-related logic.

External applications communicate with the engine through clearly defined interfaces rather than implementing caption generation independently.

---

# 4. Repository Structure

The current repository structure reflects a separation between reusable engine logic and application-specific components.

```text
DescribeX/

├── apps/
│   └── web/
│
├── components/
├── docker/
├── docs/
│
├── engine/
│   ├── core/
│   ├── formatting/
│   ├── models/
│   ├── preprocessing/
│   ├── prompting/
│   ├── tests/
│   └── utils/
│
├── hooks/
├── lib/
├── public/
├── styles/
├── supabase/
└── types/
```

The `engine/` directory represents the core of DescribeX and is intentionally isolated from frontend implementation details.

The `apps/web/` directory contains the future creator-facing interface.

The `docker/` directory contains files required for AMD Hackathon submission.

---

# 5. Core Components

DescribeX is divided into several logical components.

---

## Caption Engine

The Caption Engine is responsible for the complete caption generation pipeline.

Responsibilities include:

- Video validation
- Frame extraction
- Smart frame sampling
- Prompt construction
- AI inference
- Caption formatting
- JSON generation

The engine does not contain any UI-specific code.

---

## Web Application

The web application provides an intuitive interface for creators.

Responsibilities include:

- Authentication
- Video upload
- Displaying generated captions
- Editing captions
- Export options

The web application never performs AI inference directly.

Instead, it communicates with the Caption Engine through API endpoints.

---

## Docker Agent

The Docker Agent is a lightweight wrapper around the Caption Engine.

Its responsibilities are limited to:

- Reading `/input/tasks.json`
- Invoking the Caption Engine
- Writing `/output/results.json`
- Returning the appropriate exit code

No caption generation logic should exist inside the Docker layer.

---

## AI Layer

The AI Layer provides a standardized interface between DescribeX and external model providers.

For the MVP implementation, this consists of:

- Fireworks AI
- Gemma models

Future providers may include:

- Google Gemini
- OpenAI
- Anthropic
- Local inference backends

The rest of the engine remains unaware of which provider is being used.

---

## Prompt Layer

Prompt engineering is intentionally separated from application logic.

Prompt templates are stored independently from Python source code to enable rapid experimentation without modifying engine implementation.

This approach significantly improves maintainability during the hackathon iteration process.

---

## Formatting Layer

After inference, captions are standardized into a common internal representation before export.

This layer is responsible for:

- Caption cleanup
- Style formatting
- JSON serialization
- Export preparation

Separating formatting from inference keeps AI outputs independent from downstream consumers.

---

# End of Part 1
# 6. Caption Processing Pipeline

The DescribeX caption generation pipeline follows a staged architecture in which each module performs a single responsibility.

Instead of relying on one large inference step, the pipeline separates preprocessing, understanding, generation, and formatting into independent stages.

This design improves maintainability, reduces token consumption, and enables future extensions without major architectural changes.

The complete processing flow is shown below.

```text
Video
    │
    ▼
Video Validation
    │
    ▼
Frame Extraction (FFmpeg)
    │
    ▼
Smart Frame Sampling
    │
    ▼
Canonical Prompt Construction
    │
    ▼
Fireworks AI (Gemma Vision)
    │
    ▼
Canonical Scene Description
    │
    ▼
Style Generation Prompt
    │
    ▼
Fireworks AI (Gemma)
    │
    ▼
Multi-style JSON Response
    │
    ▼
Caption Formatter
    │
    ▼
API / Docker / Web
```

---

## Stage 1 — Video Validation

Before any processing begins, the engine validates the incoming video.

Validation includes:

- Supported format
- Video duration
- File readability
- Corrupted media detection

Invalid videos terminate the pipeline early with meaningful error messages.

---

## Stage 2 — Frame Extraction

DescribeX uses **FFmpeg** as the primary frame extraction backend.

Reasons for choosing FFmpeg include:

- Industry-standard tooling
- Excellent performance
- Accurate timestamp handling
- Docker compatibility
- Lightweight integration with Python

The extraction module is responsible only for decoding the video into individual frames.

No AI processing occurs during this stage.

---

## Stage 3 — Smart Frame Sampling

Extracting every frame from a video is computationally expensive and unnecessary.

Instead, DescribeX selects a representative subset of frames.

The sampling strategy is designed to:

- Reduce redundant visual information
- Preserve scene diversity
- Respect model frame limits
- Reduce inference cost

The current architecture targets a maximum budget of approximately sixty representative frames.

This value remains configurable through the engine configuration.

---

## Stage 4 — Canonical Prompt Construction

Representative frames are transformed into a single multimodal prompt.

The prompt requests a neutral understanding of the video rather than generating user-facing captions.

Example information extracted includes:

- Primary subjects
- Environment
- Actions
- Context
- Mood
- Visual relationships

This intermediate representation is referred to as the **Canonical Scene Description**.

---

## Stage 5 — Canonical Scene Description

The Canonical Scene Description represents the factual understanding of the video.

It intentionally avoids humor, opinion, or stylistic language.

Example structure:

```yaml
Scene:
    Urban street

Subjects:
    Person
    Bicycle

Actions:
    Riding
    Crossing road

Environment:
    Autumn
    City

Mood:
    Calm
```

This representation exists only internally and is never presented directly to end users.

---

## Stage 6 — Multi-style Caption Generation

Rather than performing multiple expensive video analyses, DescribeX analyzes the video once and generates all requested caption styles from the Canonical Scene Description.

A single prompt requests all required styles simultaneously.

Expected output:

```json
{
    "formal": "...",
    "sarcastic": "...",
    "humorous_tech": "...",
    "humorous_non_tech": "..."
}
```

Advantages include:

- One video understanding step
- One text generation request
- Lower latency
- Lower API cost
- Better stylistic consistency

---

## Stage 7 — Caption Formatting

Generated captions are normalized before being returned.

Responsibilities include:

- Output validation
- JSON formatting
- Whitespace cleanup
- Style verification
- Preparing downstream exports

Formatting remains independent from AI inference.

---

# 7. AI Provider Layer

The AI Provider Layer abstracts communication between DescribeX and external AI services.

This separation ensures the engine remains independent of any individual provider.

Current implementation:

- Fireworks AI
- Gemma models

Future providers may include:

- Google Gemini
- OpenAI
- Anthropic Claude
- Local inference
- Other OpenAI-compatible APIs

Only the provider layer communicates directly with external services.

The remainder of the engine operates independently of provider implementation.

---

## Provider Responsibilities

The provider layer handles:

- Authentication
- Request construction
- API communication
- Response parsing
- Error handling
- Retry strategies

Prompt generation remains outside this layer.

---

# 8. Module Responsibilities

DescribeX follows a modular architecture.

Each module owns exactly one responsibility.

---

## core/

Coordinates the complete processing pipeline.

Responsibilities:

- Pipeline orchestration
- Module coordination
- Error propagation

---

## preprocessing/

Responsibilities:

- Video validation
- Frame extraction
- Smart sampling

---

## prompting/

Responsibilities:

- Prompt templates
- Prompt loading
- Prompt construction

Prompt templates remain external to Python source code to simplify iteration.

---

## models/

(Current implementation)

Responsibilities:

- Fireworks integration
- Provider communication

Future versions may rename this directory to `providers/` as support for additional AI services grows.

---

## formatting/

Responsibilities:

- JSON formatting
- Output normalization
- Caption cleanup

---

## utils/

Shared helper functions.

Examples include:

- File utilities
- Configuration loading
- Logging helpers

---

## tests/

Unit and integration testing.

Every major module should be independently testable.

---

# 9. API Design

The DescribeX engine is exposed through a lightweight FastAPI service.

The API acts only as an interface.

Business logic remains inside the Caption Engine.

Example architecture:

```text
Client

↓

FastAPI

↓

Caption Engine

↓

JSON Response
```

Example endpoint:

```
POST /caption
```

Request:

- Video
- Requested styles

Response:

```json
{
    "formal": "...",
    "sarcastic": "...",
    "humorous_tech": "...",
    "humorous_non_tech": "..."
}
```

Future endpoints may include:

- Health checks
- Version information
- Configuration inspection

---

# 10. Docker Submission Architecture

The Docker submission is intentionally lightweight.

It acts only as a wrapper around the Caption Engine.

Execution flow:

```text
Container Start

↓

Read /input/tasks.json

↓

Download Video

↓

Invoke Caption Engine

↓

Generate JSON

↓

Write /output/results.json

↓

Exit
```

This separation ensures that the Docker implementation never duplicates caption generation logic.

Any improvements made to the Caption Engine automatically benefit both the web application and the hackathon submission.

---

# End of Part 2
# 11. Configuration

DescribeX centralizes runtime configuration to avoid hardcoded values throughout the codebase.

A dedicated configuration module stores parameters controlling inference behavior, preprocessing limits, and runtime settings.

Examples include:

- Maximum video duration
- Maximum frame budget
- Default AI model
- Temperature
- Logging level
- Output format

Example:

```python
MODEL = "accounts/fireworks/models/gemma"

MAX_VIDEO_DURATION = 120

MAX_FRAMES = 60

TEMPERATURE = 0.3

OUTPUT_FORMAT = "json"
```

Centralizing configuration simplifies experimentation during development while improving maintainability.

---

# 12. Logging

DescribeX adopts a lightweight logging strategy focused on debugging and observability during development.

Logging should remain informative without introducing unnecessary complexity.

Typical events include:

```text
INFO  Video received

INFO  Validation complete

INFO  Extracting frames

INFO  Smart sampling complete

INFO  Building canonical prompt

INFO  Sending request to Fireworks

INFO  Canonical description generated

INFO  Generating multi-style captions

INFO  Formatting response

INFO  Pipeline completed successfully
```

Errors should provide meaningful messages while avoiding exposure of sensitive information such as API keys.

---

# 13. Error Handling

Failures are expected and should be handled gracefully.

Potential failure scenarios include:

- Invalid video format
- Corrupted video
- Missing frames
- FFmpeg failure
- Fireworks API timeout
- Invalid model response
- Malformed JSON
- Network interruptions

The engine should fail early whenever recovery is not possible and return structured error messages suitable for debugging.

---

# 14. Future Extensibility

Although DescribeX is currently focused on the AMD Developer Hackathon, the architecture intentionally supports future expansion.

Possible future improvements include:

## AI Providers

- Google Gemini
- OpenAI
- Anthropic Claude
- Local inference (vLLM / Ollama)
- Other OpenAI-compatible APIs

---

## Caption Styles

Future styles may include:

- Marketing
- Educational
- Storytelling
- Gen Z
- Minimal
- Documentary
- Technical Documentation

---

## Export Formats

Future support may include:

- ASS
- WebVTT enhancements
- Subtitle translation
- Social-media-specific caption templates

---

## Applications

Future clients may include:

- Desktop application
- Mobile application
- Browser extension
- Python SDK

---

## Platform Features

Potential future capabilities include:

- User accounts
- Caption history
- Team workspaces
- Batch processing
- Analytics
- Collaborative editing

These features intentionally remain outside the scope of the current MVP.

---

# 15. Architecture Decision Records (ADR)

This section documents the major architectural decisions made during the design of DescribeX.

---

## ADR-001

### Decision

Use a shared Python caption engine.

### Reason

Avoid duplicate business logic between the Docker submission and future web application.

---

## ADR-002

### Decision

Expose the engine through FastAPI.

### Reason

Allow multiple clients to reuse the same implementation without embedding business logic.

---

## ADR-003

### Decision

Use FFmpeg for frame extraction.

### Reason

Industry-standard performance, Docker compatibility, and reliable video decoding.

---

## ADR-004

### Decision

Implement smart frame sampling.

### Reason

Reduce redundant visual information while maximizing scene coverage within the available frame budget.

---

## ADR-005

### Decision

Generate a Canonical Scene Description.

### Reason

Analyze the video once before generating stylistic variants.

This reduces token usage while improving consistency.

---

## ADR-006

### Decision

Generate all caption styles in a single inference request.

### Reason

Reduce API calls, latency, and overall inference cost.

---

## ADR-007

### Decision

Store prompts as standalone template files.

### Reason

Prompt engineering should evolve independently from application logic.

---

## ADR-008

### Decision

Separate provider communication from prompt construction.

### Reason

Maintain provider independence and simplify future integrations.

---

## ADR-009

### Decision

Organize the engine into independent modules.

### Reason

Improve readability, maintainability, testing, and future extensibility.

---

## ADR-010

### Decision

Prioritize the Caption Engine over the web application.

### Reason

The engine represents the reusable core of DescribeX and directly satisfies the AMD Developer Hackathon submission requirements.

---

# 16. Guiding Philosophy

DescribeX follows a simple engineering philosophy.

> Build the smallest system capable of solving the problem well.

Every architectural decision should improve one or more of the following:

- Simplicity
- Maintainability
- Performance
- Reusability
- Hackathon compliance

Features that do not meaningfully contribute to these goals are intentionally deferred.

---

# 17. Conclusion

DescribeX is designed around a modular, reusable caption generation engine that separates preprocessing, prompting, AI inference, formatting, and deployment concerns.

The resulting architecture supports both the AMD Developer Hackathon Docker submission and future creator-facing applications while remaining intentionally lightweight.

Rather than optimizing for feature count, DescribeX prioritizes a clean processing pipeline, thoughtful engineering decisions, and maintainable software design.

The architecture is intentionally minimal, focusing on delivering a robust MVP that can evolve naturally into a larger open-source platform as the project matures.

---

**End of Document**