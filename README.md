# Academic Integrity Intelligence Platform (AIIP)

> A clean, working demo built for the IBM AICTE Internship submission.

AIIP lets a user upload an assignment PDF, extracts the text through a FastAPI backend, sends it for IBM Granite–style academic integrity analysis, and displays a structured report in a React interface.

> **Note:** This is intentionally a demo project for internship submission — not a production or enterprise product.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Getting Started](#getting-started)
  - [Backend Setup](#backend-setup)
  - [IBM Granite Configuration](#ibm-granite-configuration)
  - [Frontend Setup](#frontend-setup)
- [API Endpoints](#api-endpoints)
- [Demo Flow](#demo-flow)
- [Known Limitations](#known-limitations)
- [Notes for Submission](#notes-for-submission)
- [License](#license)

---

## Tech Stack

| Layer    | Technology |
|----------|------------|
| Frontend | React, Vite, TailwindCSS |
| Backend  | FastAPI |
| AI       | IBM Granite via watsonx.ai (when credentials are configured) |
| Storage  | Local `uploads/` and `reports/` folders |

## Features

- Home page with project overview
- PDF upload page
- PDF text extraction
- IBM Granite analysis prompt covering:
  - Summary
  - Possible plagiarism observations
  - Possible AI-generated content
  - Citation suggestions
  - Academic Integrity Score (0–100)
  - Recommendations
- Structured, readable report page
- Auto-generated FastAPI OpenAPI documentation
- Clear API errors when IBM credentials are missing or Granite is unreachable

## Folder Structure

```
academic-integrity-intelligence-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── granite_service.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── pdf_utils.py
│   │   └── storage.py
│   ├── .env.example
│   └── requirements.txt
├── dataset/
│   └── sample-assignment.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ReportPage.jsx
│   │   │   └── UploadPage.jsx
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   └── tailwind.config.js
├── reports/
├── uploads/
└── README.md
```

## Getting Started

### Backend Setup

From the project root:

```bash
cd backend
python -m venv .venv

# Activate the virtual environment
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend URLs:

- Health check: `http://localhost:8000/health`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- Swagger UI: `http://localhost:8000/docs`

### IBM Granite Configuration

Copy `backend/.env.example` to `backend/.env` and fill in your IBM watsonx.ai credentials:

```env
IBM_API_KEY=your-api-key
IBM_PROJECT_ID=your-project-id
IBM_REGION=us-south
IBM_GRANITE_MODEL_ID=ibm/granite-13b-instruct-v2
```

If credentials aren't configured, the backend returns a clear API error rather than silently switching to demo output. Set `DEMO_MODE=true` in `backend/.env` only when you intentionally want local demo output (no real IBM credentials required).

### Frontend Setup

Open a second terminal from the project root:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

## API Endpoints

### `GET /health`

Checks whether the backend is running.

### `POST /upload`

Accepts a PDF assignment as multipart form data.

**Response includes:**
- `file_id`
- `filename`
- `text`
- `text_length`

### `POST /analyze`

Accepts extracted text and returns an academic integrity report.

**Request body:**

```json
{
  "file_id": "optional-upload-id",
  "text": "Extracted assignment text..."
}
```

## Demo Flow

1. Start the backend.
2. Start the frontend.
3. Open the frontend in a browser.
4. Go to the Upload page.
5. Select an assignment PDF.
6. Generate the integrity report.
7. Review the report page.

## Known Limitations

- No authentication or multi-user support — this is a single-session demo.
- No persistent database; reports and uploads are stored as local files, not in a DB.
- Plagiarism detection is prompt-based (via Granite) rather than backed by a reference corpus or web-crawling engine, so results should be treated as indicative, not authoritative.
- Not optimized for large PDFs or high concurrent load.

## Notes for Submission

- Clean module separation between `backend/app` components.
- FastAPI automatically generates OpenAPI documentation.
- Reports are saved as JSON files in `reports/`.
- Uploaded PDFs are saved in `uploads/`.
- Real Granite analysis is used when IBM credentials are provided.
- Local demo output is available only when `DEMO_MODE=true` is explicitly set.

## License

No license currently specified. Add a `LICENSE` file (e.g., MIT) if you intend for others to reuse this code.