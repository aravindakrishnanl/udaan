
from datetime import datetime
from typing import Dict, List, Union
from app.schemas import TranslationLog
from app.database import add_log_entry

# Mock Translation Dictionary
# In a real application, you would integrate with Google Translate API or another service here.
# For demonstration purposes, this dictionary simulates translations for a few languages.
MOCK_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": { # English (source language)
        "Hello": {
            "ta": "வணக்கம்", # Tamil
            "hi": "नमस्ते", # Hindi
            "kn": "ನಮಸ್ತೆ", # Kannada
            "bn": "হ্যালো"  # Bengali
        },
        "How are you?": {
            "ta": "எப்படி இருக்கிறீர்கள்?",
            "hi": "आप कैसे हैं?",
            "kn": "ಹೇಗಿದ್ದೀರಾ?",
            "bn": "কেমন আছেন?"
        },
        "Thank you": {
            "ta": "நன்றி",
            "hi": "धन्यवाद",
            "kn": "ಧನ್ಯವಾದಗಳು",
            "bn": "ধন্যবাদ"
        },
        "Good morning": {
            "ta": "காலை வணக்கம்",
            "hi": "सुप्रभात",
            "kn": "ಶುಭೋದಯ",
            "bn": "শুভ সকাল"
        },
        "I love programming": {
            "ta": "நான் நிரலாக்கத்தை விரும்புகிறேன்",
            "hi": "मुझे प्रोग्रामिंग पसंद है",
            "kn": "ನನಗೆ ಪ್ರೋಗ್ರಾಮಿಂಗ್ ಇಷ್ಟ",
            "bn": "আমি প্রোগ্রামিং ভালোবাসি"
        },
        "The quick brown fox jumps over the lazy dog.": {
            "ta": "வேகமான பழுப்பு நரி சோம்பேறி நாயின் மீது குதிக்கிறது.",
            "hi": "तेज भूरी लोमड़ी आलसी कुत्ते के ऊपर कूदती है।",
            "kn": "ವೇಗದ ಕಂದು ನರಿ ಸೋಮಾರಿ ನಾಯಿಯ ಮೇಲೆ ನೆಗೆಯುತ್ತದೆ.",
            "bn": "দ্রুত বাদামী শিয়াল অলস কুকুরের উপর ঝাঁপিয়ে পড়ে।"
        },
        "This is a test sentence.": {
            "ta": "இது ஒரு சோதனை வாக்கியம்.",
            "hi": "यह एक परीक्षण वाक्य है।",
            "kn": "ಇದು ಒಂದು ಪರೀಕ್ಷಾ ವಾಕ್ಯ.",
            "bn": "এটি একটি পরীক্ষা বাক্য।"
        }
    }
}

# Supported target languages for the mock API.
SUPPORTED_TARGET_LANGUAGES = ["ta", "hi", "kn", "bn"]

def _mock_translate(text: str, target_language: str) -> str:
    """
    Mocks the Google Translate API.
    It attempts to translate the given text to the target language using a predefined dictionary.
    If the text or language is not supported by the mock, it returns a generic message.
    """
    # Normalize text for lookup (e.g., lowercase, remove punctuation if needed)
    # For simplicity, we'll use exact match for now.
    
    translated_text = MOCK_TRANSLATIONS.get("en", {}).get(text, {}).get(target_language)
    
    if translated_text:
        return translated_text
    else:
        # Fallback if specific translation is not found in mock data
        return f"Translation for '{text}' to '{target_language}' not available in mock. (Mock: {text} -> {target_language})"

async def translate_text_service(text: str, target_language: str) -> str:
    """
    Translates a single block of text.
    Handles the translation logic and logs the request.

    Args:
        text (str): The text to be translated.
        target_language (str): The ISO code of the target language.

    Returns:
        str: The translated text.

    Raises:
        ValueError: If the target language is not supported by the mock API.
    """
    translated_text = None
    status = "error"
    error_message = None

    try:
        if target_language not in SUPPORTED_TARGET_LANGUAGES:
            raise ValueError(f"Target language '{target_language}' is not supported by the mock API.")
        
        # Simulate API call delay if desired:
        # await asyncio.sleep(0.1) 

        translated_text = _mock_translate(text, target_language)
        status = "success"
        return translated_text
    except ValueError as e:
        error_message = str(e)
        raise # Re-raise the exception to be caught by the API route
    except Exception as e:
        error_message = f"An unexpected error occurred during translation: {str(e)}"
        raise # Re-raise the exception
    finally:
        # Log the translation request regardless of success or failure
        log_entry = TranslationLog(
            timestamp=datetime.now().isoformat(),
            original_text=text,
            target_language=target_language,
            translated_text=translated_text,
            status=status,
            error_message=error_message
        )
        add_log_entry(log_entry)

async def bulk_translate_service(sentences: List[str], target_language: str) -> List[str]:
    """
    Translates a list of sentences in bulk.
    Iterates through each sentence, translates it, and logs each translation.

    Args:
        sentences (List[str]): A list of sentences to be translated.
        target_language (str): The ISO code of the target language.

    Returns:
        List[str]: A list of translated sentences.

    Raises:
        ValueError: If the target language is not supported by the mock API.
    """
    translated_sentences: List[str] = []
    
    if target_language not in SUPPORTED_TARGET_LANGUAGES:
        # Log the bulk request failure
        log_entry = TranslationLog(
            timestamp=datetime.now().isoformat(),
            original_text=f"Bulk request for {len(sentences)} sentences",
            target_language=target_language,
            translated_text=None,
            status="error",
            error_message=f"Target language '{target_language}' is not supported by the mock API for bulk translation."
        )
        add_log_entry(log_entry)
        raise ValueError(f"Target language '{target_language}' is not supported by the mock API.")

    for sentence in sentences:
        translated_text = None
        status = "error"
        error_message = None
        try:
            # Each sentence is treated as a separate translation for logging purposes
            translated_text = _mock_translate(sentence, target_language)
            status = "success"
            translated_sentences.append(translated_text)
        except Exception as e:
            error_message = f"Error translating sentence '{sentence}': {str(e)}"
            translated_sentences.append(f"[ERROR] {sentence}") # Indicate error in output
        finally:
            log_entry = TranslationLog(
                timestamp=datetime.now().isoformat(),
                original_text=sentence,
                target_language=target_language,
                translated_text=translated_text,
                status=status,
                error_message=error_message
            )
            add_log_entry(log_entry)
            
    return translated_sentences
