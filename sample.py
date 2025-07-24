import requests
import json

api_url = "http://127.0.0.1:8000/api/translate/bulk"

bulk_request_data = {
  "requests": [
    {
      "text": "Hello, how are you?",
      "target_language": "hi"  
    },
    {
      "text": "This is a test of the bulk translation service.",
      "target_language": "ta" 
    },
    {
      "text": "This is a test of the bulk translation service.",
      "target_language": "bn" 
    }
  ]
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(api_url, headers=headers, data=json.dumps(bulk_request_data))

    response.raise_for_status()

    response_data = response.json()

    print("Request Successful!")
    print("Response from server:")
    print(json.dumps(response_data, indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")