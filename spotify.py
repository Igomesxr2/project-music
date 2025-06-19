from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

import tkinter as tk
from tkinter import ttk

# Função chamada quando o usuário seleciona um gênero
def selecionar_genero(event):
    genero_selecionado = genero_var.get()
    print(f"Gênero selecionado: {genero_selecionado}")

# Criação da janela principal
janela = tk.Tk()
janela.title("Escolha um Gênero Musical")
janela.geometry("300x150")

# Lista de gêneros musicais
generos = [
    "Rock",
    "Pop",
    "Sertanejo",
    "Funk",
    "Jazz",
    "Blues",
    "Clássica",
    "Hip-Hop",
    "Eletrônica",
    "MPB",
    "Forró",
    "Reggae"
]

# Variável que armazenará o gênero selecionado
genero_var = tk.StringVar()
genero_var.set("Selecione um gênero")  # Valor padrão

# Criar o dropdown (Combobox)
genero_dropdown = ttk.Combobox(janela, textvariable=genero_var, values=generos, state="readonly")
genero_dropdown.pack(pady=20)

# Evento ao selecionar um gênero
genero_dropdown.bind("<<ComboboxSelected>>", selecionar_genero)

# Rodar a interface
janela.mainloop()


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")  
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
         "Authorization" : "Basic " + auth_base64,
         "Content-Type" : "application/x-www-form-urlencoded"
    }

    data = {"grant_type" : "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def test(token , artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content) ["artists"] ["items"]
    if len(json_result) == 0:
        print("Sem artista aqui")
        return None
    return json_result[0]
 
token = get_token()

result = test(token, "Jotape")

print(result["name"])

