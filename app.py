import google.generativeai as genai

# Configurar sua API Key
genai.configure(api_key="AIzaSyB7ACIUjNNC0betBYVo1eIPc13cWIG2NcA")

# Carregar o modelo Gemini (exemplo com Gemini Flash)
model = genai.GenerativeModel('gemini-2.0-flash')

# Fazer uma chamada simples



import tkinter as tk
from tkinter import ttk

# Função chamada quando o usuário seleciona um gênero
def selecionar_genero(event):
    genero_selecionado = genero_var.get()
    print(f"Gênero selecionado: {genero_selecionado}")
    response = model.generate_content(f"Dê uma descrição sobre o gênero: {genero_selecionado}")

    print(response.text)

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
