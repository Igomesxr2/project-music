import requests

def listar_generos():
    url = "https://api.deezer.com/genre"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erro ao buscar gêneros.")
        return

    genres = response.json()['data']
    print("Gêneros disponíveis:")
    for genre in genres:
        print(f"{genre['id']}: {genre['name']}")

listar_generos()
