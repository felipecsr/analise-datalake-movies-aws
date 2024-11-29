import boto3
import json
from botocore.exceptions import ClientError

# Criando cliente S3
s3 = boto3.client('s3', region_name='us-east-1')

# Nome do bucket e arquivos a serem carregados
bucket_name = 'bucket-exercicio-sprint05'
index_document = 'index.html'
error_document = '404.html'
index_file_path = 'index.html'
csv_file_path = 'nomes.csv'
error_file_path = '404.html'

# Função para criar o bucket
def create_bucket(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
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

# Função para desabilitar o bloqueio de acesso público
def disable_public_access_block(bucket_name):
    try:
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        print(f"Bloqueio de acesso público desabilitado para o bucket '{bucket_name}'!")
    except ClientError as e:
        print(f"Erro ao desabilitar o bloqueio de acesso público: {e}")

# Função para configurar a política de acesso público
def set_bucket_policy(bucket_name):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
            }
        ]
    }
    try:
        policy_json = json.dumps(policy)
        s3.put_bucket_policy(Bucket=bucket_name, Policy=policy_json)
        print(f"Política de acesso público configurada para o bucket '{bucket_name}'!")
    except ClientError as e:
        print(f"Erro ao configurar a política de bucket: {e}")

# Função para fazer o upload de um arquivo para o bucket
def upload_file_to_s3(local_file_path, bucket_name, s3_key, content_type=None):
    try:
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type
        s3.upload_file(local_file_path, bucket_name, s3_key, ExtraArgs=extra_args)
        print(f"Arquivo '{local_file_path}' enviado com sucesso para '{bucket_name}/{s3_key}'!")
    except ClientError as e:
        print(f"Erro ao enviar o arquivo {local_file_path} para o S3: {e}")

# Função para realizar o upload de arquivos
def upload_files():
    upload_file_to_s3(index_file_path, bucket_name, 'index.html', content_type='text/html')
    upload_file_to_s3(csv_file_path, bucket_name, 'dados/nomes.csv', content_type='text/csv')
    upload_file_to_s3(error_file_path, bucket_name, '404.html', content_type='text/html')

# Função principal
def main():
    create_bucket(bucket_name)
    enable_static_website(bucket_name, index_document, error_document)
    disable_public_access_block(bucket_name)
    set_bucket_policy(bucket_name)
    upload_files()

if __name__ == '__main__':
    main()
