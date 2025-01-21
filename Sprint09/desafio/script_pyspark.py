from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, split, explode, udf, when
from pyspark.sql.types import StringType

# Inicializar Spark
spark = SparkSession.builder \
    .appName("ETL Trusted to Refined") \
    .getOrCreate()

# Diretórios S3
trusted_imdb_path = "s3://your-bucket/trusted/imdb/"
trusted_tmdb_path = "s3://your-bucket/trusted/tmdb/"
refined_output_path = "s3://your-bucket/refined/movies/"

# Ler os arquivos Parquet
imdb_df = spark.read.parquet(trusted_imdb_path)
tmdb_df = spark.read.parquet(trusted_tmdb_path)

# Junção dos dados IMDb e TMDb
movies_df = imdb_df.join(
    tmdb_df,
    imdb_df.id == tmdb_df.imdb_id,
    how="left"
)

# Filtros
movies_filtered_df = movies_df.filter(
    (col("id_tmdb").isNotNull()) &
    (col("revenue").isNotNull()) &
    (col("budget").isNotNull()) &
    ((col("notaMedia").isNotNull()) | (col("vote_average").isNotNull()))
)

# Determinar o gênero principal
def find_main_genre(genres):
    genre_priority = ["Crime", "War"]
    for genre in genres:
        if genre in genre_priority:
            return genre
    return None

main_genre_udf = udf(find_main_genre, StringType())

movies_filtered_df = movies_filtered_df.withColumn(
    "genre_list", split(col("genre"), ",")
).withColumn(
    "main_genre", main_genre_udf(col("genre_list"))
)

# Expandir os gêneros em múltiplas linhas
movies_exploded_df = movies_filtered_df.withColumn(
    "genre", explode(col("genre_list"))
)

# Calcular ROI
movies_exploded_df = movies_exploded_df.withColumn(
    "roi", (col("revenue") - col("budget")) / col("budget")
)

# Cálculo do avg_rating com peso dinâmico
median_imdb_votes = movies_filtered_df.approxQuantile("numeroVotos", [0.5], 0.05)[0]
tmdb_weight = median_imdb_votes / 10

movies_exploded_df = movies_exploded_df.withColumn(
    "avg_rating",
    (
        (col("notaMedia") * col("numeroVotos")) +
        (col("vote_average") * lit(tmdb_weight))
    ) / (col("numeroVotos") + lit(tmdb_weight))
)

# Lista final de colunas
final_columns = [
    # IMDb fields
    "id", "tituloPincipal", "tituloOriginal", "anoLancamento", "tempoMinutos",
    "genero", "notaMedia", "numeroVotos", "generoArtista", "personagem",
    "nomeArtista", "anoNascimento", "anoFalecimento", "profissao", "titulosMaisConhecidos",
    # TMDb fields
    "id_tmdb", "title", "release_date", "overview", "poster_path", "backdrop_path",
    "budget", "revenue", "vote_average", "adult", "collection_id", "collection_name",
    "homepage", "imdb_id", "original_language", "popularity", "status", "tagline",
    "video", "source_file", "production_companies", "production_countries", "spoken_languages",
    # Calculated fields
    "main_genre", "genre", "roi", "avg_rating"
]

# Selecionar as colunas finais
refined_df = movies_exploded_df.select(final_columns)

# Salvar o dataset refinado no S3 em formato Parquet
refined_df.write.mode("overwrite").parquet(refined_output_path)

print("ETL process completed successfully.")
