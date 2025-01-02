## 🎯 Objetivo 🔴🔴🔴
Este README, da sprint 08, é o segundo de cinco etapas que compõem o **Desafio Final do Programa de Bolsas da Compass UOL**.

O desafio, em resumo, objetiva a construção de dashboard para análises de dados provenientes de um Data Lake, com um pipeline completo envolvendo coleta, tratamento, análise e visualização de dados. A etapa atual focou na **extração de informações da API pública do TMDB** para complementar os dados locais, na camada de dados brutos, ainda não filtrados e tratdos. Utilizamos tecnologias como AWS Lambda, AWS S3, AWS EventBridge e CloudWatch para garantir automação e eficiência nessa coleta.

Nesta sprint, o objetivo principal foi implementar a extração de dados do TMDB, com foco nos gêneros **Crime e Guerra**, seguindo critérios definidos para garantir que os dados coletados estejam devidamente organizados e otimizados para armazenamento e análises posteriores.

<br/>

## ✍ Escopo das atividades - Etapa 2 do desafio
- Criar uma função Lambda para extrair os dados do TMDB.
    > com limite de 15 minutos na execução da lambda 
- Foi necessário a segmentação das consultas por gênero e recortes temporais de 5 em 5 anos para respeitar os limites da API.
    > limitação de 500 páginas por requisição e limitação de 50 requisições por segundo
- Automatizar as execuções utilizando parâmetros (*eventos* na linguagem de AWS Lambda) de cada segmento agendamentos via `AWS EventBridge`.
    > com as entradas de gênero e períodos de lançamentos dos filmes
- Garantir que os dados extraídos estejam organizados no bucket S3 em formato JSON, obedecendo à estrutura de pastas definida.
    > organizados dentro da camada de dados brutos
- Testar localmente e na nuvem, ajustando o código e os agendamentos conforme necessário para otimizar o desempenho e respeitar os limites de execução da API e da função Lambda.
    > arquivos com até 100 registros e no máximo 10 MB

<br/>

## ▶️ Resolução do desafio!

### · λ Desenvolvimento e ajustes no código
A função Lambda foi implementada com os seguintes pontos de destaque:

- Entrada de dados via eventos JSON, contendo o gênero ('id 80' para Crime e 'id 10752' para Guerra) e o ano inicial para o recorte de 5 anos.
- Paginação automatizada para lidar com o limite de 500 páginas por consulta da API do TMDB.
- Armazenamento otimizado, com os dados extraídos organizados em múltiplos arquivos JSON, cada um contendo no máximo 100 registros para respeitar o limite de 10 MB por arquivo no S3.
- O código foi testado localmente para garantir a funcionalidade e o tempo necessário para a execução completa, considerando os limites de 15 minutos da função Lambda.

#### Script de teste de extração (local)
``` python
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
```
Obs: *neste momento do teste já havia mapeado o dado `imdb_id`que servirá como chave primária para integrar as base de dados, desta sprint e os dados orieundos dos IMDB da sprint 06.*

<br/>

#### Script de para mapeamento do volume de registros e páginas (estudando a API e planajando o *script servless*)
```python
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
```
OBS: o resultado deste contador, no próprio terminal, em 27/12/2024 às 17h00, foi o seguinte:
``` bash
Gênero: Crime
  Total de filmes: 35319
  Total de páginas: 1766
Gênero: Guerra
  Total de filmes: 11116
  Total de páginas: 556
```

<br/>

### Script para execução como Função Lambda
```python
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
```

<br/>

## 🌐 Testes e agendamento no AWS

### Testes locais

Inicialmente, foram realizados testes para verificar o tempo de execução e a estrutura dos arquivos gerados.
Identificou-se que uma única consulta poderia exceder o limite de 15 minutos quando da execução via `AWS Lambda`. Assim, foram adotados recortes de 5 anos por execução.

### Configuração do agendamento no AWS:

Foi criado mais um script em python, para execução via `AWS CLI` para agendar 50 execuções automáticas, cada uma com intervalo de 1 minuto, para evitar atingir os limites de requisições e páginas da API.  

Cada execução enviava um evento JSON para a função Lambda, com informações do gênero e do período de 5 anos a ser extraído.

