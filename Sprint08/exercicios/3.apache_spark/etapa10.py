# Importando as bibliotecas necessárias
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Configurando a seed para garantir reprodutibilidade
SEED = 42

# Inicializando a SparkSession
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Laboratório Etapa 10 - Pessoas por País e Geração") \
    .getOrCreate()

# Carregando o arquivo names_aleatorios.txt no DataFrame
df_nomes = spark.read.text("names_aleatorios.txt").withColumnRenamed("value", "nome")

# Lista de países fornecida
paises = [
    "Argentina", "Bolívia", "Brasil", "Chile", "Colômbia",
    "Equador", "Guiana", "Paraguai", "Peru", "Suriname",
    "Uruguai", "Venezuela", "Guiana Francesa"
]

# Adicionando a coluna 'pais' de forma aleatória baseada no seed
df_nomes = df_nomes.withColumn(
    "pais",
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

# Adicionando a coluna 'geracao' com base no ano de nascimento
df_nomes = df_nomes.withColumn(
    "geracao",
    expr("""
        CASE
            WHEN ano_nascimento BETWEEN 1945 AND 1964 THEN 'Baby Boomers'
            WHEN ano_nascimento BETWEEN 1965 AND 1979 THEN 'Geracao X'
            WHEN ano_nascimento BETWEEN 1980 AND 1994 THEN 'Millennials'
            ELSE 'Geracao Z'
        END
    """)
)

# Registrando o DataFrame como uma tabela temporária
df_nomes.createOrReplaceTempView("nomes")

# Consultando o número de pessoas por pais e geracao usando Spark SQL
resultado = spark.sql("""
    SELECT pais, geracao, COUNT(*) AS total
    FROM nomes
    GROUP BY pais, geracao
    ORDER BY pais ASC, geracao ASC, total ASC
""")

# Contando o número total de linhas no resultado
num_linhas = resultado.count()

# Exibindo todos os resultados
print(f"Exibindo todas as combinações de países e gerações (total de {num_linhas} linhas):")
resultado.show(num_linhas, truncate=False)

# Finalizando a SparkSession
spark.stop()
