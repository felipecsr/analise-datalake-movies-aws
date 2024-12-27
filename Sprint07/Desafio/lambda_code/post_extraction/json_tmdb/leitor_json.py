import os
import json
import pandas as pd

def process_json_files(directory):
    # Lista todos os arquivos JSON no diretório
    json_files = [file for file in os.listdir(directory) if file.endswith('.json')]

    # Lista para armazenar os dataframes
    dataframes = []

    # Dicionário para armazenar a contagem de registros por arquivo
    records_count_per_file = {}

    # Processa cada arquivo JSON
    for json_file in json_files:
        file_path = os.path.join(directory, json_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Converte os dados para um DataFrame
        df = pd.DataFrame(data)
        
        # Adiciona uma coluna indicando a origem dos dados
        df['source_file'] = json_file

        # Adiciona uma coluna de gênero com base no nome do arquivo
        if '80' in json_file:
            df['genre'] = 'Crime'
        elif '10752' in json_file:
            df['genre'] = 'War'
        else:
            df['genre'] = 'Unknown'
        
        # Armazena o DataFrame na lista
        dataframes.append(df)

        # Conta o número de registros no arquivo
        records_count_per_file[json_file] = len(df)

    # Concatena todos os DataFrames
    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df, records_count_per_file

def main():
    # Diretório onde estão os arquivos JSON
    directory = '.'  # Pode ser alterado conforme necessário

    # Processa os arquivos JSON
    combined_df, records_count_per_file = process_json_files(directory)

    # Exibe a contagem de registros por arquivo
    print("\nQuantidade de registros por arquivo JSON:")
    for file, count in records_count_per_file.items():
        print(f"{file}: {count} registros")

    # Filtra os filmes por gênero e faz as contagens
    total_war_movies = combined_df[combined_df['genre'] == 'War'].shape[0]
    total_crime_movies = combined_df[combined_df['genre'] == 'Crime'].shape[0]
    total_movies = combined_df.shape[0]

    # Exibe os resultados
    print("\nResumo dos filmes:")
    print(f"Total de filmes de guerra: {total_war_movies}")
    print(f"Total de filmes de crimes: {total_crime_movies}")
    print(f"Total geral de filmes: {total_movies}")

if __name__ == "__main__":
    main()
