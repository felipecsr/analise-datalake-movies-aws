# Importando as bibliotecas necessárias
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Configurando a seed para garantir reprodutibilidade
SEED = 42

# Inicializando a SparkSession
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Laboratório Etapa 5 - Corrigido") \
    .getOrCreate()

# Carregando o arquivo names_aleatorios.txt no DataFrame
df_nomes = spark.read.text("names_aleatorios.txt").withColumnRenamed("value", "nome")

# Lista de valores possíveis para 'escolaridade'
opcoes_escolaridade = ["Fundamental", "Médio", "Superior"]

# Adicionando a coluna 'escolaridade' de forma totalmente aleatória baseada no seed
df_nomes = df_nomes.withColumn(
    "escolaridade",
    expr(f"CASE CAST(rand({SEED}) * {len(opcoes_escolaridade)} AS INT) " +
         f"WHEN 0 THEN '{opcoes_escolaridade[0]}' " +
         f"WHEN 1 THEN '{opcoes_escolaridade[1]}' " +
         f"ELSE '{opcoes_escolaridade[2]}' END")
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

# Adicionando a coluna 'ano_nascimento' com valores pseudoaleatórios entre 1945 e 2010
df_nomes = df_nomes.withColumn(
    "ano_nascimento",
    expr(f"CAST(1945 + FLOOR(rand({SEED}) * 66) AS INT)")
)

# Mostrando as 10 primeiras linhas do DataFrame
print("Exibindo as 10 primeiras linhas com as novas colunas:")
df_nomes.show(10)

# Finalizando a SparkSession
spark.stop()
