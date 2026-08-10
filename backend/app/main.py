from fastapi import FastAPI

from app.api.router import api_router

from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


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

app.include_router(api_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}