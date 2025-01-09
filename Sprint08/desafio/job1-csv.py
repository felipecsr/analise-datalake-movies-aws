from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, when, trim, lower
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

# Inicializando o contexto do Glue e Spark
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Nome do Job (definido diretamente no código)
job_name = "Job1 - Trusted Zone - CSV ETL"
job.init(job_name, {})

# Caminhos S3
raw_path = "s3://desafio-filmes-series/Raw/Local/CSV/Movies/2024/12/11/movies.csv"
trusted_path = "s3://desafio-filmes-series/Trusted/Local/Parquet/Movies/2024/12/11/"

# Definindo o schema manualmente
schema = StructType([
    StructField("id", StringType(), True),
    StructField("tituloPincipal", StringType(), True),  # Nome corrigido conforme o CSV
    StructField("tituloOriginal", StringType(), True),
    StructField("anoLancamento", IntegerType(), True),
    StructField("tempoMinutos", IntegerType(), True),
    StructField("genero", StringType(), True),
    StructField("notaMedia", FloatType(), True),
    StructField("numeroVotos", IntegerType(), True),
    StructField("generoArtista", StringType(), True),
    StructField("personagem", StringType(), True),
    StructField("nomeArtista", StringType(), True),
    StructField("anoNascimento", IntegerType(), True),
    StructField("anoFalecimento", IntegerType(), True),
    StructField("profissao", StringType(), True),
    StructField("titulosMaisConhecidos", StringType(), True)
])

# Leitura do CSV com o schema definido
df = spark.read.csv(
    raw_path,
    schema=schema,
    sep='|',
    encoding='UTF-8',
    header=True
)

# Substituindo campos vazios ("") por NULL
df = df.replace("", None)

# Substituindo valores "N" por NULL nas colunas especificadas
columns_to_clean = ["tempoMinutos", "genero", "personagem", "anoNascimento", "anoFalecimento", "titulosMaisConhecidos"]
for col_name in columns_to_clean:
    df = df.withColumn(col_name, when(col(col_name) == "N", None).otherwise(col(col_name)))

# Removendo duplicatas
df = df.dropDuplicates()

# Normalizando colunas de texto (corrigindo também o nome errado da coluna)
df = df.withColumn("tituloPincipal", trim(lower(col("tituloPincipal"))))
df = df.withColumn("tituloOriginal", trim(lower(col("tituloOriginal"))))

# Filtrando filmes de Crime ou Guerra
df_filtered = df.filter(
    (col("genero").isNotNull()) & (
        (col("genero").like("%Crime%")) | 
        (col("genero").like("%Guerra%")) | 
        (col("genero").like("%War%"))
    )
)

# Escrevendo os dados na camada Trusted em formato PARQUET
df_filtered.write.mode("overwrite").parquet(trusted_path)

# Finalizando o job
job.commit()
print("Job finalizado com sucesso!")
