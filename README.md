# 📚 Academic Integrity Intelligence Platform (AIIP)

> An AI-powered Academic Integrity Platform built using **IBM Cloud**, **IBM watsonx.ai Foundation Models**, **IBM watsonx Orchestrate**, **React**, and **FastAPI** to intelligently analyze assignment submissions and generate academic integrity reports.

![IBM Cloud](https://img.shields.io/badge/IBM-Cloud-blue)
![watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-blue)
![React](https://img.shields.io/badge/React-Vite-61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Python](https://img.shields.io/badge/Python-3.11-yellow)

---

# 📖 Project Overview

Academic institutions are facing increasing challenges in detecting sophisticated plagiarism, especially with the widespread use of AI-assisted writing tools.

The **Academic Integrity Intelligence Platform (AIIP)** is an AI-powered web application that enables students and faculty to upload assignment PDFs, extract the document text, analyze it using **IBM watsonx.ai Foundation Models**, and generate a comprehensive academic integrity report.

The platform provides:

- Assignment Summary
- Academic Integrity Score
- Possible Plagiarism Observations
- AI-generated Content Analysis
- Citation Suggestions
- Recommendations for Improvement

The project also integrates **IBM watsonx Orchestrate** to provide an intelligent conversational assistant capable of answering questions related to academic integrity and plagiarism policies.

---

# 🚀 Features

- 📄 Upload Assignment PDF
- 📝 Automatic PDF Text Extraction
- 🤖 AI-powered Academic Integrity Analysis
- 📊 Academic Integrity Score (0–100)
- 🔍 Possible Plagiarism Detection
- 🧠 AI-generated Content Analysis
- 📚 Citation Suggestions
- 💡 Personalized Recommendations
- ⚡ FastAPI REST API
- 📄 OpenAPI (Swagger) Documentation
- ☁ IBM watsonx.ai Integration
- 🤝 IBM watsonx Orchestrate Agent

---

# 🏗 System Architecture

```
Student Uploads Assignment PDF
            │
            ▼
      React Frontend
            │
            ▼
      FastAPI Backend
            │
            ▼
   PDF Text Extraction
            │
            ▼
IBM watsonx.ai Foundation Models
            │
            ▼
Academic Integrity Analysis
            │
            ▼
Academic Integrity Report
```

---

# 🛠 Technology Stack

| Layer | Technology |
|--------|------------|
| Frontend | React, Vite, Tailwind CSS |
| Backend | FastAPI, Python |
| AI | IBM watsonx.ai Foundation Models (Meta Llama 3.3 70B Instruct) |
| IBM Services | IBM Cloud, IBM watsonx.ai, IBM watsonx Orchestrate |
| PDF Processing | PyPDF2 |
| Storage | Local File System |

---

# ☁ IBM Technologies Used

- IBM Cloud
- IBM watsonx.ai
- IBM watsonx Orchestrate
- IBM Foundation Models
- IBM Identity & Access Management (IAM)

---

# 📂 Project Structure

```
Academic-Integrity-Intelligence-Platform/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── .env.example
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── dataset/
│
├── uploads/
│
├── reports/
│
├── screenshots/
│   ├── home.png
│   ├── upload.png
│   └── report.png
│
├── AICTE_Project_Presentation.pptx
├── problemstatement.pdf
├── README.md
└── requirements.txt
```

---

# ⚙ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Academic-Integrity-Intelligence-Platform.git

cd Academic-Integrity-Intelligence-Platform
```

---

## 2️⃣ Backend

```bash
cd backend

python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend URLs

```
http://localhost:8000/health

http://localhost:8000/docs

http://localhost:8000/openapi.json
```

---

## 3️⃣ Frontend

Open another terminal

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:5173
```

---

# 🔑 IBM Configuration

Create

```
backend/.env
```

Example

```env
IBM_API_KEY=your_api_key
IBM_PROJECT_ID=your_project_id
IBM_REGION=eu-gb
IBM_GRANITE_MODEL_ID=meta-llama/llama-3-3-70b-instruct
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

> **Note:** Use your own IBM Cloud API Key and watsonx.ai Project ID. Never commit the `.env` file to GitHub.

---

# 🌐 API Endpoints

## Health

```
GET /health
```

---

## Upload Assignment

```
POST /upload
```

Uploads a PDF and extracts the text.

---

## Analyze Assignment

```
POST /analyze
```

Analyzes extracted text using IBM watsonx.ai Foundation Models and returns an Academic Integrity Report.

---

# 📈 Results

The developed system successfully:

- Extracts text from uploaded PDF assignments.
- Generates AI-powered academic integrity reports.
- Produces an Academic Integrity Score.
- Detects possible plagiarism indicators.
- Identifies potential AI-generated writing.
- Suggests citation improvements.
- Provides actionable academic recommendations.

---

# 📸 Screenshots

## 🏠 Home Page

> *(Add `screenshots/home.png`)*

---

## 📄 Upload Assignment

> *(Add `screenshots/upload.png`)*

---

## 📊 Academic Integrity Report

> *(Add `screenshots/report.png`)*

---

# 🔮 Future Scope

- Instructor-specific writing style analysis
- Semantic plagiarism detection using vector embeddings
- Learning Management System (LMS) integration
- Multi-language academic integrity analysis
- Historical assignment comparison
- Institutional analytics dashboard
- Explainable AI reports for faculty

---

# 👨‍💻 Author

**Kanishka Tyagi**

IBM AICTE Internship 2026

Academic Integrity Intelligence Platform (AIIP)

---

# 📄 License

This project was developed as part of the **IBM AICTE Internship 2026** for educational and demonstration purposes.
