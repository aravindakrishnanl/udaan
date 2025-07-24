import logging
import requests
import urllib.parse
from typing import List, Dict, Any
from fastapi import HTTPException

request_log: List[Dict[str, Any]] = []

def translate_text(text: str, target_lang: str, source_lang: str = "auto") -> str:
    """
    Translates text using a public Google Translate endpoint.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    encoded_text = urllib.parse.quote(text)
    
    api_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={encoded_text}"

    try:
        logging.info(f"Requesting translation for '{text[:30]}...' to '{target_lang}'")
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        request_log.append({
            "source_text": text,
            "target_language": target_lang,
            "api_response_status": response.status_code
        })

        if response.status_code == 200 and data and data[0]:
            translated_text = "".join([segment[0] for segment in data[0]])
            logging.info(f"Translation successful: '{translated_text[:30]}...'")
            return translated_text
        else:
            error_details = "Failed to parse translation from API response."
            logging.error(error_details)
            raise HTTPException(status_code=502, detail=f"Translation API error: {error_details}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Could not connect to translation service: {e}")
        raise HTTPException(status_code=503, detail="Translation service is unavailable.")
    except (IndexError, TypeError) as e:
        logging.error(f"Error parsing the translation API response: {e}")
        raise HTTPException(status_code=500, detail="Could not parse response from translation service.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during translation: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

def get_request_logs():
    """Returns the in-memory log of translation requests."""
    return request_log