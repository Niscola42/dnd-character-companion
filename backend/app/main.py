from fastapi import FastAPI


app = FastAPI(
    title="D&D Character Companion API",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}