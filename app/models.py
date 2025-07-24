from pydantic import BaseModel, Field, validator
from typing import List

class TranslationRequest(BaseModel):
    """Defines the structure for a single translation request."""
    text: str = Field(
        ...,
        title="Text to Translate",
        description="The source text that needs to be translated.",
        max_length=1000
    )
    target_language: str = Field(
        ...,
        title="Target Language (ISO 639-1 Code)",
        description="The ISO code for the target language (e.g., 'ta' for Tamil, 'hi' for Hindi).",
        min_length=2,
        max_length=5
    )

    @validator('target_language')
    def language_code_to_lower(cls, v):
        return v.lower()

class TranslationResponse(BaseModel):
    """Defines the structure for a single translation response."""
    source_text: str
    translated_text: str
    target_language: str

class BulkTranslationRequest(BaseModel):
    """Defines the structure for a bulk translation request."""
    requests: List[TranslationRequest]

class BulkTranslationResponse(BaseModel):
    """Defines the structure for a bulk translation response."""
    results: List[TranslationResponse]

class HealthStatus(BaseModel):
    """Defines the structure for the health check response."""
    status: str