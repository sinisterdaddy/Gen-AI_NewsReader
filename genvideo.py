import requests

API_KEY = "amlyaWxheDU3NkBlYnV0aG9yLmNvbQ:HRTF85Tr1zKSyxhrNomzx"
url = "https://api.d-id.com/talks"

def genvideo(img_url, summary, v_id):
    payload = {
        "source_url": img_url,
        "script": {
            "type": "text",
            "input": summary,
            "provider": {
                "type": "microsoft",
                "voice_id": v_id,
                "voice_config": {
                    "style": "Default"
                }
            }
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {API_KEY}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        id = response.json().get("id")
        if id is not None:
            print("Video ID:", id)
            return id
        else:
            print("Failed to get video ID from response JSON:", response.json())
            return None
    except requests.RequestException as e:
        print("Error occurred during request:", e)
        return None

# Example usage:
# genvideo("https://clips-presenters.d-id.com/amy/Aq6OmGZnMt/Vcq0R4a8F0/image.png", "News summary", "en-US-SaraNeural")
