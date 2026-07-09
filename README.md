<div align="center">

<img src="Branding/logo.png" alt="DescribeX Logo" width="180"/>

# DescribeX

### 🎬 Create Once. Caption Everywhere.

**Open-source AI-powered multi-style video captioning platform for creators.**

Built for **AMD Developer Hackathon: ACT II — Track 2 (Video Captioning)**

<br>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-16-000000?style=for-the-badge&logo=next.js)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Fireworks AI](https://img.shields.io/badge/Fireworks-AI-D7263D?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

</div>

---

# 🚨 Note for Hackathon Judges

Thank you for taking the time to review **DescribeX**.

DescribeX was designed as a production-ready, open-source AI video captioning platform and developed as our submission for the **AMD Developer Hackathon: ACT II**.

During the final stages of development we encountered deployment limitations that prevented us from hosting the complete production backend before the submission deadline.

## 🖥️ AMD Developer Cloud

Our intended production deployment target was **AMD Developer Cloud**, allowing DescribeX to run on AMD infrastructure while demonstrating GPU-assisted AI workflows.

Unfortunately, our AMD Developer Cloud resource request was still pending during the submission period, preventing us from deploying the live production instance before the deadline.

---

## ☁️ Temporary Render Deployment

To provide a live demonstration, we temporarily deployed the backend using **Render**.

The backend:

- ✅ Builds successfully
- ✅ Starts successfully
- ✅ Connects to Fireworks AI
- ✅ Initializes the Caption Engine correctly

However, Render's **Free Web Service** provides only **512 MB RAM**.

Video processing exceeds this memory limit, resulting in an **Out Of Memory (OOM)** error during caption generation.

This is a hosting limitation rather than an application limitation.

---

## 💻 Local Execution

The complete project runs successfully in a local development environment.

Verified components include:

- ✅ Frontend
- ✅ Backend API
- ✅ Caption Engine
- ✅ Fireworks AI Integration
- ✅ Docker Container
- ✅ End-to-End Caption Generation

> ## ⭐ **See Local Setup Guide → [Running DescribeX Locally](#-running-describex-locally)**

Thank you for your understanding and for reviewing our project.

---

# 📸 Screenshots

> Store screenshots inside:

```text
Branding/
└── screenshots/
```

## 🏠 Landing Page

![Landing Page](Branding/screenshots/landing.png)

---

## 📤 Upload Workflow

![Upload](Branding/screenshots/upload.png)

---

## 🤖 Caption Generation

![Caption Generation](Branding/screenshots/captions.png)

---

## ✏️ Caption Editing

![Editing](Branding/screenshots/editing.png)

---

## 📥 Export Options

![Export](Branding/screenshots/export.png)

---
# 🚀 Running DescribeX Locally

The project has been verified to work in a local development environment.

## 1️⃣ Clone the repository

```bash
git clone https://github.com/Anushiv7/DescribeX.git

cd DescribeX
```

---

## 2️⃣ Install the Frontend

```bash
cd apps/web

npm install
```

---

## 3️⃣ Install the Caption Engine

Return to the repository root.

Using pip:

```bash
pip install -e .
```

or using **uv** (recommended)

```bash
uv sync
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DESCRIBEX_PROVIDER=fireworks

DESCRIBEX_FIREWORKS_API_KEY=YOUR_API_KEY

DESCRIBEX_VISION_MODEL_ID=accounts/fireworks/models/kimi-k2p6

DESCRIBEX_TEXT_MODEL_ID=accounts/fireworks/models/gpt-oss-120b
```

---

## 5️⃣ Start the Backend

```bash
uvicorn engine.api:app --host 127.0.0.1 --port 8000 --reload
```

The API documentation will be available at

```
http://127.0.0.1:8000/docs
```

---

## 6️⃣ Start the Frontend

Open another terminal.

```bash
cd apps/web

npm run dev
```

The application will be available at

```
http://localhost:3000
```

---

# 🐳 Docker

DescribeX is fully containerized for the AMD Developer Hackathon submission.

The same Docker image powers the standalone caption engine and can be executed independently from the web application.

---

## Build the Docker Image

```bash
docker build -f docker/Dockerfile -t describex .
```

---

## Run the Container

```bash
docker run --rm \
--env-file .env \
-v <input_directory>:/input \
-v <output_directory>:/output \
describex
```

---

## Expected Input

The Docker container expects a folder mounted at

```
/input
```

containing

```
tasks.json
```

Example

```json
[
  {
    "id": "task_1",
    "video": "example.mp4"
  }
]
```

---

## Expected Output

The generated captions are written to

```
/output/results.json
```

Example

```json
[
  {
    "id": "task_1",
    "captions": {
      "formal": "...",
      "sarcastic": "...",
      "humorous_tech": "...",
      "humorous_non_tech": "..."
    }
  }
]
```

This execution model follows the AMD Developer Hackathon container requirements.

---

# 🌐 Deployment

DescribeX follows a split deployment architecture.

| Component | Platform |
|-----------|----------|
| Frontend | Vercel |
| Backend | Render *(temporary)* |
| Planned Production | AMD Developer Cloud |

---

## Deployment Notes

Frontend deployment is handled through **Vercel**.

The backend was temporarily deployed on **Render** for demonstration purposes.

Production deployment was intended for **AMD Developer Cloud**, which offers significantly better infrastructure for AI-powered video processing workloads.

---

# 🏗️ Architecture

<p align="center">
</p>

DescribeX consists of two independent but tightly integrated components.

## 🌐 DescribeX Web

A modern **Next.js** application focused on user experience.

Responsibilities:

- Upload videos
- Manage caption jobs
- Display AI responses
- Caption editing
- Export workflow
- Responsive UI

---

## 🧠 DescribeX Engine

A reusable Python caption engine powering both the web application and the hackathon Docker submission.

Responsibilities:

- Video preprocessing
- Frame extraction
- Prompt engineering
- Vision model inference
- Caption generation
- Caption formatting
- Output serialization

Because the engine is separated from the frontend, it can easily be integrated into future desktop applications, APIs, or batch-processing pipelines.

---

# ✨ Features

## 🎥 AI Caption Generation

Generate expressive captions in multiple writing styles.

- Formal
- Sarcastic
- Humorous (Tech)
- Humorous (Non-Tech)

Powered by state-of-the-art multimodal AI models.

---

## ✍️ Human-in-the-Loop Editing

Generated captions can be reviewed and refined before export.

This ensures AI assists creators rather than replacing creative control.

---
## 🎨 Modern User Experience

DescribeX focuses on simplicity and accessibility.

Features include:

- Clean Apple-inspired UI
- Responsive layouts
- Fast upload workflow
- Premium visual design
- Creator-first experience

---
## 📤 Export

Current export capabilities include:

- Copy generated captions
- Download generated caption text

Planned export formats include:

- SRT
- VTT
- TXT
- Burn captions into video
- Cloud storage integrations

---

## 🧩 Modular Caption Engine

The caption engine is completely separated from the frontend, allowing it to be reused as:

- Web API
- Docker container
- Standalone Python package
- Future desktop application
---

# 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | Next.js 16 |
| UI | React 19 |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Backend | Python |
| AI Provider | Fireworks AI |
| Containerization | Docker |

---
# 📂 Repository Structure

```text
DescribeX
│
├── apps/
│   └── web/                         # Next.js frontend
│       ├── src/
│       ├── public/
│       ├── package.json
│       └── next.config.ts
│
├── engine/                          # AI Caption Engine
│   ├── api.py
│   ├── core/
│   ├── formatting/
│   ├── preprocessing/
│   ├── prompting/
│   ├── providers/
│   ├── tests/
│   └── utils/
│
├── docker/                          # Docker configuration
│   ├── Dockerfile
│   ├── Dockerfile.render
│   ├── entrypoint.py
│   └── requirements.txt
│
├── Branding/
│   ├── logo.png
│   ├── architecture.png
│   └── screenshots/
│
├── docs/                            # Documentation
├── samples/                         # Sample videos
├── supabase/
├── tests/
│
├── pyproject.toml
├── README.md
├── .dockerignore
└── .gitignore
```
---

# 🔐 Environment Variables

The following variables are required.

| Variable | Description |
|-----------|-------------|
| `DESCRIBEX_PROVIDER` | AI Provider |
| `DESCRIBEX_FIREWORKS_API_KEY` | Fireworks API Key |
| `DESCRIBEX_VISION_MODEL_ID` | Vision Model |
| `DESCRIBEX_TEXT_MODEL_ID` | Text Model |

---

# 📖 Documentation

Additional project documentation is available inside the **docs/** directory.

Included documentation includes:

- Product Requirements Document (PRD)
- Software Architecture
- Project Scaffolding
- Development Planning
- API Documentation
- Hackathon Notes

---
# 🎯 Guiding Principles

DescribeX was designed around a few simple principles that influenced every architectural and product decision.

## ♿ Accessibility First

Captions should improve accessibility for everyone.

Professional caption generation should not be locked behind expensive software or subscriptions.

---

## 🎨 Creator Ownership

Creators should own their captions.

DescribeX avoids vendor lock-in by supporting standard export formats and an open architecture.

---

## 🌍 Open Source Forever

DescribeX is built as an open-source project that anyone can study, improve, and extend.

---

## ✨ Simplicity Over Complexity

Good software should feel effortless.

Every interface is designed to minimize friction while keeping advanced functionality accessible.

---

## 🤖 AI Assists, Humans Decide

Artificial Intelligence should amplify creativity—not replace it.

Generated captions remain fully editable, keeping creators in complete control.

---

# 🚧 Project Status

## Current Progress

| Component | Status |
|-----------|:------:|
| Frontend UI | ✅ |
| Backend API | ✅ |
| Caption Engine | ✅ |
| Docker Container | ✅ |
| Fireworks AI Integration | ✅ |
| Local End-to-End Execution | ✅ |
| Multi-style Caption Generation | ✅ |
| Production Deployment | 🚧 |
| AMD Developer Cloud Deployment | ⏳ |

---

# 🛣 Roadmap

DescribeX is intended to continue beyond the AMD Developer Hackathon.

## ✅ Phase 1 — Foundation

- Project architecture
- Caption engine
- Configuration system
- Logging
- Exception handling
- Docker support
- Frontend prototype
- Fireworks AI integration

**Status:** Complete

---

## 🚧 Phase 2 — Intelligent Captioning

- Multi-style prompting
- Vision understanding
- Caption refinement
- Human editing workflow
- Improved exports
- Performance optimisation

**Status:** In Progress

---

## ⏳ Phase 3 — Creator Platform

Planned improvements include:

- User authentication
- Caption history
- Cloud storage
- Team workspaces
- Shareable projects
- AI prompt customization
- Custom caption styles
- Multi-language caption generation
- Batch video processing

---

## 🔮 Future Vision

Long-term goals include:

- Desktop application
- Mobile companion app
- Plugin ecosystem
- API for developers
- Local LLM support
- AMD GPU acceleration
- Offline inference
- Enterprise deployment options

---

# 🌍 Vision

DescribeX was never intended to be "just another hackathon project."

Our goal is to build an open platform that makes professional-quality caption generation accessible to every creator, regardless of budget or technical background.

As AI tools become increasingly central to content creation, we believe creators should retain ownership, flexibility, and transparency—not become locked into closed ecosystems.

DescribeX represents our first step toward that vision.

---

# 🤝 Contributing

Contributions are always welcome.

Whether it's:

- Bug fixes
- Documentation improvements
- Performance optimisations
- New export formats
- UI enhancements
- New caption styles

...every contribution helps improve DescribeX.

If you'd like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

We appreciate every contribution, no matter how small.

---

# 📄 License

This project is licensed under the **MIT License**.

You're free to use, modify, and distribute the project in accordance with the license terms.

See the `LICENSE` file for details.

---

# 🙏 Acknowledgements

Special thanks to:

- **AMD Developer Hackathon** for the opportunity and challenge.
- **Fireworks AI** for providing high-performance inference APIs.
- The open-source community whose tools and libraries made this project possible.

---

<div align="center">

## ⭐ If you found DescribeX interesting, consider giving the repository a star!

### Built with ❤️ for the AMD Developer Hackathon: ACT II

*"Create Once. Caption Everywhere."*

</div>
