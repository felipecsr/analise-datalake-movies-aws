# Importando as bibliotecas necessárias
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Configurando a seed para garantir reprodutibilidade
SEED = 42

# Inicializando a SparkSession
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Laboratório Etapa 3 - Aleatório") \
    .getOrCreate()

# Carregando o arquivo names_aleatorios.txt no DataFrame
df_nomes = spark.read.text("names_aleatorios.txt").withColumnRenamed("value", "nome")

# Lista de valores possíveis para 'escolaridade'
opcoes_escolaridade = ["Fundamental", "Médio", "Superior"]

# Adicionando a coluna 'escolaridade' de forma totalmente aleatória com base no seed
df_nomes = df_nomes.withColumn(
    "escolaridade",
    expr(f"CASE CAST(rand({SEED}) * {len(opcoes_escolaridade)} AS INT) " +
         f"WHEN 0 THEN '{opcoes_escolaridade[0]}' " +
         f"WHEN 1 THEN '{opcoes_escolaridade[1]}' " +
         f"ELSE '{opcoes_escolaridade[2]}' END")
)

# Mostrando as 10 primeiras linhas do DataFrame
print("Exibindo as 10 primeiras linhas com 'escolaridade' aleatória:")
df_nomes.show(10)

# Finalizando a SparkSession
spark.stop()
