"""Pydantic request and response models for the AIIP API."""

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Response returned after a PDF assignment is uploaded and parsed."""

    file_id: str = Field(..., description="Unique identifier for the uploaded file.")
    filename: str = Field(..., description="Original uploaded PDF file name.")
    text: str = Field(..., description="Extracted assignment text.")
    text_length: int = Field(..., description="Number of extracted characters.")


class AnalyzeRequest(BaseModel):
    """Request body for analyzing assignment text with IBM Granite."""

    file_id: str | None = Field(default=None, description="Optional uploaded file identifier.")
    text: str = Field(..., min_length=20, description="Assignment text to analyze.")


class IntegrityReport(BaseModel):
    """Structured academic integrity report returned by the analysis endpoint."""

    summary: str
    plagiarism_observations: list[str]
    ai_generated_content: list[str]
    citation_suggestions: list[str]
    academic_integrity_score: int = Field(..., ge=0, le=100)
    recommendations: list[str]
    model_used: str
    demo_mode: bool = Field(
        default=False,
        description="True only when DEMO_MODE=true explicitly enables local demo logic.",
    )


class AnalyzeResponse(BaseModel):
    """Response returned after an assignment is analyzed."""

    report_id: str
    file_id: str | None
    report: IntegrityReport


class HealthResponse(BaseModel):
    """Health-check response used by the frontend and OpenAPI clients."""

    status: str
    app: str
    version: str
