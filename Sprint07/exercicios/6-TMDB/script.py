import requests
import pandas as pd
from IPython.display import display
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave de API do TMDB
api_key = os.getenv("TMDB_API_KEY")

# Verificar se a chave foi carregada corretamente
if not api_key:
    raise ValueError("Chave de API não encontrada. Verifique o arquivo .env.")

# URL da API (ajustado para Crime e Guerra)
url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=pt-BR"

# Fazer a requisição
response = requests.get(url)
data = response.json()

# Lista para armazenar os filmes
filmes = []

# Coletar os primeiros 30 registros diretamente
for movie in data['results'][:30]:
    df = {
        'Título': movie['title'],
        'Data de Lançamento': movie['release_date'],
        'Visão Geral': movie['overview'],
        'Votos': movie['vote_count'],
        'Média de Votos': movie['vote_average']
    }
    filmes.append(df)

# Criar DataFrame
df = pd.DataFrame(filmes)

# Exibir DataFrame
display(df)
