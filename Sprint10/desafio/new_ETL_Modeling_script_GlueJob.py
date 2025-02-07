import sys
import logging
import os
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import (
    row_number, col, explode, when, lit, split, expr, 
    count, array_contains, concat_ws, collect_set, first,
    min, max
)
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, 
    FloatType, DateType, BooleanType, ArrayType
)

# ----------------------------------------------------------------------------
# 1) Configurações Iniciais e Leitura
# ----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JobLogger")

trusted_path_movies = "s3://desafio-filmes-series/Trusted/Local/Parquet/Movies/2024/12/11/"
trusted_path_tmdb   = "s3://desafio-filmes-series/Trusted/TMDB/Parquet/Movies/2024/12/27/"
output_path         = "s3://desafio-filmes-series/Refined/"

spark = SparkSession.builder.getOrCreate()

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
    StructField("personagem", StringType(), True),   # <--- NOT used in dimension
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
    StructField("production_companies", ArrayType(StructType([
        StructField("name", StringType(), True),
        StructField("id", IntegerType(), True)
    ])), True),
    StructField("production_countries", ArrayType(StructType([
        StructField("iso_3166_1", StringType(), True),
        StructField("name", StringType(), True)
    ])), True)
])

logger.info("Lendo dados IMDB e TMDB...")

movies_df = spark.read.schema(movies_schema).parquet(trusted_path_movies)
tmdb_df   = spark.read.schema(tmdb_schema).parquet(trusted_path_tmdb)

# ----------------------------------------------------------------------------
# 2) Join e Preprocessamento
# ----------------------------------------------------------------------------

logger.info("Realizando Join (IMDB + TMDB) via id/imdb_id...")

joined_df = movies_df.join(
    tmdb_df,
    movies_df.id == tmdb_df.imdb_id,
    "left"
)

# ----------------------------------------------------------------------------
# 3) Filtro de NOT NULL para a camada Refined
# Campos: notaMedia, numeroVotos, id, budget, revenue, anoLancamento
# ----------------------------------------------------------------------------

logger.info("Filtrando registros para remover nulos em campos essenciais...")

joined_df = joined_df.filter(
    col("notaMedia").isNotNull() &
    col("numeroVotos").isNotNull() &
    col("id").isNotNull() &
    col("budget").isNotNull() &
    col("revenue").isNotNull() &
    col("anoLancamento").isNotNull()
)

# ----------------------------------------------------------------------------
# 4) Explodir e Tratar Arrays (produtoras, países, gênero)
# ----------------------------------------------------------------------------

logger.info("Explodindo production_countries...")

joined_df = joined_df.withColumn(
    "production_countries_exploded",
    explode(when(col("production_countries").isNotNull(),
                 col("production_countries")).otherwise(lit([])))
).withColumn(
    "pais_producao", col("production_countries_exploded.name")
).drop("production_countries", "production_countries_exploded")

logger.info("Explodindo production_companies...")

joined_df = joined_df.withColumn(
    "production_companies_exploded",
    explode(when(col("production_companies").isNotNull(),
                 col("production_companies")).otherwise(lit([])))
).withColumn(
    "nome_produtora",
    col("production_companies_exploded.name")
).drop("production_companies", "production_companies_exploded")

logger.info("Tratando campo genero (IMDB)...")

joined_df = joined_df.withColumn(
    "genero_list", split(expr("regexp_replace(genero, ' ', '')"), ",")
).withColumn(
    "genero_analise",
    when(array_contains(col("genero_list"), "Crime") & array_contains(col("genero_list"), "War"), lit("crime&war"))
    .when(array_contains(col("genero_list"), "Crime"), lit("crime"))
    .when(array_contains(col("genero_list"), "War"), lit("war"))
    .otherwise(lit(None))
).withColumn(
    "genero_associado", expr("filter(genero_list, x -> x NOT IN ('Crime','War'))")
)

# ----------------------------------------------------------------------------
# 5) Criação das Dimensões Principais
# ----------------------------------------------------------------------------

# 5.1 Dimensão Artista (1 registro por artista)
#    - Remove 'personagem', pois não vamos usar no dimensionamento
logger.info("Criando dim_artista...")

