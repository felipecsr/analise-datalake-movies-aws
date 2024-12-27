import subprocess
import os

def download_jsons_from_s3(bucket_path, local_dir='.'):
    """
    Faz o download de todos os arquivos JSON de um caminho específico em um bucket S3.
    
    :param bucket_path: Caminho completo no S3 (ex.: s3://bucket-name/path/to/files/).
    :param local_dir: Diretório local onde os arquivos serão salvos (padrão: diretório atual).
    """
    try:
        # Verifica se o diretório local existe
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        # Comando AWS CLI para sincronizar arquivos JSON
        command = [
            "aws", "s3", "sync", bucket_path, local_dir, "--exclude", "*", "--include", "*.json"
        ]

        # Executa o comando
        subprocess.run(command, check=True)
        print(f"Arquivos JSON baixados com sucesso para o diretório: {os.path.abspath(local_dir)}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando AWS CLI: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    # Caminho do bucket no S3
    s3_bucket_path = "s3://desafio-filmes-series/Raw/TMDB/JSON/Movies/2024/12/27/"
    
    # Diretório local onde os arquivos serão salvos
    local_directory = "."  # Padrão: diretório atual

    download_jsons_from_s3(s3_bucket_path, local_directory)
