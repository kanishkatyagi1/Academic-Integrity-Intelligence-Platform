"""Central configuration for the AIIP FastAPI backend."""

from functools import lru_cache
from os import environ
from pathlib import Path

from dotenv import dotenv_values
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or a local .env file."""

    app_name: str = "Academic Integrity Intelligence Platform"
    app_version: str = "1.0.0"
    api_prefix: str = ""
    cors_origins: str | None = None

    upload_dir: Path = Path("../uploads")
    report_dir: Path = Path("../reports")

    ibm_api_key: str | None = None
    ibm_project_id: str | None = None
    ibm_region: str | None = None
    ibm_granite_model_id: str | None = None
    demo_mode: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def watsonx_url(self) -> str:
        """Return the watsonx.ai service URL for the configured IBM region."""

        return f"https://{self.ibm_region}.ml.cloud.ibm.com"

    @property
    def allowed_origins(self) -> list[str]:
        """Split the comma-separated CORS origins into a list."""

        origins = self.cors_origins or "http://localhost:5173,http://127.0.0.1:5173"
        return [origin.strip() for origin in origins.split(",") if origin.strip()]

    def missing_ibm_variables(self) -> list[str]:
        """Return required IBM environment variables that are not configured."""

        configured_names = set(environ) | set(dotenv_values(".env"))
        required_values = {
            "IBM_API_KEY": self.ibm_api_key,
            "IBM_PROJECT_ID": self.ibm_project_id,
            "IBM_REGION": self.ibm_region,
            "IBM_GRANITE_MODEL_ID": self.ibm_granite_model_id,
            "CORS_ORIGINS": self.cors_origins,
        }
        return [
            name
            for name, value in required_values.items()
            if name not in configured_names or not str(value or "").strip()
        ]


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
