# Importando as bibliotecas necessárias
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Configurando a seed para garantir reprodutibilidade
SEED = 42

# Inicializando a SparkSession
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Laboratório Etapa 4 - Corrigido") \
    .getOrCreate()

# Carregando o arquivo names_aleatorios.txt no DataFrame
df_nomes = spark.read.text("names_aleatorios.txt").withColumnRenamed("value", "nome")

# Adicionando a coluna 'escolaridade' de forma aleatória baseada no seed
df_nomes = df_nomes.withColumn(
    "escolaridade",
    expr(f"CASE CAST(rand({SEED}) * 3 AS INT) " +
         "WHEN 0 THEN 'Fundamental' " +
         "WHEN 1 THEN 'Médio' " +
         "ELSE 'Superior' END")
)

# Lista de países fornecida
paises = [
    "Argentina", "Bolívia", "Brasil", "Chile", "Colômbia",
    "Equador", "Guiana", "Paraguai", "Peru", "Suriname",
    "Uruguai", "Venezuela", "Guiana Francesa"
]

# Adicionando a coluna 'país' de forma aleatória baseada no seed
df_nomes = df_nomes.withColumn(
    "país",
    expr(f"CASE MOD(CAST(rand({SEED}) * {len(paises)} AS INT), {len(paises)}) " +
         "WHEN 0 THEN 'Argentina' WHEN 1 THEN 'Bolívia' WHEN 2 THEN 'Brasil' " +
         "WHEN 3 THEN 'Chile' WHEN 4 THEN 'Colômbia' WHEN 5 THEN 'Equador' " +
         "WHEN 6 THEN 'Guiana' WHEN 7 THEN 'Paraguai' WHEN 8 THEN 'Peru' " +
         "WHEN 9 THEN 'Suriname' WHEN 10 THEN 'Uruguai' WHEN 11 THEN 'Venezuela' " +
         "ELSE 'Guiana Francesa' END")
)

# Mostrando as 10 primeiras linhas do DataFrame
print("Exibindo as 10 primeiras linhas com as novas colunas:")
df_nomes.show(10)

# Finalizando a SparkSession
spark.stop()
