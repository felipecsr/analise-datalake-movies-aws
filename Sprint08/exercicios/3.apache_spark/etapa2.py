# Importando a biblioteca necessária do PySpark
from pyspark.sql import SparkSession

# Inicializando a SparkSession
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Laboratório Etapa 2") \
    .getOrCreate()

# Carregando o arquivo nomes_aleatorios.txt no DataFrame
# Certifique-se de que o arquivo está na mesma pasta do script
df_nomes = spark.read.text("names_aleatorios.txt")

# Renomeando a coluna padrão 'value' para 'nome'
df_nomes = df_nomes.withColumnRenamed("value", "nome")

# Mostrando as 10 primeiras linhas do DataFrame
print("Exibindo as 10 primeiras linhas:")
df_nomes.show(10)

# Finalizando a SparkSession
spark.stop()
