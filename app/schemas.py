from pydantic import BaseModel, Field
from typing import List, Optional

# Define a Pydantic model for a single translation request.
# This schema is used for the POST /translate endpoint.
class TranslationRequest(BaseModel):
    """
    Schema for a single translation request.
    - text: The text to be translated (up to 1000 characters).
    - target_language: The ISO code of the target language (e.g., 'ta', 'hi').
    """
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The text block to be translated (max 1000 characters)."
    )
    target_language: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="The ISO 639-1 code of the target language (e.g., 'ta', 'hi', 'kn', 'bn')."
    )

# Define a Pydantic model for a bulk translation request.
# This schema is used for the POST /bulk-translate endpoint.
class BulkTranslationRequest(BaseModel):
    """
    Schema for a bulk translation request, containing a list of sentences.
    - sentences: A list of strings, where each string is a sentence to be translated.
    - target_language: The ISO code of the target language.
    """
    sentences: List[str] = Field(
        ...,
        min_items=1,
        description="A list of sentences to be translated."
    )
    target_language: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="The ISO 639-1 code of the target language (e.g., 'ta', 'hi', 'kn', 'bn')."
    )

# Define a Pydantic model for a single translation response.
# This schema is used for the response of the POST /translate endpoint.
class TranslationResponse(BaseModel):
    """
    Schema for a single translation response.
    - original_text: The original text that was translated.
    - translated_text: The text after translation.
    - target_language: The target language ISO code.
    """
    original_text: str = Field(..., description="The original text provided for translation.")
    translated_text: str = Field(..., description="The translated text.")
    target_language: str = Field(..., description="The ISO 639-1 code of the target language.")

# Define a Pydantic model for a bulk translation response.
# This schema is used for the response of the POST /bulk-translate endpoint.
class BulkTranslationResponse(BaseModel):
    """
    Schema for a bulk translation response, containing a list of translated sentences.
    - original_sentences: The list of original sentences.
    - translated_sentences: The list of translated sentences.
    - target_language: The target language ISO code.
    """
    original_sentences: List[str] = Field(..., description="The original sentences provided for translation.")
    translated_sentences: List[str] = Field(..., description="The translated sentences.")
    target_language: str = Field(..., description="The ISO 639-1 code of the target language.")

# Define a Pydantic model for logging translation requests.
# This schema is used internally for storing log entries.
class TranslationLog(BaseModel):
    """
    Schema for a translation log entry.
    - timestamp: The time the request was made.
    - original_text: The original text.
    - target_language: The target language.
    - translated_text: The translated text (if successful).
    - status: The status of the translation (e.g., 'success', 'error').
    - error_message: Optional error message if the translation failed.
    """
    timestamp: str = Field(..., description="Timestamp of the translation request.")
    original_text: str = Field(..., description="The original text submitted.")
    target_language: str = Field(..., description="The target language for translation.")
    translated_text: Optional[str] = Field(None, description="The translated text (if successful).")
    status: str = Field(..., description="Status of the translation (e.g., 'success', 'error').")
    error_message: Optional[str] = Field(None, description="Error message if translation failed.")

# Define a Pydantic model for the health check response.
class HealthCheckResponse(BaseModel):
    """
    Schema for the health check response.
    - status: The status of the service (e.g., 'healthy').
    - timestamp: The current server timestamp.
    """
    status: str = Field(..., description="Status of the service.")
    timestamp: str = Field(..., description="Current server timestamp.")
