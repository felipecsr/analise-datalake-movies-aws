import boto3
from botocore.exceptions import ClientError

# Criando cliente S3
s3 = boto3.client('s3', region_name='us-east-1')  # Usando a região US East (N. Virginia)

# Nome do bucket que será criado
bucket_name = 'bucket1-sprint05'  
index_document = 'index.html'
error_document = '404.html'

# Função para criar o bucket
def create_bucket(bucket_name):
    try:
        # Criar o bucket sem o LocationConstraint para us-east-1
        s3.create_bucket(
            Bucket=bucket_name
        )
        print(f"Bucket '{bucket_name}' criado com sucesso!")
    except ClientError as e:
        print(f"Erro ao criar o bucket: {e}")

# Função para habilitar hospedagem de site estático
def enable_static_website(bucket_name, index_document, error_document):
    try:
        s3.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'IndexDocument': {'Suffix': index_document},
                'ErrorDocument': {'Key': error_document}
            }
        )
        print(f"Hospedagem de site estático habilitada para o bucket '{bucket_name}'!")
    except ClientError as e:
        print(f"Erro ao configurar a hospedagem de site estático: {e}")

# Função principal para criar o bucket e configurar a hospedagem
def main():
    # Criar o bucket
    create_bucket(bucket_name)
    
    # Habilitar a hospedagem de site estático
    enable_static_website(bucket_name, index_document, error_document)

if __name__ == '__main__':
    main()
