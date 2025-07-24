from fastapi import APIRouter, HTTPException
from . import services
from .models import (
    TranslationRequest,
    TranslationResponse,
    BulkTranslationRequest,
    BulkTranslationResponse,
    HealthStatus
)

router = APIRouter()

@router.get("/", summary="Welcome Endpoint")
def read_root():
    return {"message": "Welcome to Project Udaan - Translation Microservice!"}

@router.get("/health", response_model=HealthStatus, summary="Health Check")
def health_check():
    return {"status": "ok"}

@router.post("/translate", response_model=TranslationResponse, summary="Translate a single block of text")
def translate_single_text(request: TranslationRequest):
    translated = services.translate_text(
        text=request.text,
        target_lang=request.target_language
    )
    return TranslationResponse(
        source_text=request.text,
        translated_text=translated,
        target_language=request.target_language
    )

@router.post("/translate/bulk", response_model=BulkTranslationResponse, summary="Translate a list of sentences")
def translate_bulk_text(request: BulkTranslationRequest):
    results = []
    for req_item in request.requests:
        try:
            translated = services.translate_text(
                text=req_item.text,
                target_lang=req_item.target_language
            )
            results.append(TranslationResponse(
                source_text=req_item.text,
                translated_text=translated,
                target_language=req_item.target_language
            ))
        except HTTPException as e:
             results.append(TranslationResponse(
                source_text=req_item.text,
                translated_text=f"ERROR: {e.detail}",
                target_language=req_item.target_language
            ))
    return BulkTranslationResponse(results=results)

@router.get("/logs", summary="View Translation Request Logs")
def get_logs():
    return {"request_logs": services.get_request_logs()}