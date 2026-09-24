import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


def parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings:
    APP_NAME = "LegalEase API"
    APP_VERSION = "1.0.0"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    BACKEND_URL = os.getenv(
        "BACKEND_URL",
        "http://127.0.0.1:8000"
    )

    CORS_ORIGINS = parse_csv(
        os.getenv(
            "CORS_ORIGINS",
            "http://localhost:8501,http://127.0.0.1:8501"
        )
    )

    REQUEST_TIMEOUT_SECONDS = int(
        os.getenv("REQUEST_TIMEOUT_SECONDS", "120")
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()