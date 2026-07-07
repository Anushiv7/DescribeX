# DescribeX

<div align="center">

### Open-source AI-powered multi-style video captioning platform for creators.

Built for **AMD Developer Hackathon: ACT II** (Track 2 – Video Captioning)

Making caption generation accessible, portable, and creator-first.

</div>

---

## ✨ Overview

DescribeX is an open-source AI-powered video captioning platform designed to help creators generate high-quality captions for short-form videos in multiple expressive styles.

Whether you're publishing on YouTube, Instagram, LinkedIn, or any other platform, DescribeX enables you to generate, edit, and export captions without being locked into a single ecosystem.

Built for the **AMD Developer Hackathon: ACT II**, DescribeX is designed to outlive the competition as a long-term open-source project focused on accessibility and creator ownership.

---

## 🏗 Project Architecture

DescribeX consists of two primary components.

### 🌐 DescribeX Web

A modern web application where creators can:

- Upload videos
- Generate captions
- Edit captions
- Export captions
- Manage previous caption jobs

### 🧠 DescribeX Engine

A reusable Python-based caption generation engine responsible for:

- Video preprocessing
- Frame extraction
- AI inference
- Caption generation
- Caption formatting

The same engine powers both the web application and the AMD Hackathon Docker submission.

---

## ✨ Features

### Caption Generation

- Multi-style AI caption generation
- Formal captions
- Sarcastic captions
- Humorous (Tech)
- Humorous (Non-Tech)

### Editing

- Inline caption editing
- Human-in-the-loop workflow

### Export

- Export as SRT
- Export as VTT
- Export as TXT
- Burn captions into video
- Copy to clipboard
- Upload directly to Google Drive

### User Experience

- Google Authentication
- Caption history
- Dark / Light mode
- Creator-first interface

---

## 🛠 Tech Stack

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui

### Backend

- Python

### AI

- Fireworks AI
- Gemma

### Database

- Supabase PostgreSQL

### Authentication

- Supabase Auth
- Google OAuth

---

## 📂 Repository Structure

```text
DescribeX/

├── apps/
│   └── web/
│
├── engine/
│   ├── core/
│   ├── preprocessing/
│   ├── prompting/
│   ├── formatting/
│   ├── models/
│   ├── utils/
│   └── tests/
│
├── docker/
├── docs/
├── components/
├── hooks/
├── lib/
├── public/
├── styles/
├── supabase/
└── types/
```

---

## 🎯 Product Principles

DescribeX is built around five core principles.

- Accessibility First
- Creator Ownership
- Open Source Forever
- Simplicity Over Complexity
- AI Assists, Humans Decide

---

## 🚧 Development Status

**Current Phase**

Documentation & System Design

### Next Milestones

- Software Architecture
- Engine Development
- Web Application
- Docker Submission
- Deployment

---

## 📖 Documentation

Project documentation is available inside the `docs/` directory.

- Product Requirements Document
- Software Architecture
- Project Scaffolding
- API Documentation
- Hackathon Compliance

---

## 🌍 Vision

DescribeX exists to make professional-quality caption generation free, accessible, and portable for creators everywhere.

Accessibility should never become a premium feature.

---

## 🤝 Contributing

DescribeX is open source and community contributions are always welcome.

Contribution guidelines will be published as the project progresses.

---

## 📄 License

This project is licensed under the MIT License.