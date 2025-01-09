from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, trim, lower, when, explode, size, input_file_name, regexp_extract
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, BooleanType, DateType, ArrayType

# Inicializando o contexto do Glue e Spark
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Nome do Job (definido diretamente no código)
job_name = "Job2 - Trusted Zone - JSON ETL"
job.init(job_name, {})

# Caminhos S3
raw_path = "s3://desafio-filmes-series/Raw/TMDB/JSON/Movies/2024/12/27/"
trusted_path = "s3://desafio-filmes-series/Trusted/TMDB/Parquet/Movies/2024/12/27/"

# Definição do schema
schema = StructType([
    StructField("id_tmdb", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("release_date", DateType(), True),
    StructField("overview", StringType(), True),
    StructField("poster_path", StringType(), True),
    StructField("backdrop_path", StringType(), True),
    StructField("production_companies", ArrayType(
        StructType([
            StructField("name", StringType(), True),
            StructField("id", IntegerType(), True)
        ])
    ), True),
    StructField("production_countries", ArrayType(
        StructType([
            StructField("iso_3166_1", StringType(), True),
            StructField("name", StringType(), True)
        ])
    ), True),
    StructField("spoken_languages", ArrayType(
        StructType([
            StructField("iso_639_1", StringType(), True),
            StructField("name", StringType(), True)
        ])
    ), True),
    StructField("budget", IntegerType(), True),
    StructField("revenue", IntegerType(), True),
    StructField("vote_average", FloatType(), True),
    StructField("adult", BooleanType(), True),
    StructField("belongs_to_collection", StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ]), True),
    StructField("homepage", StringType(), True),
    StructField("imdb_id", StringType(), True),
    StructField("original_language", StringType(), True),
    StructField("popularity", FloatType(), True),
    StructField("status", StringType(), True),
    StructField("tagline", StringType(), True),
    StructField("video", BooleanType(), True)
])

# Leitura dos arquivos JSON com o schema definido
df = spark.read.json(
    raw_path,
    schema=schema,
    multiLine=True
)

# Adicionando o nome do arquivo como coluna "source_file"
df = df.withColumn("source_file", input_file_name())

# Extraindo o gênero do nome do arquivo e adicionando como coluna "genre"
df = df.withColumn("genre", regexp_extract(col("source_file"), r"genre-(\d+)-", 1))

# Mapeando códigos de gênero para nomes legíveis
genre_map = {"80": "Crime", "10752": "War"}
genre_keys = list(genre_map.keys())

df = df.withColumn("genre", when(col("genre").isin(genre_keys), col("genre").cast(StringType())).alias("genre_name"))
for code, name in genre_map.items():
    df = df.withColumn("genre", when(col("genre") == code, name).otherwise(col("genre")))

# Substituindo listas vazias ("[]") por NULL nos arrays
columns_with_arrays = ["production_companies", "production_countries", "spoken_languages"]
for col_name in columns_with_arrays:
    df = df.withColumn(col_name, when((col(col_name).isNull()) | (size(col(col_name)) == 0), None).otherwise(col(col_name)))

# Substituindo strings vazias ("") por NULL em todos os campos
columns_with_empty_strings = [col_name for col_name in df.columns if df.schema[col_name].dataType == StringType()]
for col_name in columns_with_empty_strings:
    df = df.withColumn(col_name, when(col(col_name) == "", None).otherwise(col(col_name)))

# Substituindo valores 0 por NULL nos campos "budget" e "revenue"
df = df.withColumn("budget", when(col("budget") == 0, None).otherwise(col("budget")))
df = df.withColumn("revenue", when(col("revenue") == 0, None).otherwise(col("revenue")))

# Normalizando colunas de texto
df = df.withColumn("title", trim(lower(col("title"))))
df = df.withColumn("homepage", trim(lower(col("homepage"))))

# Explodindo e desdobrando arrays
flattened_df = df.withColumn("company", explode(col("production_companies")))
flattened_df = flattened_df.withColumn("country", explode(col("production_countries")))
flattened_df = flattened_df.withColumn("language", explode(col("spoken_languages")))

# Criando coluna com o nome do arquivo JSON extraído
flattened_df = flattened_df.withColumn("file_name", regexp_extract(col("source_file"), r"([^/]+)\.json$", 1))

# Selecionando as colunas finais para o DataFrame consolidado
final_df = flattened_df.select(
    col("id_tmdb"),
    col("title"),
    col("release_date"),
    col("overview"),
    col("poster_path"),
    col("backdrop_path"),
    col("budget"),
    col("revenue"),
    col("vote_average"),
    col("adult"),
    col("belongs_to_collection.id").alias("collection_id"),
    col("belongs_to_collection.name").alias("collection_name"),
    col("homepage"),
    col("imdb_id"),
    col("original_language"),
    col("popularity"),
    col("status"),
    col("tagline"),
    col("video"),
    col("source_file"),
    col("genre"),
    col("company.name").alias("company_name"),
    col("company.id").alias("company_id"),
    col("country.iso_3166_1").alias("country_iso"),
    col("country.name").alias("country_name"),
    col("language.iso_639_1").alias("language_iso"),
    col("language.name").alias("language_name"),
    col("file_name")
)

# Salvando cada JSON como um arquivo Parquet separado
file_names = [row.file_name for row in final_df.select("file_name").distinct().collect()]

for file_name in file_names:
    file_df = final_df.filter(col("file_name") == file_name)
    file_df.write.mode("overwrite").parquet(f"{trusted_path}{file_name}.parquet")

# Finalizando o job
job.commit()
print("Job finalizado com sucesso!")
