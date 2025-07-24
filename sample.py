import requests
import json

api_url = "http://127.0.0.1:8000/api/translate"

headers = {
    "Content-Type": "application/json"
}

def translate_custom_text():
    """
    Prompts the user for text and a language, then sends a request
    to the translation microservice.
    """
    print("\n--- New Translation ---")
    
    try:
        text_to_translate = input("Enter the text you want to translate (or type 'quit' to exit): ")
        if text_to_translate.lower() == 'quit':
            return False

        target_lang = input("Enter the target language code (e.g., hi, ta, fr, es): ")
        if not target_lang:
            print("Error: Target language cannot be empty.")
            return True
    except (KeyboardInterrupt, EOFError):
        return False

    request_data = {
        "text": text_to_translate,
        "target_language": target_lang.lower() 
    }

    print(f"\nSending request to translate '{text_to_translate}' to '{target_lang}'...")

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(request_data))

        response.raise_for_status()

        response_data = response.json()

        print("\nTranslation Successful!")
        print(f"  Source Text: {response_data.get('source_text')}")
        print(f"  Target Language: {response_data.get('target_language')}")
        print(f"  Translated Text: {response_data.get('translated_text')}")

    except requests.exceptions.HTTPError as e:
        print(f"\nAn error occurred: {e.response.status_code} {e.response.reason}")
        print(f"   Server says: {e.response.json().get('detail', 'No details provided.')}")
    except requests.exceptions.RequestException as e:
        print(f"\nA network error occurred: {e}")
        print("   Please make sure your FastAPI server is running.")

    return True 

if __name__ == "__main__":
    
    while translate_custom_text():
        pass
    print("\n  Exited")
