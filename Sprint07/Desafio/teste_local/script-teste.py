import os
import json
from datetime import datetime
from dotenv import load_dotenv
from tmdbv3api import TMDb, Movie, Genre

def fetch_movies_by_genre(target_genres):
    # Carregar a chave da API do arquivo .env
    load_dotenv()
    TMDB_API_KEY = os.getenv("TMDB_API_KEY")

    if not TMDB_API_KEY:
        raise ValueError("API Key do TMDB não encontrada. Certifique-se de configurá-la no arquivo .env.")

    # Configuração da API TMDB
    tmdb = TMDb()
    tmdb.api_key = TMDB_API_KEY
    tmdb.language = "pt-BR"

    movie_api = Movie()
    genre_api = Genre()

    # Obter mapeamento de gêneros
    genres = genre_api.movie_list()
    genre_map = {g["name"]: g["id"] for g in genres}

    # Identificar os IDs dos gêneros-alvo (Crime e Guerra)
    target_genre_ids = [genre_map[g] for g in target_genres if g in genre_map]

    # Paginação e filtro por gênero
    all_movies = []
    page = 1
    while len(all_movies) < 100:
        movies = movie_api.popular(page=page)
        if not movies:
            break  # Se não houver mais filmes, interrompa
        for movie in movies:
            if len(all_movies) >= 100:
                return all_movies  # Limitar exatamente a 100 registros
            if set(movie.genre_ids).intersection(target_genre_ids):
                # Obter detalhes completos do filme
                movie_details = movie_api.details(movie.id)
                movie_data = {
                    "id_tmdb": movie_details.id,
                    "title": movie_details.title,
                    "release_date": movie_details.release_date,
                    "overview": movie_details.overview,
                    "poster_path": movie_details.poster_path,
                    "backdrop_path": movie_details.backdrop_path,
                    "production_companies": [
                        {"name": company.name, "id": company.id} for company in (movie_details.production_companies or [])
                    ],
                    "production_countries": [
                        {"iso_3166_1": country.iso_3166_1, "name": country.name} for country in (movie_details.production_countries or [])
                    ],
                    "spoken_languages": [
                        {"iso_639_1": language.iso_639_1, "name": language.name} for language in (movie_details.spoken_languages or [])
                    ],
                    "budget": movie_details.budget,
                    "revenue": movie_details.revenue,
                    "vote_average": movie_details.vote_average,
                    "adult": movie_details.adult,
                    "belongs_to_collection": {
                        "id": movie_details.belongs_to_collection.id,
                        "name": movie_details.belongs_to_collection.name
                    } if movie_details.belongs_to_collection else None,
                    "homepage": movie_details.homepage,
                    "imdb_id": movie_details.imdb_id,
                    "original_language": movie_details.original_language,
                    "popularity": movie_details.popularity,
                    "status": movie_details.status,
                    "tagline": movie_details.tagline,
                    "video": movie_details.video
                }
                all_movies.append(movie_data)
        page += 1

    return all_movies

def save_movies_to_json(movies, base_path="desafio-filmes-series/Raw/TMDB/JSON/Movies"):
    # Configurar o caminho com base na data atual
    today = datetime.now()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")

    output_dir = os.path.join(base_path, year, month, day)
    os.makedirs(output_dir, exist_ok=True)

    batch_size = 100
    for i, batch in enumerate(range(0, len(movies), batch_size)):
        batch_data = movies[batch:batch + batch_size]
        file_path = os.path.join(output_dir, f"movies_batch_{i + 1}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(batch_data, f, ensure_ascii=False, indent=4)

        print(f"Arquivo salvo: {file_path}")

def main():
    try:
        print("Buscando filmes dos gêneros Crime e Guerra do TMDB...")
        target_genres = ["Crime", "Guerra"]
        movies = fetch_movies_by_genre(target_genres)

        print(f"Total de filmes encontrados: {len(movies)}")

        print("Salvando os filmes em arquivos JSON...")
        save_movies_to_json(movies)

        print("Processo concluído com sucesso.")
    except Exception as e:
        print(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    main()
