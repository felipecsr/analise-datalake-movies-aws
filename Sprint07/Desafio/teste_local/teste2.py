import os
import json
import requests
import logging
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_movie_details(movie_id, tmdb_api_key):
    """Busca os detalhes de um filme específico usando o ID."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": tmdb_api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_movies_by_year(genre_id, year, tmdb_api_key, max_pages=500):
    """Busca filmes por gênero e ano-calendário com todos os campos detalhados."""
    base_url = "https://api.themoviedb.org/3/discover/movie"
    all_movies = []

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    for page in range(1, max_pages + 1):
        params = {
            "with_genres": genre_id,
            "primary_release_date.gte": start_date,
            "primary_release_date.lte": end_date,
            "page": page,
            "api_key": tmdb_api_key
        }
        try:
            logging.info(f"Buscando filmes - Gênero: {genre_id}, Ano: {year}, Página: {page}")
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            movies = data.get("results", [])
            if not movies:
                logging.info("Nenhum filme encontrado ou páginas esgotadas.")
                break

            for movie in movies:
                # Obter detalhes do filme
                movie_details = fetch_movie_details(movie["id"], tmdb_api_key)
                movie_data = {
                    "id_tmdb": movie_details.get("id"),
                    "title": movie_details.get("title"),
                    "release_date": movie_details.get("release_date"),
                    "overview": movie_details.get("overview"),
                    "poster_path": movie_details.get("poster_path"),
                    "backdrop_path": movie_details.get("backdrop_path"),
                    "production_companies": [
                        {"name": company["name"], "id": company["id"]} for company in movie_details.get("production_companies", [])
                    ],
                    "production_countries": [
                        {"iso_3166_1": country["iso_3166_1"], "name": country["name"]} for country in movie_details.get("production_countries", [])
                    ],
                    "spoken_languages": [
                        {"iso_639_1": language["iso_639_1"], "name": language["name"]} for language in movie_details.get("spoken_languages", [])
                    ],
                    "budget": movie_details.get("budget"),
                    "revenue": movie_details.get("revenue"),
                    "vote_average": movie_details.get("vote_average"),
                    "adult": movie_details.get("adult"),
                    "belongs_to_collection": {
                        "id": movie_details["belongs_to_collection"]["id"],
                        "name": movie_details["belongs_to_collection"]["name"]
                    } if movie_details.get("belongs_to_collection") else None,
                    "homepage": movie_details.get("homepage"),
                    "imdb_id": movie_details.get("imdb_id"),
                    "original_language": movie_details.get("original_language"),
                    "popularity": movie_details.get("popularity"),
                    "status": movie_details.get("status"),
                    "tagline": movie_details.get("tagline"),
                    "video": movie_details.get("video")
                }
                all_movies.append(movie_data)

            # Adicionando atraso para evitar bloqueios
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao buscar filmes na página {page}: {e}")
            break

    return all_movies

def save_movies_locally(movies, genre_name, year):
    """Salva os filmes localmente em arquivos JSON por ano."""
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    json_data = json.dumps(movies, ensure_ascii=False, indent=4)
    file_name = f"{output_folder}/{genre_name}_{year}.json"
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(json_data)
        logging.info(f"Arquivo salvo localmente: {file_name}")
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo {file_name}: {e}")

def main():
    """Função principal para execução local."""
    tmdb_api_key = os.getenv("TMDB_API_KEY")
    genres = {
        "Guerra": {"id": 10752, "years": range(1900, 2025)}  # Gera arquivos de 1900 a 2024
    }

    for genre_name, genre_data in genres.items():
        genre_id = genre_data["id"]
        for year in genre_data["years"]:
            logging.info(f"Processando filmes do gênero {genre_name} no ano {year}...")
            movies = fetch_movies_by_year(genre_id, year, tmdb_api_key)
            save_movies_locally(movies, genre_name, year)

if __name__ == "__main__":
    main()
