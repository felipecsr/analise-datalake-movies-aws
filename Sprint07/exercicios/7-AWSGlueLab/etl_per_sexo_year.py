import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import upper

## @params: [JOB_NAME, S3_INPUT_PATH, S3_TARGET_PATH]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_file = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH']

# Definir o schema do arquivo CSV
schema = StructType([
    StructField("nome", StringType(), True),
    StructField("sexo", StringType(), True),  # Letra única
    StructField("total", IntegerType(), True),
    StructField("ano", IntegerType(), True)  # Ano como inteiro
])

# Ler o arquivo CSV com o schema definido
df = spark.read.csv(source_file, schema=schema, header=True)

# 1. Imprimir o schema do DataFrame
print("[INFO] Schema do DataFrame lido:")
df.printSchema()

# 2. Converter a coluna "nome" para maiúsculas
uppercase_df = df.withColumn("nome", upper(df["nome"]))
print("[INFO] Coluna 'nome' convertida para maiúsculas.")

# 3. Contar as linhas do DataFrame
row_count = uppercase_df.count()
print(f"[INFO] Número total de linhas no DataFrame: {row_count}")

# 4. Contar os nomes agrupados por "ano" e "sexo", ordenados pelo ano mais recente
grouped_df = uppercase_df.groupBy("ano", "sexo").count().orderBy(uppercase_df["ano"].desc())
print("[INFO] Contagem de nomes agrupados por ano e sexo (ano mais recente primeiro):")
grouped_df.show()

# 5. Encontrar o nome feminino mais registrado e o ano correspondente
most_female_name = uppercase_df.filter(uppercase_df["sexo"] == "F") \
    .groupBy("nome", "ano") \
    .sum("total") \
    .orderBy("sum(total)", ascending=False) \
    .first()
if most_female_name:
    print(f"[INFO] Nome feminino mais registrado: {most_female_name['nome']} em {most_female_name['ano']}")
else:
    print("[INFO] Nenhum registro encontrado para sexo feminino.")

# 6. Encontrar o nome masculino mais registrado e o ano correspondente
most_male_name = uppercase_df.filter(uppercase_df["sexo"] == "M") \
    .groupBy("nome", "ano") \
    .sum("total") \
    .orderBy("sum(total)", ascending=False) \
    .first()
if most_male_name:
    print(f"[INFO] Nome masculino mais registrado: {most_male_name['nome']} em {most_male_name['ano']}")
else:
    print("[INFO] Nenhum registro encontrado para sexo masculino.")

# 7. Total de registros por ano (apenas os 10 primeiros, ordenados por ano crescente)
yearly_totals_df = uppercase_df.groupBy("ano").sum("total").orderBy("ano").limit(10)
print("[INFO] Total de registros por ano (10 primeiros, ordenados por ano crescente):")
yearly_totals_df.show()

# 8. Escrever o DataFrame resultante com "nome" em maiúsculas no S3 em formato JSON
uppercase_df.write.mode("overwrite").option("spark.sql.sources.partitionOverwriteMode", "dynamic").partitionBy("sexo", "ano").json(target_path)

print("[INFO] Processamento concluído e dados salvos no S3.")

job.commit()
