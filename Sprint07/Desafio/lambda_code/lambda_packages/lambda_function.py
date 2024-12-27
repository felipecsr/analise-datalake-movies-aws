import os
import json
import requests
import logging
import boto3
from datetime import datetime
from botocore.exceptions import NoCredentialsError

# Configuração de logs com nível DEBUG para capturar todos os detalhes
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Cliente do S3
s3 = boto3.client('s3')

def fetch_movie_details(movie_id, tmdb_api_key):
    """Busca os detalhes de um filme específico usando o ID."""
    logging.debug(f"Buscando detalhes do filme ID: {movie_id}")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": tmdb_api_key}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        logging.debug(f"Detalhes do filme {movie_id} recuperados com sucesso.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar detalhes do filme {movie_id}: {e}")
        raise

def fetch_movies_by_interval(genre_id, start_year, end_year, tmdb_api_key, max_pages=500):
    """Busca filmes por gênero e intervalo de anos, capturando todas as páginas."""
    base_url = "https://api.themoviedb.org/3/discover/movie"
    all_movies = []
    page = 1

    while True:
        params = {
            "with_genres": genre_id,
            "primary_release_date.gte": f"{start_year}-01-01",
            "primary_release_date.lte": f"{end_year}-12-31",
            "page": page,
            "api_key": tmdb_api_key
        }
        try:
            logging.info(f"Buscando filmes - Gênero: {genre_id}, Intervalo: {start_year}-{end_year}, Página: {page}")
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Adiciona os filmes da página atual
            movies = data.get("results", [])
            all_movies.extend(movies)

            total_pages = data.get("total_pages", 0)
            logging.debug(f"Página {page} de {total_pages} processada.")

            # Verifica se chegou na última página
            if page >= total_pages or page >= max_pages:
                logging.info(f"Busca completa: total de {len(all_movies)} filmes capturados.")
                break

            # Avança para a próxima página
            page += 1

        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao buscar filmes na página {page}: {e}")
            break

    return all_movies

def save_to_s3(bucket_name, folder_path, filename, data):
    """Salva o JSON no S3."""
    file_path = f"{folder_path}/{filename}"
    try:
        logging.info(f"Tentando salvar arquivo {filename} no bucket {bucket_name}.")
        s3.put_object(Bucket=bucket_name, Key=file_path, Body=json.dumps(data, ensure_ascii=False, indent=4))
        logging.info(f"Arquivo salvo no S3: s3://{bucket_name}/{file_path}")
    except NoCredentialsError:
        logging.error("Credenciais AWS não configuradas corretamente.")
        raise
    except Exception as e:
        logging.error(f"Erro ao salvar arquivo no S3: {e}")
        raise

def lambda_handler(event, context):
    """Handler principal do AWS Lambda."""
    logging.debug("Iniciando execução do lambda_handler.")
    logging.debug(f"Evento recebido: {event}")

    tmdb_api_key = os.getenv("TMDB_API_KEY")
    if not tmdb_api_key:
        logging.error("Chave da API do TMDb não configurada.")
        raise ValueError("Chave da API do TMDb não configurada nas variáveis de ambiente.")
    
    bucket_name = "desafio-filmes-series"
    base_path = f"Raw/TMDB/JSON/Movies/{datetime.now().strftime('%Y/%m/%d')}"

    # Validação de parâmetros no evento
    if "start_year" not in event or "genre_id" not in event:
        logging.error("Os parâmetros 'start_year' e 'genre_id' são obrigatórios.")
        raise KeyError("Os parâmetros 'start_year' e 'genre_id' são obrigatórios no evento.")

    start_year = int(event["start_year"])
    genre_id = event["genre_id"]
    end_year = start_year + 4  # Ajustando para intervalos de 5 anos
    logging.debug(f"Parâmetros processados: start_year={start_year}, end_year={end_year}, genre_id={genre_id}")

    logging.info(f"Processando filmes do gênero {genre_id} para o intervalo {start_year}-{end_year}.")

    try:
        movies = fetch_movies_by_interval(genre_id, start_year, end_year, tmdb_api_key)
        logging.info(f"Número total de filmes processados: {len(movies)}.")

        detailed_movies = []
        for movie in movies:
            try:
                movie_id = movie.get("id")
                movie_details = fetch_movie_details(movie_id, tmdb_api_key)
                detailed_movies.append({
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
                })
            except Exception as e:
                logging.error(f"Erro ao buscar detalhes para o filme ID {movie.get('id')}: {e}")

        batch_number = 1

        # Divisão e salvamento dos registros detalhados
        for i in range(0, len(detailed_movies), 100):
            chunk = detailed_movies[i:i + 100]
            filename = f"genre-{genre_id}-{start_year}-{end_year}-{batch_number}.json"
            logging.info(f"Criando lote {batch_number}: {len(chunk)} registros serão salvos no arquivo {filename}.")
            save_to_s3(bucket_name, base_path, filename, chunk)
            logging.info(f"Lote {batch_number} salvo com sucesso: {len(chunk)} registros no arquivo {filename}.")
            batch_number += 1

        logging.info(f"Processamento completo para o intervalo {start_year}-{end_year}. Total de arquivos gerados: {batch_number - 1}.")
    except Exception as e:
        logging.error(f"Erro durante o processamento: {e}")
        raise
    finally:
        logging.debug("lambda_handler concluído com sucesso.")
