import pandas as pd
import os

# Passo 1: Configuração inicial e leitura do arquivo
# Localizar o arquivo dinamicamente na pasta atual
current_dir = os.getcwd()  # Obtém o diretório atual
file_name = 'CAT202306.csv'  # Nome do arquivo CSV original
file_path = os.path.join(current_dir, file_name)  # Caminho completo para o arquivo

# Verificar se o arquivo existe
if not os.path.exists(file_path):
    raise FileNotFoundError(f"O arquivo {file_name} não foi encontrado no diretório atual.")

# Leitura do arquivo CSV
try:
    df = pd.read_csv(file_path, encoding='utf-8', sep=';')  # Lê o arquivo em um DataFrame
except Exception as e:
    raise Exception(f"Erro ao ler o arquivo CSV: {e}")

# Passo 2: Tratamentos necessários
# a) Substituir células em branco por NULL
print("Substituindo células em branco por NULL...")
df = df.fillna('NULL')

# b) Substituir valores '{ñ class}' e '{ñ Class}' por NULL
print("Substituindo '{ñ class}' e '{ñ Class}' por NULL...")
df = df.replace(to_replace=r'\{ñ class\}|\{ñ Class\}', value='NULL', regex=True)

# c) Eliminar espaços sobressalentes no início e fim de todas as células
print("Removendo espaços sobressalentes...")
df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

# d) Converter colunas de data para o formato brasileiro (DD/MM/YYYY)
print("Convertendo colunas de datas para formato datetime...")
date_columns = [
    'Data Acidente',  # Coluna 2
    'Data Afastamento',  # Coluna 21
    'Data Acidente.1',  # Coluna 22
    'Data Nascimento',  # Coluna 23
    'Data Acidente.2'  # Coluna 24
]

for col in date_columns:
    if col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')
        except Exception as e:
            print(f"Erro ao converter a coluna {col} para datetime: {e}")

# Passo 3: Adicionar coluna de idade no momento do acidente
print("Calculando idade no momento do acidente...")
if 'Data Nascimento' in df.columns and 'Data Acidente' in df.columns:
    df['Idade no momento do acidente'] = ((df['Data Acidente'] - df['Data Nascimento']).dt.days // 365).astype('Int64')
else:
    print("Colunas necessárias para cálculo de idade não encontradas.")

# Passo 4: Adicionar coluna com % da amostragem e coluna acima da média
print("Calculando % da amostragem e identificando acima da média...")
if 'Idade no momento do acidente' in df.columns:
    total_count = len(df)
    idade_counts = df['Idade no momento do acidente'].value_counts().reset_index()
    idade_counts.columns = ['Idade', 'Contagem']
    idade_counts['Relevancia estatistica % da idade na amostra'] = (idade_counts['Contagem'] / total_count * 100).round(2)
    media_percentual = idade_counts['Relevancia estatistica % da idade na amostra'].mean()
    idade_counts['Acima da Média %'] = idade_counts['Relevancia estatistica % da idade na amostra'] > media_percentual

    # Mapear os valores de % da amostragem e acima da média de volta para o DataFrame original
    df = df.merge(idade_counts[['Idade', 'Relevancia estatistica % da idade na amostra', 'Acima da Média %']], how='left', left_on='Idade no momento do acidente', right_on='Idade')
    df.drop(columns=['Idade'], inplace=True)
else:
    print("Coluna 'Idade no momento do acidente' não encontrada.")

# Passo 5: Adicionar coluna com % do CBO na amostra
print("Calculando relevância estatística % do CBO na amostra...")
if 'CBO' in df.columns:
    cbo_counts = df['CBO'].value_counts().reset_index()
    cbo_counts.columns = ['CBO', 'Contagem']
    cbo_counts['Relevancia estatistica % do CBO na amostra'] = (cbo_counts['Contagem'] / total_count * 100).round(2)

    # Mapear os valores de % do CBO de volta para o DataFrame original
    df = df.merge(cbo_counts[['CBO', 'Relevancia estatistica % do CBO na amostra']], how='left', on='CBO')
else:
    print("Coluna 'CBO' não encontrada.")

# Passo 6: Salvar o arquivo tratado
output_file_name = 'CAT202306-tratado.csv'
output_file_path = os.path.join(current_dir, output_file_name)

print(f"Salvando o arquivo tratado como {output_file_name}...")
try:
    df.to_csv(output_file_path, index=False, sep=';', encoding='utf-8')
    print(f"Arquivo tratado salvo com sucesso em: {output_file_path}")
except Exception as e:
    raise Exception(f"Erro ao salvar o arquivo tratado: {e}")

# Passo 7: Aplicar filtros para gerar o arquivo filtrado
print("Aplicando filtros para gerar o arquivo filtrado...")
if 'CBO' in df.columns and 'Acima da Média %' in df.columns and 'Relevancia estatistica % do CBO na amostra' in df.columns:
    # a) Filtrar CBO inválidos (NULL, branco ou 0)
    df_filtered = df[(df['CBO'] != 'NULL') & (df['CBO'] != '') & (df['CBO'] != '0')]

    # b) Apenas valores TRUE na coluna 'Acima da Média %'
    df_filtered = df_filtered[df_filtered['Acima da Média %'] == True]

    # Identificar os 10 CBOs com maiores valores de relevância
    top_cbo_counts = df_filtered[['CBO', 'Relevancia estatistica % do CBO na amostra']].drop_duplicates()
    top_cbo_counts = top_cbo_counts.sort_values(by='Relevancia estatistica % do CBO na amostra', ascending=False).head(10)
    top_cbo_labels = top_cbo_counts['CBO']
    df_filtered = df_filtered[df_filtered['CBO'].isin(top_cbo_labels)]

    # Salvar o arquivo filtrado
    output_filtered_file_name = 'CAT202306-filtrado.csv'
    output_filtered_file_path = os.path.join(current_dir, output_filtered_file_name)
    print(f"Salvando o arquivo filtrado como {output_filtered_file_name}...")
    try:
        df_filtered.to_csv(output_filtered_file_path, index=False, sep=';', encoding='utf-8')
        print(f"Arquivo filtrado salvo com sucesso em: {output_filtered_file_path}")
    except Exception as e:
        raise Exception(f"Erro ao salvar o arquivo filtrado: {e}")
else:
    print("Colunas necessárias para filtragem não encontradas.")

# Passo 8: Gerar indicadores
print("Gerando indicadores...")
if not df_filtered.empty:
    # a) Distribuição por sexo
    sexo_dist = df_filtered['Sexo'].value_counts(normalize=True).reset_index()
    sexo_dist.columns = ['Sexo', '% Distribuição']
    sexo_dist['% Distribuição'] = (sexo_dist['% Distribuição'] * 100).round(2)

    # b) Indicadores por sexo e CBO
    def percent_no_sexo(group):
        total_sexo = len(df_filtered[df_filtered['Sexo'] == group.name[0]])
        return (len(group) / total_sexo) * 100 if total_sexo > 0 else 0

    cbo_sexo_stats = df_filtered.groupby(['Sexo', 'CBO']).agg(
        Contagem=('CBO', 'count'),
        Idade_Máxima=('Idade no momento do acidente', 'max'),
        Idade_Mínima=('Idade no momento do acidente', 'min'),
        Idade_Média=('Idade no momento do acidente', 'mean')
    ).reset_index()

    # Calcular o percentual dentro do sexo manualmente
    cbo_sexo_stats['% no Sexo'] = cbo_sexo_stats.apply(
        lambda row: (row['Contagem'] / len(df_filtered[df_filtered['Sexo'] == row['Sexo']])) * 100, axis=1
    )

    cbo_sexo_stats['% no Sexo'] = cbo_sexo_stats['% no Sexo'].round(2)
    cbo_sexo_stats['Idade_Média'] = cbo_sexo_stats['Idade_Média'].round(2)

    # c) Identificar CBOs com óbito registrado
    if 'Indica Óbito Acidente' in df_filtered.columns:
        cbo_obitos = df_filtered[df_filtered['Indica Óbito Acidente'] == 'Sim']['CBO'].unique()
        cbo_obitos_df = pd.DataFrame({'CBO com Óbito Registrado': cbo_obitos})
    else:
        cbo_obitos_df = pd.DataFrame({'CBO com Óbito Registrado': []})

    # Consolidar indicadores em um único DataFrame para exportação
    indicadores = {
        'Distribuição por Sexo': sexo_dist,
        'Estatísticas por Sexo e CBO': cbo_sexo_stats,
        'CBOs com Óbito Registrado': cbo_obitos_df
    }

    # Salvar cada indicador como abas em um único arquivo Excel
    output_indicadores_file_name = 'CAT202306-indicadores.xlsx'
    with pd.ExcelWriter(output_indicadores_file_name) as writer:
        for sheet_name, data in indicadores.items():
            data.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Arquivo de indicadores salvo como {output_indicadores_file_name}")
else:
    print("O DataFrame filtrado está vazio, nenhum indicador foi gerado.")