dim_artista_df = (
    movies_df
    .filter(col("nomeArtista").isNotNull())
    .groupBy("nomeArtista")
    .agg(
        concat_ws("|", collect_set("generoArtista")).alias("artista_genero"),
        concat_ws("|", collect_set("profissao")).alias("artista_profissao"),
        # 'personagem' não será usado na análise => não agregamos
        concat_ws("|", collect_set("titulosMaisConhecidos")).alias("artista_outrosTitulos"),
        min("anoNascimento").alias("artista_ano_nascimento"),
        max("anoFalecimento").alias("artista_ano_falecimento")
    )
    .withColumn("id_artista", row_number().over(Window.orderBy("nomeArtista")))
)

# 5.2 Dimensão Coleção (1:1 ou 1:N, mas cada filme tem 0 ou 1 collection_id)
#    - Calculamos colecao_quantidade_filmes
logger.info("Criando dim_colecao...")

dim_colecao_df = (
    joined_df
    .filter(col("collection_id").isNotNull())
    .groupBy("collection_id", "collection_name")
    .agg(count("*").alias("colecao_quantidade_filmes"))
    .withColumn("id_colecao", row_number().over(Window.orderBy("collection_id")))
)

# 5.3 Dimensão Detalhes
logger.info("Criando dim_detalhes...")

dim_detalhes_df = (
    joined_df
    .select("overview", "poster_path", "backdrop_path", 
            "homepage", "status", "tagline", "video", "source_file")
    .distinct()
    .withColumn("id_detalhes", row_number().over(Window.orderBy("overview")))
)

# 5.4 Dimensão Idioma
logger.info("Criando dim_idioma...")

dim_idioma_df = (
    joined_df
    .select("original_language")
    .distinct()
    .withColumn("id_idioma", row_number().over(Window.orderBy("original_language")))
)

# 5.5 Dimensão Gênero
#    - Precisamos 1 registro por gênero do array 'genero_associado'.
logger.info("Criando dim_genero...")

exploded_generos_df = joined_df.select(
    explode(col("genero_associado")).alias("genero_item")
).filter(col("genero_item").isNotNull()).distinct()

dim_genero_df = (
    exploded_generos_df
    .withColumn("id_genero", row_number().over(Window.orderBy("genero_item")))
)

# 5.6 Dimensão País
logger.info("Criando dim_pais...")

dim_pais_df = (
    joined_df
    .select("pais_producao")
    .filter(col("pais_producao").isNotNull())
    .distinct()
    .withColumn("id_pais", row_number().over(Window.orderBy("pais_producao")))
)

# 5.7 Dimensão Produtora
logger.info("Criando dim_produtora...")

dim_produtora_df = (
    joined_df
    .select("nome_produtora")
    .filter(col("nome_produtora").isNotNull())
    .distinct()
    .withColumn("id_produtora", row_number().over(Window.orderBy("nome_produtora")))
)

# ----------------------------------------------------------------------------
# 6) Criação da Fato Principal (1 registro por filme)
#    - Calculamos as métricas necessárias
# ----------------------------------------------------------------------------

logger.info("Criando fato_principal...")

from pyspark.sql import functions as F

# Agrupamos por "id" do IMDB para que fique 1 linha por filme.
# Caso haja múltiplas produtoras/países, não iremos duplicar aqui.
fato_filme_df = (
    joined_df
    .groupBy("id")
    .agg(
        F.first("id_tmdb", True).alias("f_filme_id_tmdb"),
        F.first("tituloOriginal", True).alias("f_filme_tituloOriginal"),
        F.first("tituloPincipal", True).alias("f_filme_tituloPincipal"),
        F.first("anoLancamento", True).alias("f_tempo_anoLancamento"),
        F.first("release_date", True).alias("f_tempo_dataLancamento"),
        F.first("tempoMinutos", True).alias("f_tempo_minutos"),
        F.first("notaMedia", True).alias("f_aval_notaMedia_imdb"),
        F.first("numeroVotos", True).alias("f_aval_numeroVotos_imdb"),
        F.first("vote_average", True).alias("f_aval_notaMedia_tmdb"),
        F.first("popularity", True).alias("f_aval_popularity_tmdb"),
        F.first("adult", True).alias("f_filme_adult"),
        F.first("budget", True).alias("f_fin_orcamento"),
        F.first("revenue", True).alias("f_fin_receita"),
        F.first("overview", True).alias("dim_detalhes_overview"),
        F.first("original_language", True).alias("dim_idioma_code"),
        F.first("collection_id", True).alias("dim_colecao_id"),
        F.first("genero_analise", True).alias("f_filme_genero_analise")
    )
    .withColumnRenamed("id", "f_filme_id_imdb")
)

