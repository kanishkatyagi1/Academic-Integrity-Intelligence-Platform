# Academic Integrity Intelligence Platform (AIIP)

<!-- README for the IBM AICTE internship full-stack demo project. -->

AIIP is a clean working demo for IBM AICTE Internship submission. It lets a user upload an assignment PDF, extracts the PDF text through a FastAPI backend, sends the text for IBM Granite-style academic integrity analysis, and displays a structured report in a React interface.

This is intentionally a demo project, not an enterprise product.

## Tech Stack

- Frontend: React, Vite, TailwindCSS
- Backend: FastAPI
- AI: IBM Granite through watsonx.ai when credentials are configured
- Storage: Local `uploads/` and `reports/` folders

## Features

- Home page for the project overview
- PDF upload page
- PDF text extraction
- IBM Granite analysis prompt for:
  - Summary
  - Possible plagiarism observations
  - Possible AI-generated content
  - Citation suggestions
  - Academic Integrity Score from 0 to 100
  - Recommendations
- Beautiful report page
- FastAPI OpenAPI documentation
- Clear API errors when IBM credentials are missing or Granite cannot be reached

## Folder Structure

```text
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

## Backend Setup

From the project root:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend URLs:

- Health API: `http://localhost:8000/health`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- Swagger UI: `http://localhost:8000/docs`

## IBM Granite Configuration

Copy `backend/.env.example` to `backend/.env` and fill in your IBM watsonx.ai credentials:

```env
IBM_API_KEY=your-api-key
IBM_PROJECT_ID=your-project-id
IBM_REGION=us-south
IBM_GRANITE_MODEL_ID=ibm/granite-13b-instruct-v2
```

If credentials are not configured, the backend returns a clear API error instead of silently switching to demo output. Set `DEMO_MODE=true` in `backend/.env` only when you intentionally want local demo output.

## Frontend Setup

Open a second terminal from the project root:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## API Endpoints

### GET `/health`

Checks whether the backend is running.

### POST `/upload`

Accepts a PDF assignment as multipart form data.

Response includes:

- `file_id`
- `filename`
- `text`
- `text_length`

### POST `/analyze`

Accepts extracted text and returns an academic integrity report.

Request:

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
4. Go to Upload.
5. Select an assignment PDF.
6. Generate the integrity report.
7. Review the report page.

## Notes for Submission

- The project uses clean module separation.
- FastAPI automatically generates OpenAPI.
- Reports are saved as JSON files in `reports/`.
- Uploaded PDFs are saved in `uploads/`.
- Real Granite analysis is used when IBM credentials are provided.
- Local demo output is available only when `DEMO_MODE=true` is explicitly configured.
