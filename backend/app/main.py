from fastapi import FastAPI

from app.api.router import api_router

from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="D&D Character Companion API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],


)
settings.upload_directory.mkdir(
    parents=True,
    exist_ok=True,
)

app.mount(
    "/uploads",
    StaticFiles(
        directory=settings.upload_directory
    ),
    name="uploads",
)

app.include_router(api_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}