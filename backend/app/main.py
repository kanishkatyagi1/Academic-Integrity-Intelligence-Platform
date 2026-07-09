"""FastAPI entry point for the Academic Integrity Intelligence Platform."""

from pathlib import Path
from uuid import uuid4

import logging

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .granite_service import GraniteService, GraniteServiceError
from .models import AnalyzeRequest, AnalyzeResponse, HealthResponse, UploadResponse
from .pdf_utils import extract_text_from_pdf
from .storage import ensure_directories, save_report, save_upload

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    settings = get_settings()
    ensure_directories(settings.upload_dir, settings.report_dir)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Demo API for PDF upload, text extraction, and IBM Granite academic integrity analysis.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Return a simple API health check."""

    return HealthResponse(status="ok", app=settings.app_name, version=settings.app_version)


@app.post("/upload", response_model=UploadResponse, tags=["Assignments"])
def upload_assignment(
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
) -> UploadResponse:
    """Upload a PDF assignment and extract readable text from it."""

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_id, saved_path = save_upload(file, Path(settings.upload_dir))

    try:
        text = extract_text_from_pdf(saved_path)
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Could not extract text from PDF.") from exc

    if not text:
        raise HTTPException(status_code=422, detail="No readable text was found in the PDF.")

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        text=text,
        text_length=len(text),
    )


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Assignments"])
def analyze_assignment(
    payload: AnalyzeRequest,
    settings: Settings = Depends(get_settings),
) -> AnalyzeResponse:
    """Analyze extracted assignment text with IBM Granite."""

    service = GraniteService(settings)
    try:
        report = service.analyze(payload.text)
    except GraniteServiceError as exc:
        logger.exception("Academic integrity analysis failed: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    response = AnalyzeResponse(
        report_id=uuid4().hex,
        file_id=payload.file_id,
        report=report,
    )
    save_report(response, Path(settings.report_dir))
    return response
