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
