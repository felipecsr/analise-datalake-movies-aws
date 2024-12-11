import json
import pandas as pd
import boto3

def lambda_handler(event, context):
    # Inicializa o cliente S3
    s3_client = boto3.client('s3')
    
    # Nome do bucket e arquivo no S3
    bucket_name = 'bucket-exercicio-sprint05'
    s3_file_name = 'dados/nomes.csv'
    
    try:
        # Debug: Mensagem para identificar progresso
        print(f"Tentando acessar o arquivo {s3_file_name} no bucket {bucket_name}")
        
        # Obtém o objeto do S3
        objeto = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)
        
        # Lê o arquivo CSV
        df = pd.read_csv(objeto['Body'], sep=',')
        rows = len(df)
        
        # Retorna o número de linhas
        return {
            'statusCode': 200,
            'body': f"Este arquivo tem {rows} linhas."
        }
    
    except Exception as e:
        # Retorna um erro em caso de falha
        print(f"Erro ao processar: {e}")
        return {
            'statusCode': 500,
            'body': f"Erro ao processar o arquivo: {str(e)}"
        }
