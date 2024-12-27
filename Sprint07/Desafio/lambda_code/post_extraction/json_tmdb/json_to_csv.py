import os
import json
import pandas as pd

def process_json_files(directory):
    # Lista todos os arquivos JSON no diretório
    json_files = [file for file in os.listdir(directory) if file.endswith('.json')]

    # Lista para armazenar os dataframes
    dataframes = []

    # Processa cada arquivo JSON
    for json_file in json_files:
        file_path = os.path.join(directory, json_file)

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Converte os dados para um DataFrame, garantindo a normalização completa
        df = pd.json_normalize(data)

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

    # Concatena todos os DataFrames
    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df

def main():
    # Diretório onde estão os arquivos JSON
    directory = '.'  # Diretório atual

    # Processa os arquivos JSON
    combined_df = process_json_files(directory)

    # Salva o DataFrame combinado em um arquivo CSV com separador '|'
    output_file = 'combined_data.csv'
    combined_df.to_csv(output_file, sep='|', index=False, encoding='utf-8')

    print(f"Arquivo CSV gerado: {output_file}")

if __name__ == "__main__":
    main()
