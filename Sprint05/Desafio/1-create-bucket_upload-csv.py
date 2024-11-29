import boto3
from botocore.exceptions import ClientError

# Criando cliente S3
s3 = boto3.client('s3', region_name='us-east-1')  # Usando a região US East (N. Virginia)

# Nome do bucket
bucket_name = 'bucket-desafio-sprint05'

# Caminho local do arquivo a ser enviado
csv_file_path = 'CAT202306.csv'  # Caminho local do arquivo

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

# Função para fazer o upload de um arquivo para o bucket
def upload_file_to_s3(local_file_path, bucket_name, s3_key, content_type=None):
    try:
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type  # Define o tipo MIME para o arquivo
        s3.upload_file(local_file_path, bucket_name, s3_key, ExtraArgs=extra_args)
        print(f"Arquivo '{local_file_path}' enviado com sucesso para '{bucket_name}/{s3_key}'!")
    except ClientError as e:
        print(f"Erro ao enviar o arquivo {local_file_path} para o S3: {e}")

# Função principal para criar o bucket e realizar upload
def main():
    # Criar o bucket
    create_bucket(bucket_name)

    # Upload do arquivo CSV
    upload_file_to_s3(csv_file_path, bucket_name, 'CAT202306.csv', content_type='text/csv')

if __name__ == '__main__':
    main()
