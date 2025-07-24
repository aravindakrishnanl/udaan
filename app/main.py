import logging
from fastapi import FastAPI
from .routes import router as api_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Project Udaan - Translation Microservice",
    description="A lightweight RESTful API for text translation, structured for maintainability.",
    version="1.1.0",
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root_redirect():
    """A simple welcome message at the root."""
    return {
        "message": "Welcome! The API is available under the /api path. Go to /docs for the interactive API documentation."
    }