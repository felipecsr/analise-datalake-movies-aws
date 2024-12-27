import os
import requests
from dotenv import load_dotenv

def get_total_pages_and_results(genre_id):
    # Carregar a chave da API do TMDB a partir do arquivo .env
    load_dotenv()
    TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
    
    if not TMDB_API_KEY:
        raise ValueError("API Key do TMDB não encontrada. Certifique-se de configurá-la no arquivo .env.")

    # URL base do endpoint de descoberta
    base_url = "https://api.themoviedb.org/3/discover/movie"
    headers = {"Authorization": f"Bearer {TMDB_API_KEY}"}

    # Parâmetros para a requisição inicial
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "page": 1  # Apenas a primeira página é necessária para obter as informações
    }

    # Fazer a requisição HTTP
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code != 200:
        raise ValueError(f"Erro na API TMDB: {response.status_code}, {response.text}")

    data = response.json()
    total_results = data.get("total_results", 0)
    total_pages = data.get("total_pages", 0)

    return total_results, total_pages

def main():
    genres = {
        "Crime": 80,
        "Guerra": 10752
    }

    for genre_name, genre_id in genres.items():
        try:
            total_results, total_pages = get_total_pages_and_results(genre_id)
            print(f"Gênero: {genre_name}")
            print(f"  Total de filmes: {total_results}")
            print(f"  Total de páginas: {total_pages}")
        except Exception as e:
            print(f"Erro ao obter informações para o gênero {genre_name}: {e}")

if __name__ == "__main__":
    main()
