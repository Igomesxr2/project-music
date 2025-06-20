import requests

def get_genre_id(genre_name):
    url = "https://api.deezer.com/genre"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erro ao buscar gêneros.")
        return None
    genres = response.json()['data']
    for genre in genres:
        if genre_name.lower() == genre['name'].lower():
            return genre['id']
    print(f"Gênero '{genre_name}' não encontrado.")
    return None

def get_artists_by_genre(genre_id):
    url = f"https://api.deezer.com/genre/{genre_id}/artists"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao buscar artistas do gênero {genre_id}.")
        return []
    return response.json()['data']

def get_tracks_of_artist_in_year(artist_id, year):
    url_albums = f"https://api.deezer.com/artist/{artist_id}/albums"
    response = requests.get(url_albums)
    if response.status_code != 200:
        return []
    albums = response.json().get('data', [])
    
    tracks = []
    for album in albums:
        release_date = album.get('release_date', '')
        if release_date.startswith(str(year)):
            album_id = album['id']
            url_tracks = f"https://api.deezer.com/album/{album_id}/tracks"
            resp_tracks = requests.get(url_tracks)
            if resp_tracks.status_code == 200:
                album_tracks = resp_tracks.json().get('data', [])
                for track in album_tracks:
                    tracks.append({
                        'title': track['title'],
                        'artist': track['artist']['name'],
                        'rank': track.get('rank', 0),
                        'link': track['link']
                    })
    return tracks

def get_top_tracks_by_genre_and_year(genre_name, year, top_n=50):
    genre_id = get_genre_id(genre_name)
    if not genre_id:
        return
    
    artists = get_artists_by_genre(genre_id)
    
    all_tracks = []
    for artist in artists[:20]:
        artist_id = artist['id']
        artist_tracks = get_tracks_of_artist_in_year(artist_id, year)
        all_tracks.extend(artist_tracks)
    
    if not all_tracks:
        print(f"Nenhuma música encontrada no gênero '{genre_name}' no ano {year}.")
        return
    
    # Ordenar por rank (popularidade)
    all_tracks.sort(key=lambda x: x['rank'], reverse=True)

    # Filtrar por rank acima de 70
    filtered_tracks = [track for track in all_tracks if track['rank'] > 70]
    
    print(f"\nTop {top_n} músicas do gênero '{genre_name}' no ano {year} com rank acima de 70:\n")
    for track in filtered_tracks[:top_n]:
        print(f"{track['title']} - {track['artist']} | Popularidade: {track['rank']} | Link: {track['link']}")

# -------------------------
# EXEMPLO DE USO:
genero_input = input("Digite o gênero musical: ")
ano_input = input("Digite o ano (ex: 2023): ")

get_top_tracks_by_genre_and_year(genero_input, int(ano_input), top_n=100)
