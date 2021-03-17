import requests

def get(url):
    res = requests.get(url)
    if res.status_code != 200:
        return None
    return res.json()