# Importando a biblioteca necessária do PySpark
from pyspark.sql import SparkSession

# Inicializando a SparkSession
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("pyspark-lab") \
    .getOrCreate()

# Carregando o arquivo names_aleatorios.txt no DataFrame
# Cada linha será tratada como um registro (sem cabeçalhos)
df_nomes = spark.read.text("names_aleatorios.txt")

# Renomeando a coluna padrão 'value' para 'nome'
df_nomes = df_nomes.withColumnRenamed("value", "nome")

# Mostrando as 5 primeiras linhas do DataFrame
df_nomes.show(5)

# Finalizando a SparkSession
spark.stop()
