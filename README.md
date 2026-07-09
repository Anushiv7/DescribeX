<div align="center">

<img src="Branding/logo.png" alt="DescribeX Logo" width="180"/>

# DescribeX

### 🎬 Create Once. Caption Everywhere.

**Open-source AI-powered multi-style video captioning platform for creators.**

Built for **AMD Developer Hackathon: ACT II — Track 2 (Video Captioning)**

<br>

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Next.js](https://img.shields.io/badge/Next.js-16-black)
![React](https://img.shields.io/badge/React-19-61DAFB)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![Fireworks AI](https://img.shields.io/badge/Fireworks-AI-red)
![MIT License](https://img.shields.io/badge/License-MIT-green)

</div>

---

# 🚨 Note for Hackathon Judges

Thank you for taking the time to review **DescribeX**.

During the final stage of development we encountered deployment limitations unrelated to the application itself.

## AMD Developer Cloud

DescribeX was originally intended to be deployed on **AMD Developer Cloud** to showcase GPU-powered inference.

Unfortunately, our AMD Developer Cloud resource request was still pending during the submission period, preventing us from deploying the production instance before the deadline.

---

## Temporary Deployment

As a temporary alternative, the backend was deployed on **Render**.

The application builds successfully and the API starts correctly, however Render's free web service is limited to **512 MB RAM**.

Video processing exceeds this memory limit, resulting in an **Out Of Memory (OOM)** error while processing uploaded videos.

This is a hosting limitation rather than an application limitation.

---

## Local Execution

The application runs successfully in a local environment, including:

- ✅ Caption Engine
- ✅ Fireworks AI integration
- ✅ Docker container
- ✅ Frontend
- ✅ Backend API

### ⭐ **See Local Setup → [Running DescribeX Locally](#-running-describex-locally)**

Thank you for your understanding.

---

# 📸 Screenshots

> Replace these placeholder images with screenshots stored inside:
