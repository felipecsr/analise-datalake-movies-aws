import pandas as pd
import boto3
from botocore.exceptions import ClientError

# Configuração inicial
bucket_name = 'bucket-desafio-sprint05'  # Nome do bucket
input_file_key = 'CAT202306.csv'         # Caminho do arquivo dentro do bucket
output_dir = 'outputs/'                  # Diretório de saída dentro do bucket

# Criando cliente S3
s3 = boto3.client('s3', region_name='us-east-1')

# Passo 1: Leitura do arquivo CSV diretamente do S3
print(f"Lendo o arquivo '{input_file_key}' diretamente do bucket '{bucket_name}'...")
try:
    response = s3.get_object(Bucket=bucket_name, Key=input_file_key)
    print("Criando Dataframe...")
    df = pd.read_csv(response['Body'], encoding='utf-8', sep=';')
    print("> Dataframe criado")
except ClientError as e:
    raise Exception(f"Erro ao obter o arquivo do S3: {e}")
except Exception as e:
    raise Exception(f"Erro ao ler o arquivo CSV: {e}")

# Passo 2: Tratamentos necessários
print("\n>>> Realizando tratamentos:")
# a) Substituir células em branco por NULL
print("1) Substituindo células em branco por NULL")
df = df.fillna('NULL')

# b) Substituir valores '{ñ class}' e '{ñ Class}' por NULL
print("2) Substituindo '{ñ class}' e '{ñ Class}' por NULL")
df = df.replace(to_replace=r'\{ñ class\}|\{ñ Class\}', value='NULL', regex=True)

# c) Eliminar espaços sobressalentes no início e fim de todas as células
print("3) Removendo espaços sobressalentes")
df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

# d) Converter colunas de data para o formato brasileiro
print("4) Convertendo colunas de datas para formato datetime")
date_columns = ['Data Acidente', 'Data Afastamento', 'Data Acidente.1', 'Data Nascimento', 'Data Acidente.2']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')

# Passo 3: Adicionar coluna de idade no momento do acidente
print("\n>>> Realizando processamentos:")
if 'Data Nascimento' in df.columns and 'Data Acidente' in df.columns:
    print("1) Calculando idade no momento do acidente")
    df['Idade no momento do acidente'] = ((df['Data Acidente'] - df['Data Nascimento']).dt.days // 365).astype('Int64')

# Passo 4: Adicionar coluna com % da amostragem e coluna acima da média
if 'Idade no momento do acidente' in df.columns:
    print("2) Adicionando % da amostragem e identificando acima da média")
    total_count = len(df)
    idade_counts = df['Idade no momento do acidente'].value_counts().reset_index()
    idade_counts.columns = ['Idade', 'Contagem']
    idade_counts['Relevancia estatistica % da idade na amostra'] = (idade_counts['Contagem'] / total_count * 100).round(2)
    media_percentual = idade_counts['Relevancia estatistica % da idade na amostra'].mean()
    idade_counts['Acima da Média %'] = idade_counts['Relevancia estatistica % da idade na amostra'] > media_percentual
    df = df.merge(idade_counts[['Idade', 'Relevancia estatistica % da idade na amostra', 'Acima da Média %']], how='left', left_on='Idade no momento do acidente', right_on='Idade')
    df.drop(columns=['Idade'], inplace=True)

# Passo 5: Adicionar coluna com % do CBO na amostra
if 'CBO' in df.columns:
    print("3) Calculando relevância estatística % do CBO na amostra")
    cbo_counts = df['CBO'].value_counts().reset_index()
    cbo_counts.columns = ['CBO', 'Contagem']
    cbo_counts['Relevancia estatistica % do CBO na amostra'] = (cbo_counts['Contagem'] / total_count * 100).round(2)
    df = df.merge(cbo_counts[['CBO', 'Relevancia estatistica % do CBO na amostra']], how='left', on='CBO')

# Passo 6: Salvar o arquivo tratado para o bucket
output_treated_key = f'{output_dir}CAT202306-tratado.csv'
try:
    treated_csv = df.to_csv(index=False, sep=';', encoding='utf-8')
    s3.put_object(Bucket=bucket_name, Key=output_treated_key, Body=treated_csv)
    print(f"> Arquivo tratado e processado, enviado para o bucket em: {output_treated_key}")
except ClientError as e:
    raise Exception(f"Erro ao salvar o arquivo tratado no S3: {e}")

# Passo 7: Aplicar filtros e gerar o arquivo filtrado
print("\n>>> Realizando filtragens dos dados:")
if 'CBO' in df.columns and 'Acima da Média %' in df.columns:
    print("1) Filtrando CBO inválidos")
    df_filtered = df[(df['CBO'] != 'NULL') & (df['CBO'] != '') & (df['CBO'] != '0')]
    print("2) Mantendo apenas valores acima da média")
    df_filtered = df_filtered[df_filtered['Acima da Média %'] == True]
    print("3) Identificando os 10 principais CBOs")
    top_cbo_counts = df_filtered[['CBO', 'Relevancia estatistica % do CBO na amostra']].drop_duplicates()
    top_cbo_counts = top_cbo_counts.sort_values(by='Relevancia estatistica % do CBO na amostra', ascending=False).head(10)
    top_cbo_labels = top_cbo_counts['CBO']
    df_filtered = df_filtered[df_filtered['CBO'].isin(top_cbo_labels)]
    output_filtered_key = f'{output_dir}CAT202306-filtrado.csv'
    try:
        filtered_csv = df_filtered.to_csv(index=False, sep=';', encoding='utf-8')
        s3.put_object(Bucket=bucket_name, Key=output_filtered_key, Body=filtered_csv)
        print(f"> Arquivo filtrado enviado para o bucket em: {output_filtered_key}")
    except ClientError as e:
        raise Exception(f"Erro ao salvar o arquivo filtrado no S3: {e}")

# Passo 8: Gerar indicadores e salvar no bucket
print("\n>>> Realizando análises e criando indicadores:")
if not df_filtered.empty:
    print("1) Calculando distribuição por sexo")
    sexo_dist = df_filtered['Sexo'].value_counts(normalize=True).reset_index()
    sexo_dist.columns = ['Sexo', '% Distribuição']
    sexo_dist['% Distribuição'] = (sexo_dist['% Distribuição'] * 100).round(2)

    print("2) Gerando estatísticas por sexo e CBO")
    cbo_sexo_stats = df_filtered.groupby(['Sexo', 'CBO']).agg(
        Contagem=('CBO', 'count'),
        Idade_Máxima=('Idade no momento do acidente', 'max'),
        Idade_Mínima=('Idade no momento do acidente', 'min'),
        Idade_Média=('Idade no momento do acidente', 'mean')
    ).reset_index()
    cbo_sexo_stats['Idade_Média'] = cbo_sexo_stats['Idade_Média'].round(2)

    indicadores = {
        'Distribuição por Sexo': sexo_dist,
        'Estatísticas por Sexo e CBO': cbo_sexo_stats
    }
    output_indicators_key = f'{output_dir}CAT202306-indicadores.xlsx'
    try:
        with pd.ExcelWriter('/tmp/indicadores.xlsx') as writer:
            for sheet_name, data in indicadores.items():
                data.to_excel(writer, sheet_name=sheet_name, index=False)
        with open('/tmp/indicadores.xlsx', 'rb') as f:
            s3.put_object(Bucket=bucket_name, Key=output_indicators_key, Body=f)
        print(f"> Arquivo de indicadores enviado para o bucket em: {output_indicators_key}")
    except ClientError as e:
        raise Exception(f"Erro ao salvar o arquivo de indicadores no S3: {e}")