# Cálculos
fato_filme_df = fato_filme_df.withColumn(
    "f_fin_resultado", 
    col("f_fin_receita") - col("f_fin_orcamento")
).withColumn(
    "f_fin_roi", 
    when(col("f_fin_orcamento") != 0,
         (col("f_fin_receita") - col("f_fin_orcamento")) / col("f_fin_orcamento"))
    .otherwise(None)
).withColumn(
    "f_release_decade", 
    (col("f_tempo_anoLancamento") / 10).cast("int") * 10
).withColumn(
    "f_fin_lucro_por_minuto",
    when(col("f_tempo_minutos") > 0,
         (col("f_fin_receita") - col("f_fin_orcamento")) / col("f_tempo_minutos"))
    .otherwise(None)
).withColumn(
    "f_fin_tempo_votos_por_minuto",
    when(col("f_tempo_minutos") > 0,
         col("f_aval_numeroVotos_imdb") / col("f_tempo_minutos"))
    .otherwise(None)
)

# Criar um ID de fato substituto
fato_principal_df = fato_filme_df.withColumn(
    "id_fato", row_number().over(Window.orderBy("f_filme_id_imdb"))
)

# ----------------------------------------------------------------------------
# 7) Associar a Fato com Dimensões 1:1 (colecao, detalhes, idioma)
#    - Gênero, artista, país, produtora serão tratados por Tabelas de Ponte
# ----------------------------------------------------------------------------

# 7.1 Coleção
fato_principal_df = fato_principal_df.join(
    dim_colecao_df.select("collection_id", "id_colecao"),
    fato_principal_df["dim_colecao_id"] == dim_colecao_df["collection_id"],
    "left"
).drop("dim_colecao_id", "collection_id")

# 7.2 Detalhes
fato_principal_df = fato_principal_df.join(
    dim_detalhes_df.select("overview", "id_detalhes"),
    fato_principal_df["dim_detalhes_overview"] == dim_detalhes_df["overview"],
    "left"
).drop("dim_detalhes_overview", "overview")

# 7.3 Idioma
fato_principal_df = fato_principal_df.join(
    dim_idioma_df.select("original_language", "id_idioma"),
    fato_principal_df["dim_idioma_code"] == dim_idioma_df["original_language"],
    "left"
).drop("dim_idioma_code", "original_language")

# ----------------------------------------------------------------------------
# 8) Criação das Tabelas de Ponte (bridges) p/ relacionamentos 1:N
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# 8.1 fact_film_artist
# ----------------------------------------------------------------------------
logger.info("Criando tabela de ponte: fact_film_artist...")

film_artist_raw = joined_df.select(
    col("id").alias("imdb_film_id"),
    col("nomeArtista").alias("raw_artista")
).filter(col("imdb_film_id").isNotNull() & col("raw_artista").isNotNull())

fact_film_artist_df = (
    film_artist_raw
    # join c/ fato principal => p/ resgatar "id_fato"
    .join(
        fato_principal_df.select("f_filme_id_imdb","id_fato"),
        film_artist_raw["imdb_film_id"] == fato_principal_df["f_filme_id_imdb"],
        "inner"
    )
    # join c/ dim_artista => p/ resgatar "id_artista"
    .join(
        dim_artista_df.select("nomeArtista","id_artista"),
        film_artist_raw["raw_artista"] == dim_artista_df["nomeArtista"],
        "left"
    )
    .select(
        col("id_fato"),
        col("id_artista")
    )
    .dropDuplicates(["id_fato","id_artista"])  # remove duplicados (se não quiser repetição)
)

