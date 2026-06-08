<div align="center">

# 👁️ ForensiX AI
**Enterprise Digital Media Forensics & Deepfake Detection Platform**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-red.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PyTorch](https://img.shields.io/badge/AI-PyTorch-orange.svg?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*Unifying mathematical forensics, cryptographic chain-of-custody tracking, and deep learning into a single analytical Security Operations Center (SOC).*

---

![ForensiX AI Dashboard](https://via.placeholder.com/1000x500/0b0f19/3b82f6?text=+[Upload+a+Screenshot+of+your+Dashboard+Here]+)

</div>

## 📖 Overview

**ForensiX AI** is a multi-modal, enterprise-grade platform designed to detect AI-generated content, deepfakes, and manipulated media. Built for cybersecurity analysts, journalists, and digital investigators, the platform automatically deconstructs images, video, and audio to uncover hidden synthetic artifacts that the human eye cannot see.

## 🚀 Core Capabilities

* 📂 **Multi-Modal Batch Ingestion:** Process massive queues of Images, Videos, and Audio files simultaneously without crashing system memory.
* 🧠 **Deep Neural Detection:** Integrates HuggingFace Vision Transformers (ViT) and Audio Classification pipelines for live AI-synthesis detection.
* 🔐 **Cryptographic Chain of Custody:** Automatically generates and tracks MD5, SHA1, and SHA256 hashes for court-admissible evidence integrity.
* 🗺️ **Structural Heatmaps:** Generates visual Error Level Analysis (ELA) arrays for image manipulation and Mel-Spectrograms for audio anomaly detection.
* 🎞️ **Temporal Video Analysis:** OpenCV-powered frame-by-frame extraction targeting temporal deepfake artifacts.
* 🌍 **Global Threat Intelligence:** Live API integration with VirusTotal to cross-reference file hashes against 70+ global cybersecurity vendors.
* 📄 **Automated Reporting:** Dynamically generates immutable, court-ready PDF forensic reports via `reportlab`.

## 🛠️ Technology Stack

| Category | Technologies |
| :--- | :--- |
| **Backend & Core** | Python 3.11, Flask, SQLite/PostgreSQL |
| **AI & Machine Learning** | PyTorch, HuggingFace Transformers, OpenCV, Scikit-Learn, Librosa |
| **Frontend UI/UX** | Bootstrap 5, Asynchronous JavaScript, Jinja2 (Dark SOC-Theme) |
| **Forensic Utilities** | ReportLab (PDF Generation), Hashlib (Cryptography), Requests (Threat API) |

## ⚙️ Installation & Deployment

It is highly recommended to run ForensiX AI inside an isolated virtual environment to prevent dependency conflicts.

**1. Clone the repository:**
```bash
git clone [https://github.com/Jatin-pardeshi/ForensiX_AI.git](https://github.com/Jatin-pardeshi/ForensiX_AI.git)
cd ForensiX_AI