import requests

import aiohttp

API_KEY = "amlyaWxheDU3NkBlYnV0aG9yLmNvbQ:HRTF85Tr1zKSyxhrNomzx"

async def download_video(id):
    url = f"https://api.d-id.com/talks/{id}"

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {API_KEY}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_json = await response.json()
                if "result_url" in response_json:
                    url = response_json["result_url"]
                    print(url)
                    return url
                else:
                    print("Error: 'result_url' not found in API response")
                    return None
    except aiohttp.ClientError as e:
        print("Error occurred during request:", e)
        return None
