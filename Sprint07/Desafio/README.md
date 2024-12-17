
# 🎯 Objetivo 🔴

Este README, da sprint 07, é o primeiro de cinco etapas que compõem o **Desafio Final Programa de Bolsas da Compass UOL**.  

**O desafio, em resumo**, (que começa na sprint 06 e termina na sprint 10) consiste na criação de dashboards para análise de dados provenientes de um Data Lake - que estamos começando a construir nesta sprint. Todo o processo envolverá a troca de arquivos locais, execução de scripts em ambiente local e na nuvem, extração de dados de APIs públicas, tratamentos diversos, com o objetivo final de integrar ao Console AWS, e lá criar visualizações analíticas.  

**Como primeira etapa do desafio**, nesta sprint, recebemos dois arquivos `csv` contendo dados sobre filmes e séries, com informações diversas desse universo. Inicialmente, fomos orientados a explorar esses dados, levando em consideração as possibilidades adicionais que surgirão ao extrair informações via API do [site TMDB](https://www.themoviedb.org/?language=pt-br).   

Após a análise do conjunto de dados e das [possibilidades de dados extraíveis do TMDB](../Desafio/Lista%20de%20possibilidades%20TMBD%20-%20Preparado%20por%20Felipe%20Reis%20-%20Planilhas%20Google.pdf), o ponto de partida dos trabalhos seria a elaboração de perguntas a serem respondidas ao final do desafio, que orientarão todo o processo. A seguir, apresentamos algumas perguntas direcionadoras.

>Para a minha squad, número 2, o tema são séries e filmes do gênero **Crime e Guerra**.

<br/>

## ❓ Perguntas direcionadoras do desafio

1) Dentro do segmento `Crime/ Guerra`, quais os 10 ou 20 filmes mais votados(`numeroVotos`) e melhores votados (`notaMedia`)?

2) Destes, existe algum ator ou atriz (`nomeArtista`) que aparece em mais de um filme?

    *Obs: eventualmente inverter 2 e 1, para caso a amostragem seja inviável nessa disposição apresentada.* 

3) Destes, quais os atores/atrizes que estão vivos (`anoFalecimento`), de acordo com a base?

4) Destes, com os dados agregados do TMDB, quais são os filmes com melhor resultado (`revenue` - `budget`), ou seja que a receita cobre o orçamento?

5) Outra análise que é possível é de valor médio de orçamento x receita (ou diferença = resultado), na linha do tempo, talvez anualmente ou por décadas.

<br/>

## ▶️ Resolução do desafio!

### 🐍 Criação do script em Python

A primeira etapa foi a criação do script com o seguinte escopo:

- **Configura variáveis** com o nome do bucket S3 e os caminhos dos arquivos CSV.
- **Lê e valida** os arquivos CSV com `pandas`.
- **Verifica e cria** o bucket S3 caso não exista.
- **Faz upload** dos arquivos CSV para o S3.

*Obs: realizei o teste localmente antes da criação e execução do container, para primeiro teste.*

```python
import boto3
from botocore.exceptions import ProfileNotFound
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configurações principais
BUCKET_NAME = "desafio-filmes-series"

# Gerar automaticamente os caminhos de pasta com base na data atual
today = datetime.now()
year, month, day = today.strftime("%Y"), today.strftime("%m"), today.strftime("%d")
RAW_PATH_MOVIES = f"Raw/Local/CSV/Movies/{year}/{month}/{day}/movies.csv"
RAW_PATH_SERIES = f"Raw/Local/CSV/Series/{year}/{month}/{day}/series.csv"

# Função para carregar credenciais explicitamente
def load_credentials():
    try:
        session = boto3.Session(profile_name=None)  # Usar o perfil padrão
        print("Credenciais carregadas do perfil padrão.")
    except ProfileNotFound:
        raise Exception("Não foi possível carregar credenciais do perfil padrão.")

# Função para upload de arquivos ao S3
def upload_to_s3(file_path, bucket, key):
    print(f"Tentando fazer upload do arquivo {file_path} para s3://{bucket}/{key}")
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket, key)
        print(f"Arquivo {file_path} enviado com sucesso para s3://{bucket}/{key}")
    except Exception as e:
        raise Exception(f"Erro ao enviar {file_path} para o S3: {e}")

# Função para verificar/criar bucket
def ensure_bucket_exists(bucket_name):
    print(f"Verificando se o bucket '{bucket_name}' existe...")
    s3_client = boto3.client('s3')
    try:
        # Verificar se o bucket existe
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' já existe.")
    except boto3.exceptions.botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"Bucket '{bucket_name}' não encontrado. Criando...")
            try:
                # Verificar a região e ajustar o LocationConstraint
                region = s3_client.meta.region_name
                if region == "us-east-1":
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={
                            'LocationConstraint': region
                        }
                    )
                print(f"Bucket '{bucket_name}' criado com sucesso.")
            except Exception as create_error:
                raise Exception(f"Erro ao criar o bucket: {create_error}")
        elif error_code == '403':
            print(f"Permissão negada para verificar o bucket '{bucket_name}'.")
            raise
        else:
            raise Exception(f"Erro ao verificar o bucket: {e}")

# Função para validar os arquivos locais
def validate_files(*file_paths):
    print("Validando a existência dos arquivos...")
    for file_path in file_paths:
        if not Path(file_path).is_file():
            print(f"Erro: Arquivo {file_path} não encontrado.")
            return False
    print("Todos os arquivos foram encontrados.")
    return True

# Função para leitura e validação de dados
def read_and_validate_csv(file_path):
    print(f"Tentando ler o arquivo {file_path} com pandas...")
    try:
        # Ler o arquivo CSV especificando o separador | e desativar "low_memory"
        df = pd.read_csv(file_path, sep="|", low_memory=False)
        print(f"Arquivo {file_path} carregado com sucesso. Total de registros: {len(df)}")
        return df
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return None

# Função principal
def main():
    print("Iniciando o script...")
    
    # Carregar credenciais explicitamente
    load_credentials()

    # Caminhos locais dos arquivos CSV
    local_movies_path = "data/movies.csv"
    local_series_path = "data/series.csv"

    # Validar se os arquivos existem
    if not validate_files(local_movies_path, local_series_path):
        print("Erro: Alguns arquivos não foram encontrados. Encerrando.")
        return

    # Ler os arquivos CSV e validar o conteúdo
    print("Lendo e validando os arquivos CSV...")
    movies_df = read_and_validate_csv(local_movies_path)
    series_df = read_and_validate_csv(local_series_path)

    # Caso algum arquivo não tenha sido lido, interrompe o processo
    if movies_df is None or series_df is None:
        print("Erro: Não foi possível ler os arquivos CSV. Upload interrompido.")
        return

    # Verificar e criar o bucket, se necessário
    ensure_bucket_exists(BUCKET_NAME)

    # Upload para o S3
    print("Iniciando upload para o S3...")
    success = True
    try:
        upload_to_s3(local_movies_path, BUCKET_NAME, RAW_PATH_MOVIES)
    except Exception as e:
        success = False
        print(f"Falha no upload de {local_movies_path}: {e}")
    
    try:
        upload_to_s3(local_series_path, BUCKET_NAME, RAW_PATH_SERIES)
    except Exception as e:
        success = False
        print(f"Falha no upload de {local_series_path}: {e}")

    if success:
        print("Upload concluído com sucesso!")
    else:
        print("Erro: Um ou mais uploads falharam. Verifique os logs acima.")

# Executar o script
if __name__ == "__main__":
    main()
```
<br/>

