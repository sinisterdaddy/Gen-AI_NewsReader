import requests

API_KEY="ZGVqb2RlbTQ2MUBodWl6ay5jb20:aYbSvK-Hpb5S8D4ycgvNj"

def download_video(id):
    url = "https://api.d-id.com/talks/"+id

    headers = {
        "accept": "application/json",
        "authorization": f"Basic {API_KEY}"
    }

    response = requests.get(url, headers=headers)
    print(response.json())
    url=response.json()["result_url"]
    
    return url