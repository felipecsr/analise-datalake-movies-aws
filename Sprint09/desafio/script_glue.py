import sys
import boto3
import logging
import os
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from pyspark.sql.functions import col, explode, from_json, when, lit, split, expr
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, DateType, BooleanType, ArrayType

# Caminhos fixos
trusted_path_movies = "s3://desafio-filmes-series/Trusted/Local/Parquet/Movies/2024/12/11/"
trusted_path_tmdb = "s3://desafio-filmes-series/Trusted/TMDB/Parquet/Movies/2024/12/27/"
output_path = "s3://desafio-filmes-series/Refined/"

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger('JobLogger')

logger.info("Job iniciado.")

try:
    # Inicialização do Spark Context
    sc = SparkContext.getOrCreate()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    logger.info("SparkSession inicializada com sucesso.")

    # Definindo o esquema para os campos com base no JSON
    movies_schema = StructType([
        StructField("id", StringType(), True),
        StructField("tituloPincipal", StringType(), True),
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

    tmdb_schema = StructType([
        StructField("id_tmdb", IntegerType(), True),
        StructField("title", StringType(), True),
        StructField("release_date", DateType(), True),
        StructField("overview", StringType(), True),
        StructField("poster_path", StringType(), True),
        StructField("backdrop_path", StringType(), True),
        StructField("budget", IntegerType(), True),
        StructField("revenue", IntegerType(), True),
        StructField("vote_average", FloatType(), True),
        StructField("adult", BooleanType(), True),
        StructField("collection_id", IntegerType(), True),
        StructField("collection_name", StringType(), True),
        StructField("homepage", StringType(), True),
        StructField("imdb_id", StringType(), True),
        StructField("original_language", StringType(), True),
        StructField("popularity", FloatType(), True),
        StructField("status", StringType(), True),
        StructField("tagline", StringType(), True),
        StructField("video", BooleanType(), True),
        StructField("source_file", StringType(), True),
        StructField("genre", StringType(), True),
        StructField("production_companies", ArrayType(StructType([
            StructField("name", StringType(), True),
            StructField("id", IntegerType(), True)
        ])), True),
        StructField("production_countries", ArrayType(StructType([
            StructField("iso_3166_1", StringType(), True),
            StructField("name", StringType(), True)
        ])), True),
        StructField("spoken_languages", ArrayType(StructType([
            StructField("iso_639_1", StringType(), True),
            StructField("name", StringType(), True)
        ])), True)
    ])

    # Leitura de dados com esquemas definidos
    logger.info("Carregando dados da camada Trusted.")
    movies_df = spark.read.schema(movies_schema).format("parquet").load(trusted_path_movies)
    tmdb_df = spark.read.schema(tmdb_schema).format("parquet").load(trusted_path_tmdb)


    # Renomear as colunas antes da junção para evitar colisões
    logger.info("Renomeando colunas das tabelas.")
    for col_name in movies_df.columns:
        movies_df = movies_df.withColumnRenamed(col_name, f"{col_name}___imdb")
    for col_name in tmdb_df.columns:
        tmdb_df = tmdb_df.withColumnRenamed(col_name, f"{col_name}___tmdb")

    # Junção de tabelas
    logger.info("Realizando junção das tabelas.")
    joined_df = movies_df.join(tmdb_df, movies_df.id___imdb == tmdb_df.imdb_id___tmdb, "left")


    # Processamento de campos aninhados (production_companies, production_countries, obs: spoken_languages foi cortado do ETL, ficaremos apenas com original_language)
    logger.info("Processando campos aninhados.")

    # Verificação e renomeação de colunas de campos aninhados
    # Explodir e renomear `production_companies`
    if "production_companies___tmdb" in joined_df.columns:
        joined_df = joined_df.withColumn(
            "production_companies_exploded",
            explode(when(col("production_companies___tmdb").isNotNull(), col("production_companies___tmdb")).otherwise(lit([])))
        )
        joined_df = joined_df.withColumn(
            "company_name", col("production_companies_exploded.name")
        ).withColumn(
            "company_id", col("production_companies_exploded.id")
        ).drop("production_companies___tmdb", "production_companies_exploded")

    # Explodir e renomear `production_countries`
    if "production_countries___tmdb" in joined_df.columns:
        joined_df = joined_df.withColumn(
            "production_countries_exploded",
            explode(when(col("production_countries___tmdb").isNotNull(), col("production_countries___tmdb")).otherwise(lit([])))
        )
        joined_df = joined_df.withColumn(
            "country_name", col("production_countries_exploded.name")
        ).withColumn(
            "country_iso", col("production_countries_exploded.iso_3166_1")
        ).drop("production_countries___tmdb", "production_countries_exploded")

    # Filtros NOT NULL
    logger.info("Aplicando filtros NOT NULL.")
    filtered_df = joined_df.filter(
        col("notaMedia___imdb").isNotNull() &
        col("numeroVotos___imdb").isNotNull() &
        col("id_tmdb___tmdb").isNotNull() &
        col("budget___tmdb").isNotNull() &
        col("revenue___tmdb").isNotNull()
    )

    # Explodindo o campo 'genero___imdb'
    logger.info("Explodindo campo 'genero___imdb'.")
    filtered_df = filtered_df.withColumn(
        "genero", 
        explode(split(expr("regexp_replace(genero___imdb, ' ', '')"), ","))
    )

    # Cálculo de campos adicionais: ROI e financial_result
    logger.info("Adicionando campos calculados.")
    filtered_df = filtered_df.withColumn(
        "ROI", (col("revenue___tmdb") - col("budget___tmdb")) / col("budget___tmdb")
    ).withColumn(
        "financial_result", col("revenue___tmdb") - col("budget___tmdb")
    )

    # Adicionando o campo 'release_decade'
    logger.info("Adicionando campo 'release_decade'.")
    filtered_df = filtered_df.withColumn(
        "release_decade", expr("floor(anoLancamento___imdb / 10) * 10")
    )

      # Criando tabelas de dimensões
    logger.info("Criando tabelas de dimensões e gerando IDs únicos.")

    dim_colecao_df = filtered_df.select(
        "collection_id___tmdb", "collection_name___tmdb"
    ).dropDuplicates().withColumn(
        "id_colecao", row_number().over(Window.orderBy("collection_id___tmdb"))
    )

    dim_produtora_df = filtered_df.select(
        col("company_name").alias("company_name_dim"),
        col("company_id").alias("company_id_dim")
    ).dropDuplicates().withColumn(
        "id_producao", row_number().over(Window.orderBy("company_name_dim"))
    )

    dim_pais_df = filtered_df.select(
        col("country_iso").alias("country_iso_dim"),
        col("country_name").alias("country_name_dim")
    ).dropDuplicates().withColumn(
        "id_pais", row_number().over(Window.orderBy("country_name_dim"))
    )

    dim_artista_df = filtered_df.select(
        "nomeArtista___imdb", "generoArtista___imdb", "personagem___imdb", "anoNascimento___imdb",
        "anoFalecimento___imdb", "profissao___imdb", "titulosMaisConhecidos___imdb"
    ).dropDuplicates().withColumn(
        "id_artista", row_number().over(Window.orderBy("nomeArtista___imdb"))
    )

    dim_genero_df = filtered_df.select(
        "genero", "genre___tmdb"
    ).dropDuplicates().withColumn(
        "id_genero", row_number().over(Window.orderBy("genero"))
    )

    dim_detalhes_df = filtered_df.select(
        "overview___tmdb", "poster_path___tmdb", "backdrop_path___tmdb", "adult___tmdb", "homepage___tmdb",
        "status___tmdb", "tagline___tmdb", "video___tmdb", "source_file___tmdb", "popularity___tmdb"
    ).dropDuplicates().withColumn(
        "id_detalhes", row_number().over(Window.orderBy("overview___tmdb"))
    )

    dim_idioma_df = filtered_df.select(
        col("original_language___tmdb").alias("original_language")
    ).dropDuplicates().withColumn(
        "id_idioma", row_number().over(Window.orderBy("original_language"))
    )

    # Criando a tabela de fato
    logger.info("Criando tabela de fato com colunas de ligação para dimensões.")

    fato_principal_df = filtered_df.select(
        "id___imdb", "id_tmdb___tmdb", "tituloPincipal___imdb", "tituloOriginal___imdb",
        "anoLancamento___imdb", "release_date___tmdb", "release_decade", 
        "tempoMinutos___imdb", "notaMedia___imdb", "numeroVotos___imdb", "vote_average___tmdb",
        "budget___tmdb", "revenue___tmdb", "financial_result", "ROI",
        "collection_id___tmdb", "company_id", "country_iso", "nomeArtista___imdb", "genero", "overview___tmdb", "original_language___tmdb"
    ).withColumn(
        "id_fato", row_number().over(Window.orderBy("id___imdb"))
    )

    # Realizando os joins entre fato e dimensões
    logger.info("Realizando joins entre fato e dimensões.")

    fato_principal_df = fato_principal_df.join(
        dim_colecao_df.select("collection_id___tmdb", "id_colecao"),
        "collection_id___tmdb", "left"
    ).join(
        dim_produtora_df.select("company_id_dim", "id_producao"),
        fato_principal_df["company_id"] == dim_produtora_df["company_id_dim"], "left"
    ).join(
        dim_pais_df.select("country_iso_dim", "id_pais"),
        fato_principal_df["country_iso"] == dim_pais_df["country_iso_dim"], "left"
    ).join(
        dim_artista_df.select("nomeArtista___imdb", "id_artista"),
        fato_principal_df["nomeArtista___imdb"] == dim_artista_df["nomeArtista___imdb"], "left"
    ).join(
        dim_genero_df.select("genero", "id_genero"),
        fato_principal_df["genero"] == dim_genero_df["genero"], "left"
    ).join(
        dim_detalhes_df.select("overview___tmdb", "id_detalhes"),
        fato_principal_df["overview___tmdb"] == dim_detalhes_df["overview___tmdb"], "left"
    ).join(
        dim_idioma_df.select("original_language", "id_idioma"),
        fato_principal_df["original_language___tmdb"] == dim_idioma_df["original_language"], "left"
    )


    # Removendo colunas de chaves originais na tabela fato
    logger.info("Removendo colunas de chaves originais da tabela fato.")
    fato_principal_df = fato_principal_df.drop(
        "collection_id___tmdb", "company_id", "country_iso", "nomeArtista___imdb", "genero", "overview___tmdb", "original_language___tmdb"
    )

    # Salvando tabelas refinadas
    logger.info("Salvando tabelas refinadas.")
    fato_principal_df.write.mode("overwrite").parquet(os.path.join(output_path, "fato_principal"))
    dim_colecao_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_colecao"))
    dim_produtora_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_produtora"))
    dim_pais_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_pais"))
    dim_artista_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_artista"))
    dim_genero_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_genero"))
    dim_detalhes_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_detalhes"))
    dim_idioma_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_idioma"))

    logger.info("Job concluído com sucesso.")

except Exception as e:
    logger.error(f"Ocorreu um erro: {str(e)}")
    sys.exit(1)