# Importando as bibliotecas necessárias
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Configurando a seed para garantir reprodutibilidade
SEED = 42

# Inicializando a SparkSession
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Laboratório Etapa 7 - SQL com LIMIT") \
    .getOrCreate()

# Carregando o arquivo names_aleatorios.txt no DataFrame
df_nomes = spark.read.text("names_aleatorios.txt").withColumnRenamed("value", "nome")

# Adicionando a coluna 'escolaridade' com valores pseudoaleatórios baseados no seed
df_nomes = df_nomes.withColumn(
    "escolaridade",
    expr(f"CASE WHEN rand({SEED}) < 0.33 THEN 'Fundamental' " +
         f"WHEN rand({SEED}) < 0.66 THEN 'Médio' ELSE 'Superior' END")
)

# Adicionando a coluna 'país' com valores pseudoaleatórios baseados no seed
paises = [
    "Argentina", "Bolívia", "Brasil", "Chile", "Colômbia",
    "Equador", "Guiana", "Paraguai", "Peru", "Suriname",
    "Uruguai", "Venezuela", "Guiana Francesa"
]
df_nomes = df_nomes.withColumn(
    "país",
    expr(f"CASE MOD(CAST(rand({SEED}) * {len(paises)} AS INT), {len(paises)}) " +
         "WHEN 0 THEN 'Argentina' WHEN 1 THEN 'Bolívia' WHEN 2 THEN 'Brasil' " +
         "WHEN 3 THEN 'Chile' WHEN 4 THEN 'Colômbia' WHEN 5 THEN 'Equador' " +
         "WHEN 6 THEN 'Guiana' WHEN 7 THEN 'Paraguai' WHEN 8 THEN 'Peru' " +
         "WHEN 9 THEN 'Suriname' WHEN 10 THEN 'Uruguai' WHEN 11 THEN 'Venezuela' " +
         "ELSE 'Guiana Francesa' END")
)

# Adicionando a coluna 'ano_nascimento' com valores pseudoaleatórios baseados no seed
df_nomes = df_nomes.withColumn(
    "ano_nascimento",
    expr(f"CAST(1945 + FLOOR(rand({SEED}) * 66) AS INT)")
)

# Registrando o DataFrame como uma tabela temporária
df_nomes.createOrReplaceTempView("nomes")

# Aplicando o filtro utilizando Spark SQL e limitando os resultados
df_nascidos_2000_sql = spark.sql("""
    SELECT *
    FROM nomes
    WHERE ano_nascimento >= 2000
    LIMIT 10
""")

# Exibindo as 10 linhas retornadas pela consulta SQL
print("Exibindo as 10 primeiras linhas filtradas (usando Spark SQL com LIMIT):")
df_nascidos_2000_sql.show()

# Finalizando a SparkSession
spark.stop()
