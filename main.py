# main.py
# This is the main entry point for the FastAPI application.
# It initializes the FastAPI app and includes the API routes.

from fastapi import FastAPI
from app.routes import router as api_router

# Initialize the FastAPI application
app = FastAPI(
    title="Project Udaan - Translation Microservice",
    description="A lightweight, modular translation microservice using a mock Google Translate API.",
    version="1.0.0",
)

# Include the API router, which contains all the defined endpoints.
# The prefix "/api/v1" ensures all endpoints under this router are
# accessible at paths like /api/v1/translate.
app.include_router(api_router, prefix="/api/v1")

# You can add more global event handlers here if needed,
# for example, startup/shutdown events for database connections.

# Example of a root endpoint for basic testing (optional)
@app.get("/")
async def read_root():
    """
    Root endpoint to confirm the service is running.
    """
    return {"message": "Welcome to Project Udaan Translation Microservice! Visit /docs for API documentation."}
