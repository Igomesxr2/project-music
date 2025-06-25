import requests
from flask import Flask, render_template, request

app = Flask(__name__)

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
                    })
    return tracks

def get_top_tracks_by_genre_and_year(genre_name, year, top_n):
    genre_id = get_genre_id(genre_name)
    if not genre_id:
        return []
    
    artists = get_artists_by_genre(genre_id)
    
    all_tracks = []
    for artist in artists[:10]:
        artist_id = artist['id']
        artist_tracks = get_tracks_of_artist_in_year(artist_id, year)
        all_tracks.extend(artist_tracks)
    
    if not all_tracks:
        print(f"Nenhuma música encontrada no gênero '{genre_name}' no ano {year}.")
        return []
    
    # Ordenar por rank (popularidade)
    all_tracks.sort(key=lambda x: x['rank'], reverse=True)
    filter_tracks = [track for track in all_tracks if track['rank'] > 500000]
    return filter_tracks


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        genero = request.form['genero']
        ano = int(request.form['ano'])
        top_n = int(request.form.get('top_n', 50))

        musicas = get_top_tracks_by_genre_and_year(genero, ano, top_n)
        return render_template('index.html', musicas=musicas, genero=genero, ano=ano)
    
    return render_template('index.html', musicas=None)
    
if __name__ == '__main__':
    app.run(debug=True)

