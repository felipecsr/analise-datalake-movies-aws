import os
import glob
import shutil
from pyspark.sql import SparkSession

# 1. Inicializar a SparkSession
spark = SparkSession.builder \
    .appName("Word Count Exercise") \
    .master("local[*]") \
    .getOrCreate()

# 2. Definir o caminho absoluto do arquivo README.md
file_path = "/home/jovyan/work/README.md"

# 3. Carregar o arquivo README.md como RDD
rdd = spark.sparkContext.textFile(file_path)

# 4. Contar as palavras no arquivo (preservando a ordem de primeira aparição)
word_counts_with_order = (rdd.flatMap(lambda line: line.split())    # Quebra linhas em palavras
                              .zipWithIndex()                      # Associa cada palavra a seu índice global
                              .map(lambda word_idx: (word_idx[0], (1, word_idx[1])))  # Formato (palavra, (1, índice))
                              .reduceByKey(lambda acc, val: (acc[0] + val[0], min(acc[1], val[1])))  # Soma contagens, mantém o menor índice
                              .sortBy(lambda word_idx: word_idx[1][1])  # Ordena pelo índice de aparição
                              .map(lambda word_idx: (word_idx[0], word_idx[1][0])))  # Resultado final: (palavra, contagem)

# 5. Converter para DataFrame
word_counts_df = word_counts_with_order.toDF(["word", "count"])

# 6. Salvar como CSV em uma única partição
temp_output_path = "/home/jovyan/work/results/temp_word_counts"
word_counts_df.coalesce(1).write.csv(temp_output_path, header=True, mode="overwrite")

# 7. Renomear o arquivo CSV gerado para um nome mais intuitivo
csv_part_file = glob.glob(temp_output_path + "/part-*.csv")[0]  # Busca o arquivo CSV na pasta
final_csv_file = "/home/jovyan/work/results/word_counts_final.csv"

shutil.move(csv_part_file, final_csv_file)  # Renomeia o arquivo
shutil.rmtree(temp_output_path)  # Remove a pasta temporária

print(f"Contagem de palavras concluída e salva como um único arquivo CSV em {final_csv_file}")
