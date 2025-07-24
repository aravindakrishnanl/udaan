import logging
from typing import List, Dict, Any

import requests
from fastapi import FastAPI, HTTPException, APIRouter, Body
from pydantic import BaseModel, Field, validator
from app.schemas import HealthStatus, TranslationRequest, TranslationResponse
from app.services import TranslationService

api_router = APIRouter()

@api_router.get("/", summary="Welcome Endpoint")
def read_root():
    """A simple welcome message to confirm the service is running."""
    return {"message": "Welcome to Project Udaan - Translation Microservice!"}

@api_router.get("/health", response_model=HealthStatus, summary="Health Check")
def health_check():
    """Provides a simple health check endpoint to confirm the service is operational."""
    logging.info("Health check requested.")
    return {"status": "ok"}

@api_router.post("/translate", response_model=TranslationResponse, summary="Translate a single block of text")
def translate_single_text(request: TranslationRequest):
    """
    Accepts a single block of text and a target language, and returns the translation.
    """
    translated = TranslationService.translate_text(
        text=request.text,
        target_lang=request.target_language
    )
    return TranslationResponse(
        source_text=request.text,
        translated_text=translated,
        target_language=request.target_language
    )

@api_router.post("/translate/bulk", response_model=BulkTranslationResponse, summary="Translate a list of sentences")
def translate_bulk_text(request: BulkTranslationRequest):
    """
    Accepts an array of sentences for translation.
    Note: This performs sequential API calls. For high-throughput, you might
    consider asynchronous requests.
    """
    results = []
    for req_item in request.requests:
        try:
            translated = TranslationService.translate_text(
                text=req_item.text,
                target_lang=req_item.target_language
            )
            results.append(TranslationResponse(
                source_text=req_item.text,
                translated_text=translated,
                target_language=req_item.target_language
            ))
        except HTTPException as e:
            # For bulk requests, we can choose to return partial results.
            # Here, we'll create a response indicating the error for the failed item.
             results.append(TranslationResponse(
                source_text=req_item.text,
                translated_text=f"ERROR: {e.detail}",
                target_language=req_item.target_language
            ))
    return BulkTranslationResponse(results=results)

@api_router.get("/logs", summary="View Translation Request Logs")
def get_logs():
    """
    (For Demo) Returns the in-memory log of translation requests.
    In a real application, you would read from a database or log file.
    """
    return {"request_logs": TranslationService.request_log}