### 🐋 Criação do Dockerfile
As instruções do desafio solicitam a criação de um container para execução do script acima, com intenção de isolar os efeitos do ambiente local, garantindo possibilidade de replicar (via container) em qualquer máquina!

```dockerfile
# Usar imagem base completa do Python
FROM python:3.9

# Instalar dependências Python
RUN pip install --no-cache-dir pandas boto3

# Definir diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . /app

# Comando padrão para executar o script Python
CMD ["python", "script.py"]
```

*Obs: pensei em utilizar a imagem do Python 3.9 Slim, para otimizar ainda o espaço de armazenamento, mas conversando com o monitor Gilson, entendemos que os megabytes que economizaria, não seriam suficientemente relevantes - além de complexizar um pouco a instalação de bibliotecas. Segui com a versão normal, o Python 3.9.*

<br/>

### 🐚 Encapsulamento com Shell

Ao final improvisei criando um script Shell para encapsular uma execução de terminal que foi necessária, pra mim, por conta das credenciais de login da AWS, via SSO. 

Por algum motivo que não consegui ainda compreender, minhas chaves quando atualizadas ficam num "cache virtual" e não no arquivo de texto `credentials` e `config`. Para contornar, precisaria sempre executar o Docker (run) com mais alguns parâmetros. Para facilitar a execução, encapsulei!

```shell
#!/bin/bash

docker run \
  -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
  -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
  -e AWS_SESSION_TOKEN="$AWS_SESSION_TOKEN" \
  -v "$(pwd)/data:/app/data" \
  data-lake-uploader
```
<br/>

### 🤖 Criação do container e execução

Após os códigos criados, bastou a criação do container em si, e a sua execução através do Shell. O container ao ser executado, automaticamente executa o script Python. Ao verificarmos o bucket criado, os arquivos armazenados na estrutura de pastas sugerida nas instruções, concluí que atingi o ponto final neste desafio!

>Estrutura de pastas:
![estrutura para filmes](../evidencias/desafio/estrutura-movies.png)
![estrutura para series](../evidencias/desafio/estrutura-series.png)

<br/>

## 📌 Considerações finais sobre a Sprint 06

A Sprint 06 foi marcada pela integração entre várias tecnologias e pela construção de um pipeline completo de dados, desde a manipulação inicial de arquivos locais até o upload para o S3, com o uso de contêineres Docker para garantir a reprodutibilidade e consistência do ambiente de execução. Essa etapa foi fundamental para consolidar o aprendizado em Python, pandas e AWS, especialmente ao lidar com grandes volumes de dados e interagir diretamente com os serviços da nuvem, utilizando o `boto3`.

Além disso, foi uma oportunidade de aplicar conhecimentos adquiridos anteriormente, como a utilização de credenciais no AWS SSO e a automação do processo de execução do script em diferentes máquinas via Docker. A criação de uma estrutura eficiente de pastas e o uso de contêineres demonstraram a importância de um ambiente controlado e facilmente replicável, fundamental para garantir o sucesso no gerenciamento de dados em nuvem.

Estou satisfeito com o progresso realizado até aqui, tanto no desenvolvimento técnico quanto na compreensão do fluxo de trabalho. Esta sprint me preparou para os desafios seguintes e para aprofundar meu entendimento sobre pipelines de dados e integração com a AWS. Estou motivado para seguir adiante e continuar expandindo meus conhecimentos enquanto trabalho nas próximas etapas do projeto. 🚀