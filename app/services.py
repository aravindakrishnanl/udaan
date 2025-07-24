import logging
import requests
from typing import List, Dict, Any
from fastapi import HTTPException

# In-memory log for demonstration purposes.
request_log: List[Dict[str, Any]] = []

def translate_text(text: str, target_lang: str, source_lang: str = "en") -> str:
    """Translates text using the MyMemory API."""
    api_url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": f"{source_lang}|{target_lang}"}

    try:
        logging.info(f"Requesting translation for '{text[:30]}...' to '{target_lang}'")
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Log the request details
        request_log.append({
            "source_text": text,
            "target_language": target_lang,
            "api_response_status": data.get("responseStatus")
        })

        if data.get("responseStatus") == 200:
            translated_text = data["responseData"]["translatedText"]
            logging.info(f"Translation successful: '{translated_text[:30]}...'")
            return translated_text
        else:
            error_details = data.get("responseDetails", "Unknown API error")
            logging.error(f"API returned an error: {error_details}")
            raise HTTPException(status_code=502, detail=f"Translation API error: {error_details}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Could not connect to translation service: {e}")
        raise HTTPException(status_code=503, detail="Translation service is unavailable.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during translation: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

def get_request_logs():
    """Returns the in-memory log of translation requests."""
    return request_log