import requests

url = "https://api.reccobeats.com/v1/track"
params = {
    "ids": "01K4zKU104LyJ8gMb7227B"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print(response.json())
else:
    print("Erro:", response.status_code)
    print(response.text)
