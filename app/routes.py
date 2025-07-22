
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from typing import List

from app.schemas import (
    TranslationRequest,
    TranslationResponse,
    BulkTranslationRequest,
    BulkTranslationResponse,
    HealthCheckResponse,
    TranslationLog
)
from app.services import translate_text_service, bulk_translate_service, SUPPORTED_TARGET_LANGUAGES
from app.database import get_all_logs

# Create an APIRouter instance. This allows organizing routes into separate files.
router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse, summary="Health Check")
async def health_check():
    """
    **Health Check Endpoint**

    This endpoint provides a simple way to check the operational status of the microservice.
    It returns a JSON object indicating the service's health and the current timestamp.

    **Responses:**
    - `200 OK`: If the service is running correctly.
      Returns: `{"status": "healthy", "timestamp": "ISO 8601 datetime"}`
    """
    return HealthCheckResponse(status="healthy", timestamp=datetime.now().isoformat())

@router.post(
    "/translate",
    response_model=TranslationResponse,
    status_code=status.HTTP_200_OK,
    summary="Translate Text Block"
)
async def translate_text(request: TranslationRequest):
    """
    **Translate Text Block**

    This endpoint accepts a block of text and a target language, then returns the translated text.

    **Request Body:**
    - `text` (string, required): The text (up to 1000 characters) to be translated.
    - `target_language` (string, required): The ISO 639-1 code of the target language (e.g., `ta`, `hi`, `kn`, `bn`).

    **Responses:**
    - `200 OK`: Translation successful.
      Returns: `{"original_text": "...", "translated_text": "...", "target_language": "..."}`
    - `400 Bad Request`: Invalid input (e.g., unsupported language, text too long).
      Returns: `{"detail": "Error message"}`
    - `500 Internal Server Error`: An unexpected error occurred during translation.
      Returns: `{"detail": "Error message"}`
    """
    try:
        translated_text = await translate_text_service(request.text, request.target_language)
        return TranslationResponse(
            original_text=request.text,
            translated_text=translated_text,
            target_language=request.target_language
        )
    except ValueError as e:
        # Catch specific ValueErrors from the service layer (e.g., unsupported language)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post(
    "/bulk-translate",
    response_model=BulkTranslationResponse,
    status_code=status.HTTP_200_OK,
    summary="Bulk Translate Sentences"
)
async def bulk_translate_sentences(request: BulkTranslationRequest):
    """
    **Bulk Translate Sentences**

    This endpoint accepts an array of sentences and a target language, then returns
    a list of translated sentences.

    **Request Body:**
    - `sentences` (array of strings, required): A list of sentences to be translated.
    - `target_language` (string, required): The ISO 639-1 code of the target language.

    **Responses:**
    - `200 OK`: Bulk translation successful.
      Returns: `{"original_sentences": [...], "translated_sentences": [...], "target_language": "..."}`
    - `400 Bad Request`: Invalid input (e.g., unsupported language).
      Returns: `{"detail": "Error message"}`
    - `500 Internal Server Error`: An unexpected error occurred during translation.
      Returns: `{"detail": "Error message"}`
    """
    # Basic validation for sentence length (each sentence should ideally be short)
    # This can be refined based on actual API limits or performance considerations.
    for sentence in request.sentences:
        if len(sentence) > 1000: # Re-using the 1000 char limit for individual sentences
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sentence '{sentence[:50]}...' exceeds maximum length of 1000 characters."
            )

    try:
        translated_sentences = await bulk_translate_service(request.sentences, request.target_language)
        return BulkTranslationResponse(
            original_sentences=request.sentences,
            translated_sentences=translated_sentences,
            target_language=request.target_language
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during bulk translation: {str(e)}"
        )

@router.get(
    "/logs",
    response_model=List[TranslationLog],
    summary="Retrieve Translation Logs"
)
async def get_logs():
    """
    **Retrieve Translation Logs**

    This endpoint retrieves all stored translation request logs.

    **Responses:**
    - `200 OK`: Returns a list of translation log entries.
    """
    return get_all_logs()