import requests

# URL base da API
base_url = "https://api.reccobeats.com/v1"

# Exemplo: Obter recomendações com base em um gênero
def get_music_recommendations(seed_genres, limit=20):
    endpoint = f"{base_url}/recommendations"
    params = {
        "seed_genres": seed_genres,  # Exemplo: "pop,rock"
        "limit": limit
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Levanta exceção para erros HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

# Exemplo de chamada
recommendations = get_music_recommendations(seed_genres="pop", limit=10)
if recommendations:
    print(recommendations)


def extract_audio_features(file_path):
    endpoint = "https://api.reccobeats.com/v1/analysis/audio-features"
    headers = {"Content-Type": "multipart/form-data"}
    try:
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(endpoint, files=files, headers=headers)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None

# Exemplo de chamada
features = extract_audio_features("path/to/audio.mp3")
if features:
    print(features)