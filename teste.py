import requests
from flask import Flask, render_template, request
import tempfile
import os

app = Flask(__name__)

# Função para buscar id do gênero no Deezer
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

# Busca artistas pelo gênero
def get_artists_by_genre(genre_id):
    url = f"https://api.deezer.com/genre/{genre_id}/artists"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao buscar artistas do gênero {genre_id}.")
        return []
    return response.json()['data']

# Busca faixas de um artista no ano específico
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
                        'preview': track.get('preview', None),
                    })
    return tracks

# Função para chamar API ReccoBeats para extrair audio features a partir do preview (url)
def get_audio_features(preview_url):
    if not preview_url:
        return None
    url_api = "https://api.reccobeats.com/v1/analysis/audio-features"
    try:
        preview_response = requests.get(preview_url)
        if preview_response.status_code != 200:
            print(f"Erro ao baixar preview: {preview_response.status_code}")
            return None
        
        print(f"Tamanho do preview: {len(preview_response.content)} bytes")
        
        # Corrigido para evitar erro de permissão no Windows
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(preview_response.content)
            tmp_file_path = tmp_file.name

        try:
            with open(tmp_file_path, 'rb') as f_audio:
                files = {'audioFile': (os.path.basename(tmp_file_path), f_audio, 'audio/mpeg')}
                response = requests.post(url_api, files=files)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Erro ReccoBeats: {response.status_code} - {response.text}")
                    return None
        finally:
            os.remove(tmp_file_path)  # remove arquivo temporário manualmente
    except Exception as e:
        print(f"Erro ao chamar API ReccoBeats: {e}")
        return None

# Buscar músicas top por gênero e ano, pegar poucas pra teste, já com features
def get_top_tracks_by_genre_and_year(genre_name, year, top_n=5):
    genre_id = get_genre_id(genre_name)
    if not genre_id:
        return []
    
    artists = get_artists_by_genre(genre_id)
    
    all_tracks = []
    for artist in artists[:3]:  # menos artistas pra teste
        artist_id = artist['id']
        artist_tracks = get_tracks_of_artist_in_year(artist_id, year)
        all_tracks.extend(artist_tracks)
        if len(all_tracks) >= top_n:
            break
    
    all_tracks = all_tracks[:top_n]  # limitar número de músicas
    
    # Pega features de áudio pelo preview e adiciona ao dict
    for track in all_tracks:
        print(f"Analisando track: {track['title']} - {track['artist']}")
        print(f"Baixando preview de: {track['preview']}")
        features = get_audio_features(track['preview'])
        track['features'] = features or {}
    
    # Ordenar por rank (popularidade)
    all_tracks.sort(key=lambda x: x['rank'], reverse=True)
    return all_tracks


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        genero = request.form['genero']
        ano = int(request.form['ano'])
        top_n = int(request.form.get('top_n', 5))
        musicas = get_top_tracks_by_genre_and_year(genero, ano, top_n)
        return render_template('index.html', musicas=musicas, genero=genero, ano=ano)
    return render_template('index.html', musicas=None)

if __name__ == '__main__':
    app.run(debug=True)