```python
import os
import json
import logging
import boto3
from datetime import datetime, timedelta, timezone

# Configuração de logs
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Cliente AWS Scheduler
scheduler = boto3.client('scheduler')

# Configurações iniciais
lambda_arn = "arn:aws:lambda:us-east-1:767828750921:function:extract_tmdb_crimes_war"  # Substitua pelo ARN correto
role_arn = "arn:aws:iam::767828750921:role/service-role/extract_tmdb_crimes_war-role-6jvjnxv6"  # Substituído pelo ARN correto com ID da conta e nome do role
region = "us-east-1"
genres = [
    {"id": 80, "name": "Crime"},       # Gênero Crime
    {"id": 10752, "name": "Guerra"}   # Gênero Guerra
]
decades = list(range(1900, 2025, 5))  # Intervalos de 5 anos de 1900 até 2024

# Configuração de tempo
start_time = datetime(2024, 12, 27, 16, 55, tzinfo=timezone.utc)  # Ajustado para UTC correspondente ao horário local (UTC-3, 15h02 no Brasil)
interval_minutes = 1  # Intervalo de 1 minuto entre os cronogramas

# Loop para criar cronogramas
for genre_index, genre in enumerate(genres):
    for decade_index, start_year in enumerate(decades):
        # Nome do cronograma
        schedule_name = f"Schedule_{genre['name']}_{start_year}-{start_year + 4}"

        # Payload para a Lambda
        payload = {
            "start_year": start_year,
            "genre_id": genre["id"]
        }

        # Calcular o horário para cada execução
        schedule_time = start_time + timedelta(minutes=(genre_index * len(decades) + decade_index) * interval_minutes)
        cron_expression = f"cron({schedule_time.minute} {schedule_time.hour} {schedule_time.day} {schedule_time.month} ? {schedule_time.year})"

        # Criar o cronograma
        try:
            logging.info(f"Criando cronograma: {schedule_name} com cronograma {cron_expression}...")
            scheduler.create_schedule(
                Name=schedule_name,
                ScheduleExpression=cron_expression,
                FlexibleTimeWindow={"Mode": "OFF"},
                Target={
                    "Arn": lambda_arn,
                    "RoleArn": role_arn,
                    "Input": json.dumps(payload)
                }
            )
            logging.info(f"Cronograma criado com sucesso: {schedule_name}")
        except Exception as e:
            logging.error(f"Erro ao criar cronograma {schedule_name}: {e}")
```

![evidência dos agendamentos](../evidencias/desafio/1-scheduler.png)

### Armazenamento no S3:

Os dados foram organizados em um diretório específico dentro do bucket desafio-filmes-series, com a seguinte estrutura, e organizados em **473 objetos** (arquivos `.json`):

> s3://desafio-filmes-series/Raw/TMDB/JSON/Movies/2024/12/27/

<br/>

![arquivos armazenados no bucket](../evidencias/desafio/2-json_extracted.png)

## 🔍 Monitoramento
O processo foi monitorado via CloudWatch para garantir que todas as execuções ocorreram com sucesso. Também foi validado se os arquivos gerados estavam sendo salvos corretamente no bucket S3.

Neste ponto houveram dificuldades que não consegui superar, sobre logs detalhados de execução. Infelizmente só consegui inicio e fim da execução, sem detalhamentos de monitoramento.

<br/>

## 💾 Resultados
### Tempo de execução otimizado: 
Cada execução da função Lambda foi configurada para processar apenas 5 anos, garantindo que o tempo máximo de 15 minutos não fosse excedido.

### Dados organizados: 
Arquivos JSON de até 100 registros, com tamanho médio de 150 KB, armazenados em uma estrutura lógica no S3.

### Automação bem-sucedida: 
A integração com EventBridge garantiu que os agendamentos ocorreram sem falhas.

<br/>

## 📌 Considerações finais sobre a Sprint 07

A Sprint 07 foi desafiadora e enriquecedora, com foco em compreender e utilizar os serviços AWS para extrair e organizar dados de forma eficiente. Essa etapa consolidou o aprendizado sobre:

- Configuração e uso de funções Lambda para tarefas automáticas e escaláveis.
- Gerenciamento de limites de APIs públicas e ajustes necessários para otimizar processos.
- Organização de dados no S3, criando uma base sólida para as próximas etapas do desafio.

O resultado alcançado é um pipeline funcional e confiável para a extração de dados do TMDB, atendendo aos requisitos do desafio e estabelecendo uma base sólida para análises futuras.

Estou motivado para avançar para as próximas sprints, onde os dados coletados serão tratados e utilizados para a criação de dashboards analíticos no AWS QuickSight. 🚀
