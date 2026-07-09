"""File-system storage helpers for uploads and generated reports."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from .models import AnalyzeResponse


def ensure_directories(upload_dir: Path, report_dir: Path) -> None:
    """Create required storage folders if they are missing."""

    upload_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)


def save_upload(file: UploadFile, upload_dir: Path) -> tuple[str, Path]:
    """Persist an uploaded PDF and return its generated file id and path."""

    file_id = uuid4().hex
    safe_name = Path(file.filename or "assignment.pdf").name
    destination = upload_dir / f"{file_id}_{safe_name}"

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_id, destination


def save_report(response: AnalyzeResponse, report_dir: Path) -> Path:
    """Write an analysis report as JSON for later inspection."""

    report_path = report_dir / f"{response.report_id}.json"
    report_path.write_text(
        json.dumps(response.model_dump(), indent=2),
        encoding="utf-8",
    )
    return report_path