# ----------------------------------------------------------------------------
# 8.2 fact_film_genero
#    - Precisamos explodir 'genero_associado' para cada filme
# ----------------------------------------------------------------------------
logger.info("Criando tabela de ponte: fact_film_genero...")

film_genero_raw = joined_df.select(
    col("id").alias("imdb_film_id"),
    explode(col("genero_associado")).alias("genero_item")
).filter(col("genero_item").isNotNull())

fact_film_genero_df = (
    film_genero_raw
    .join(
        fato_principal_df.select("f_filme_id_imdb","id_fato"),
        film_genero_raw["imdb_film_id"] == fato_principal_df["f_filme_id_imdb"],
        "inner"
    )
    .join(
        dim_genero_df.select("genero_item","id_genero"),
        film_genero_raw["genero_item"] == dim_genero_df["genero_item"],
        "left"
    )
    .select(
        col("id_fato"),
        col("id_genero")
    )
    .dropDuplicates(["id_fato","id_genero"])
)

# ----------------------------------------------------------------------------
# 8.3 fact_film_pais
# ----------------------------------------------------------------------------
logger.info("Criando tabela de ponte: fact_film_pais...")

film_pais_raw = joined_df.select(
    col("id").alias("imdb_film_id"),
    col("pais_producao")
).filter(col("pais_producao").isNotNull())

fact_film_pais_df = (
    film_pais_raw
    .join(
        fato_principal_df.select("f_filme_id_imdb","id_fato"),
        film_pais_raw["imdb_film_id"] == fato_principal_df["f_filme_id_imdb"],
        "inner"
    )
    .join(
        dim_pais_df.select("pais_producao","id_pais"),
        film_pais_raw["pais_producao"] == dim_pais_df["pais_producao"],
        "left"
    )
    .select("id_fato","id_pais")
    .dropDuplicates(["id_fato","id_pais"])
)

# ----------------------------------------------------------------------------
# 8.4 fact_film_produtora
# ----------------------------------------------------------------------------
logger.info("Criando tabela de ponte: fact_film_produtora...")

film_produtora_raw = joined_df.select(
    col("id").alias("imdb_film_id"),
    col("nome_produtora")
).filter(col("nome_produtora").isNotNull())

fact_film_produtora_df = (
    film_produtora_raw
    .join(
        fato_principal_df.select("f_filme_id_imdb","id_fato"),
        film_produtora_raw["imdb_film_id"] == fato_principal_df["f_filme_id_imdb"],
        "inner"
    )
    .join(
        dim_produtora_df.select("nome_produtora","id_produtora"),
        film_produtora_raw["nome_produtora"] == dim_produtora_df["nome_produtora"],
        "left"
    )
    .select("id_fato","id_produtora")
    .dropDuplicates(["id_fato","id_produtora"])
)

# ----------------------------------------------------------------------------
# 9) Escrita em Parquet
# ----------------------------------------------------------------------------

logger.info("Salvando tabelas...")

fato_principal_df.write.mode("overwrite").parquet(os.path.join(output_path, "fato_principal"))
dim_artista_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_artista"))
dim_colecao_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_colecao"))
dim_detalhes_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_detalhes"))
dim_genero_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_genero"))
dim_idioma_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_idioma"))
dim_pais_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_pais"))
dim_produtora_df.write.mode("overwrite").parquet(os.path.join(output_path, "dim_produtora"))

fact_film_artist_df.write.mode("overwrite").parquet(os.path.join(output_path, "fact_film_artist"))
fact_film_genero_df.write.mode("overwrite").parquet(os.path.join(output_path, "fact_film_genero"))
fact_film_pais_df.write.mode("overwrite").parquet(os.path.join(output_path, "fact_film_pais"))
fact_film_produtora_df.write.mode("overwrite").parquet(os.path.join(output_path, "fact_film_produtora"))

logger.info("Pipeline concluído com sucesso!")
