<div align="center">

<img src="Branding/logo.png" alt="DescribeX Logo" width="180"/>

# DescribeX

### 🎬 Create Once. Caption Everywhere.

**Open-source AI-powered multi-style video captioning platform for creators.**

Built for **AMD Developer Hackathon: ACT II — Track 2 (Video Captioning)**

<p align="center">

<img src="Branding/Screenshots/landing.png" width="900"/>

</p>

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
### Built for AMD Developer Hackathon: ACT II — Track 2

DescribeX reads `/input/tasks.json`, processes each video, generates captions in the requested styles, and writes the results to `/output/results.json` using a Dockerized AI caption engine.

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
# 🏆 AMD Developer Hackathon Compliance

DescribeX was built for **AMD Developer Hackathon: ACT II – Track 2 (Video Captioning Agent)**.

The submission fully complies with the required container interface.

### Docker container

- ✅ Reads `/input/tasks.json`
- ✅ Downloads videos from `video_url`
- ✅ Generates captions in all requested styles
- ✅ Writes `/output/results.json`
- ✅ Handles multiple tasks
- ✅ Returns valid JSON
- ✅ Exits with the required status codes

The same Caption Engine powers both the Docker submission and the DescribeX web application.
---


# 🏗️ Architecture

<p align="center">
</p>

DescribeX consists of two independent but tightly integrated components.
tasks.json
      │
      ▼
Local Video
      │
      ├──────────────┐
      ▼              │
Frame Extraction     │
                     │
video_url
      │
      ▼
Download
      │
      ▼
Frame Extraction

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
The DescribeX Caption Engine is the single source of truth for the project.

It powers:

- the AMD Hackathon Docker submission
- the FastAPI backend
- the DescribeX web application

This guarantees identical caption generation behaviour across every execution environment.
---

# 📸 Screenshots



## 🏠 Landing Page

![Landing Page](Branding/Screenshots/landing.png)

---

## 📤 Upload Workflow

![Upload](Branding/Screenshots/upload.png)

---

## 🤖 Caption Generation

![Caption Generation](Branding/Screenshots/captions.png)

---

## ✏️ Caption Editing

![Editing](Branding/Screenshots/editing.png)

---

## 📥 Export Options

![Export](Branding/Screenshots/export.png)

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
## Quick Docker Test

```bash
docker build -f docker/Dockerfile -t describex .

docker run --rm \
--env-file .env \
-v <input>:/input \
-v <output>:/output \
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
    "task_id": "task_1",
    "video": "example.mp4",
    "video_url": "https://example.com/video.mp4",
    "styles": ["formal", "sarcastic", "humorous_tech", "humorous_non_tech"]
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
    "task_id": "task_1",
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

| Component | Platform |
|-----------|----------|
| Frontend | Vercel |
| Backend | Render (Temporary) |
| Planned Production | AMD Developer Cloud |

### Required Environment Variables

| Variable | Description |
|-----------|-------------|
| DESCRIBEX_PROVIDER | AI Provider |
| DESCRIBEX_FIREWORKS_API_KEY | Fireworks API Key |
| DESCRIBEX_VISION_MODEL_ID | Vision Model |
| DESCRIBEX_TEXT_MODEL_ID | Text Model |

---

## Deployment Notes

Frontend deployment is handled through **Vercel**.

The backend was temporarily deployed on **Render** for demonstration purposes.

Production deployment was intended for **AMD Developer Cloud**, which offers significantly better infrastructure for AI-powered video processing workloads.

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

Current export capabilities

- Copy generated captions
- Download generated caption text

Planned capabilities

- SRT
- VTT
- Burned-in video captions
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
## Documentation

Detailed documentation is available inside:

docs/

- PRD
- Software Architecture
- API Documentation
- Development Notes

---


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

# 🚧 Development Status

Status: ✅ Official Track 2 submission — Docker validated against the public sample clips.

## Completed

- Frontend
- Caption Engine
- Docker
- Fireworks AI Integration
- Local Execution

## Known Deployment Limitation

- Render Free Tier
- AMD Cloud access pending

## Future Plans

- Authentication
- Caption history
- Cloud storage
- Batch processing
- Multi-language support
- Offline inference

DescribeX is intended to continue beyond the AMD Developer Hackathon as an open-source creator platform focused on accessibility, portability, and creator ownership.
---

# 🤝 Contributing

Contributions of all kinds are welcome.

If you'd like to improve DescribeX:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.
---

# 📄 License

This project is licensed under the **MIT License**.

You're free to use, modify, and distribute the project in accordance with the license terms.

See the `LICENSE` file for details.

---

<div align="center">

## ⭐ If you found DescribeX interesting, consider giving the repository a star!

### Built with ❤️ for the AMD Developer Hackathon: ACT II

*"Create Once. Caption Everywhere."*

</div>
