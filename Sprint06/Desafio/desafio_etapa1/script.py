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
