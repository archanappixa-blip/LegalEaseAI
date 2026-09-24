from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from backend.config import (
    get_settings
)

from backend.routes import router


settings = get_settings()


app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP_VERSION,

    description=(
        "LegalEase AI-assisted "
        "legal document drafting "
        "and export API."
    )
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=(
        settings.CORS_ORIGINS
    ),

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.include_router(
    router
)