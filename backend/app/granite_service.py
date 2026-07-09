"""IBM Granite analysis service using the official IBM watsonx.ai SDK."""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from .config import Settings
from .models import IntegrityReport

logger = logging.getLogger(__name__)


class GraniteServiceError(RuntimeError):
    """Raised when IBM Granite analysis cannot be completed."""


class GraniteService:
    """Generate academic integrity reports with IBM Granite."""

    def __init__(self, settings: Settings):
        """Store settings needed for IBM watsonx.ai calls."""

        self.settings = settings

    def analyze(self, text: str) -> IntegrityReport:
        """Analyze assignment text through IBM Granite."""

        if self.settings.demo_mode:
            return self._demo_report(text, reason="DEMO_MODE=true is enabled")

        missing_variables = self.settings.missing_ibm_variables()
        if missing_variables:
            joined_names = ", ".join(missing_variables)
            raise GraniteServiceError(
                f"Missing IBM watsonx.ai environment variables: {joined_names}. "
                "Create backend/.env and restart the backend."
            )

        try:
            return self._analyze_with_granite(text)
        except GraniteServiceError:
            raise
        except Exception as exc:
            logger.exception("IBM Granite analysis failed: %s", exc)
            raise GraniteServiceError(f"IBM Granite analysis failed: {exc}") from exc

    def _analyze_with_granite(self, text: str) -> IntegrityReport:
        """Call IBM Granite through the official watsonx.ai SDK."""

        try:
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
        except ImportError as exc:
            raise GraniteServiceError(
                "The ibm-watsonx-ai SDK is not installed. Run: pip install -r requirements.txt"
            ) from exc

        prompt = self._build_prompt(text)
        credentials = Credentials(
            url=self.settings.watsonx_url,
            api_key=self.settings.ibm_api_key,
        )
        model = ModelInference(
            model_id=self.settings.ibm_granite_model_id,
            credentials=credentials,
            project_id=self.settings.ibm_project_id,
            params={
                GenParams.DECODING_METHOD: "greedy",
                GenParams.MAX_NEW_TOKENS: 900,
                GenParams.MIN_NEW_TOKENS: 150,
                GenParams.TEMPERATURE: 0.2,
            },
        )

        generated_text = model.generate_text(prompt=prompt)
        parsed = self._parse_json_block(generated_text)

        return IntegrityReport(
            summary=str(parsed.get("summary", "")).strip(),
            plagiarism_observations=self._as_list(parsed.get("plagiarism_observations")),
            ai_generated_content=self._as_list(parsed.get("ai_generated_content")),
            citation_suggestions=self._as_list(parsed.get("citation_suggestions")),
            academic_integrity_score=self._score(parsed.get("academic_integrity_score")),
            recommendations=self._as_list(parsed.get("recommendations")),
            model_used=self.settings.ibm_granite_model_id,
            demo_mode=False,
        )

    def _build_prompt(self, text: str) -> str:
        """Build the analysis prompt sent to IBM Granite."""

        clipped_text = text[:12000]
        return f"""
You are an academic integrity assistant for a university internship demo.
Analyze the assignment text below. Do not accuse the student. Use cautious language.

Return only valid JSON with these exact keys:
summary: string for Assignment Summary
plagiarism_observations: array of strings for Possible Plagiarism Observations
ai_generated_content: array of strings for Possible AI-Generated Content
citation_suggestions: array of strings for Citation Suggestions
recommendations: array of strings
academic_integrity_score: integer from 0 to 100

Assignment text:
\"\"\"{clipped_text}\"\"\"
"""

    def _parse_json_block(self, generated_text: str) -> dict[str, Any]:
        """Extract a JSON object from a language-model response."""

        match = re.search(r"\{.*\}", generated_text, flags=re.DOTALL)
        if not match:
            raise GraniteServiceError("IBM Granite did not return a JSON report.")
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise GraniteServiceError("IBM Granite returned invalid JSON.") from exc

    def _as_list(self, value: Any) -> list[str]:
        """Normalize model output into a list of strings."""

        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        return []

    def _score(self, value: Any) -> int:
        """Clamp a model-provided score into the allowed 0-100 range."""

        try:
            score = int(value)
        except (TypeError, ValueError):
            score = 70
        return max(0, min(100, score))

    def _demo_report(self, text: str, reason: str) -> IntegrityReport:
        """Create a deterministic local report for demo runs without IBM credentials."""

        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        unique_ratio = len(set(words)) / max(len(words), 1)
        citation_hits = len(re.findall(r"\((?:[A-Za-z]+,\s*)?\d{4}\)|\[\d+\]", text))
        ai_markers = [
            phrase
            for phrase in ["in conclusion", "it is important to note", "overall", "furthermore"]
            if phrase in text.lower()
        ]

        score = 78
        if unique_ratio < 0.45:
            score -= 14
        if citation_hits == 0:
            score -= 12
        if len(ai_markers) >= 2:
            score -= 8
        score = max(0, min(100, score))

        return IntegrityReport(
            summary=(
                "The submission discusses the uploaded assignment content and appears suitable "
                "for an academic-integrity review. This report is generated in demo mode because "
                f"{reason}."
            ),
            plagiarism_observations=[
                "Repeated vocabulary or low source variety may require manual comparison with references."
                if unique_ratio < 0.45
                else "No direct source overlap can be confirmed without a reference database.",
                "Use this observation as a screening signal, not as proof of plagiarism.",
            ],
            ai_generated_content=[
                "Some broad transition phrases may resemble AI-assisted writing."
                if ai_markers
                else "No strong AI-writing pattern was detected by the local demo heuristic.",
                "A human review should check whether claims, examples, and citations match course expectations.",
            ],
            citation_suggestions=[
                "Add in-text citations for factual claims, statistics, definitions, and borrowed ideas."
                if citation_hits == 0
                else "Review citation formatting for consistency across all referenced claims.",
                "Include a complete bibliography or references section in the required academic style.",
            ],
            academic_integrity_score=score,
            recommendations=[
                "Ask the student to clarify sources for unsupported claims.",
                "Check the uploaded text against institutional plagiarism tools if available.",
                "Encourage transparent disclosure when AI tools were used for drafting or editing.",
            ],
            model_used=f"{self.settings.ibm_granite_model_id} (local demo fallback)",
            demo_mode=True,
        )
