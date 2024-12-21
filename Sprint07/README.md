# 💻 Exercícios

Nesta sprint 07, seguimos com a segunda etapa de construção do **Desafio Final** do Programa de Bolsas da Compass UOL - a etapa 2 de 5.

Nesta sprint o tema principal é o `Apache Spark`e suas utilizações para manipulação e análise de dados. Entre suas principais características está o processamento distribuído e paralelo, que é essencial para volumes na ordem dos gigabytes e terabytes, os Data Lakes. Há outras características importantes também como:

- escalabilidade horizontal;
- integração com Python e SQL;
- aceita dados semi e não estruturados - além, claro, dos estruturados;
- trabalha (entre outras) com extensões como `ORC` e `Parquet` que são otimizadas para velocidade de processamento e compactação no armazenamento;
- integráveis com serviços em nuvem, com a AWS.

<br/>

Abaixo veremos os exercícios realizados nesta sprint.

## 1 - Exercício: Contador de Palavras com Apache Spark ✨ e Jupyter Lab 🪐

O objetivo deste exercício foi utlizarmos o `Pyspark`para uma análise simples, de contagem de palavras num determinado arquivo - o README da nossa sprint. Em outras palavras, ao invés da original do `Apache Spark`, a linguagem `Scala`, utilizaremos o Pyspark, que de forma nativa também, têm Python e SQL como possibilidades.

### 1.1 - Preparação do Docker

1. Pull da imagem Docker + Jupyter
![Docker Image](../Sprint07/evidencias/ex5-spark-jupyter/1-dockerpull.png)

<br/>

2. Execução do Jupyter, via docker, com os parâmetros de porta e path ajustados 

``` Shell
docker run -it --rm \
    -p 8888:8888 \
    -v /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint07/exercicios/5-Apache_Spark_Contador_de_Palavras:/home/jovyan/work \
    jupyter/all-spark-notebook
```

![Jupyter via Docker](../Sprint07/evidencias/ex5-spark-jupyter/2-jupyter_via_docker.png)

![Jupyter no navegador](../Sprint07/evidencias/ex5-spark-jupyter/3-jupyter_interface.png)

<br/>

3. Testes de execução da Spark Session e reflexo entre diretório do docker e meu ambiente local: sucesso!

![teste jupyter](../Sprint07/evidencias/ex5-spark-jupyter/4-teste_jupyter.png)

![teste jupyter](../Sprint07/evidencias/ex5-spark-jupyter/5-reflexo_docker_local.png)

<br/>

### 1.2 - Execução dos comandos via Pyspark + Resultado

1. Execução do docker no modo interativo
```bash
docker run -it --rm \
    -v /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint07/exercicios/5-Apache_Spark_Contador_de_Palavras:/home/jovyan/work \
    jupyter/all-spark-notebook /bin/bash
```

<br/>

2. Download do README.md para o diretório do docker
```bash
wget --header="Authorization: token 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" \
https://raw.githubusercontent.com/felipecsr/PB-FELIPE-REIS/refs/heads/main/README.md -O /home/jovyan/work/README.md
```
>  **Obs:** *foi necessário criar um token via interface do Github, que utilizei na execução do wget no terminal, e apesar de descrito aqui no código/ documentalão/ print, já foi deletado/ expirado e por isso mantive.*

![wget sucesso](../Sprint07/evidencias/ex5-spark-jupyter/6-wget.png)

<br/>

3. Código contador de palavras executado no Pyspark

``` python
import os
import glob
import shutil
from pyspark.sql import SparkSession

# 1. Inicializar a SparkSession
spark = SparkSession.builder \
    .appName("Word Count Exercise") \
    .master("local[*]") \
    .getOrCreate()

# 2. Definir o caminho absoluto do arquivo README.md
file_path = "/home/jovyan/work/README.md"

# 3. Carregar o arquivo README.md como RDD
rdd = spark.sparkContext.textFile(file_path)

# 4. Contar as palavras no arquivo (preservando a ordem de primeira aparição)
word_counts_with_order = (rdd.flatMap(lambda line: line.split())    # Quebra linhas em palavras
                              .zipWithIndex()                      # Associa cada palavra a seu índice global
                              .map(lambda word_idx: (word_idx[0], (1, word_idx[1])))  # Formato (palavra, (1, índice))
                              .reduceByKey(lambda acc, val: (acc[0] + val[0], min(acc[1], val[1])))  # Soma contagens, mantém o menor índice
                              .sortBy(lambda word_idx: word_idx[1][1])  # Ordena pelo índice de aparição
                              .map(lambda word_idx: (word_idx[0], word_idx[1][0])))  # Resultado final: (palavra, contagem)

# 5. Converter para DataFrame
word_counts_df = word_counts_with_order.toDF(["word", "count"])

# 6. Salvar como CSV em uma única partição
temp_output_path = "/home/jovyan/work/results/temp_word_counts"
word_counts_df.coalesce(1).write.csv(temp_output_path, header=True, mode="overwrite")

# 7. Renomear o arquivo CSV gerado para um nome mais intuitivo
csv_part_file = glob.glob(temp_output_path + "/part-*.csv")[0]  # Busca o arquivo CSV na pasta
final_csv_file = "/home/jovyan/work/results/word_counts_final.csv"

shutil.move(csv_part_file, final_csv_file)  # Renomeia o arquivo
shutil.rmtree(temp_output_path)  # Remove a pasta temporária

print(f"Contagem de palavras concluída e salva como um único arquivo CSV em {final_csv_file}")
```
<br/>

Além do código acima, registrei a execução do script via Docker > Pyspark:
![sucesso script](../Sprint07/evidencias/ex5-spark-jupyter/7-pyspark-sucesso.png)


4. Resultado obtido

E por fim, neste exercício, o resultado obtido de acordo com o que desenvolvi no script foi um arquivo `csv` que pode ser [consultado aqui neste link](../Sprint07/exercicios/5-Apache_Spark/results/word_counts_final.csv).

> **Obs:** *foi interessante verificar, durante as diversas tentativas de resolução do exercício, o retorno do Spark com arquivos 'particionados', por exemplo 2 arquivos.crc (com os metadados) e outros 2 arquivos.csv - que é demonstração cabal de sua form distribuída de processamentos!*

<br/>

## 2 - Exercício: TMDB 🍿📽️
Neste exercício, o objetivo foi realizar uma consulta ao agregador de informações de filmes e séries, [TMDB (The Movie Data Base)](https://www.themoviedb.org/?language=pt-BR), via sua API pública.

1. Foi criada uma conta gratuita com meus dados pessoais;
2. Depois solicitei a liberação de uma chave e token, através da área voltada para desenvolvedores - com êxito!
3. Construí um código semelhante ao do exemplo do exercício, apenas para teste simples.
```python
import requests
import pandas as pd
from IPython.display import display
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave de API do TMDB
api_key = os.getenv("TMDB_API_KEY")

# Verificar se a chave foi carregada corretamente
if not api_key:
    raise ValueError("Chave de API não encontrada. Verifique o arquivo .env.")

# URL da API (ajustado para Crime e Guerra)
url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=pt-BR"

# Fazer a requisição
response = requests.get(url)
data = response.json()

# Lista para armazenar os filmes
filmes = []

# Coletar os primeiros 30 registros diretamente
for movie in data['results'][:30]:
    df = {
        'Título': movie['title'],
        'Data de Lançamento': movie['release_date'],
        'Visão Geral': movie['overview'],
        'Votos': movie['vote_count'],
        'Média de Votos': movie['vote_average']
    }
    filmes.append(df)

# Criar DataFrame
df = pd.DataFrame(filmes)

# Exibir DataFrame
display(df)
```
> **Obs:** pesquisando utilizei uma biblioteca e método que tornam as chaves ocultas no código, para dar mais segurança e praticidade. Trata-se do biblioteca `dotenv`. O funcionamento é simples: cria-se um arquivo .env que terá a chave/ senha  /  o código consulta este arquivo e consulta a senha apenas na memória (de forma oculta ao usuário) e a ligação com a API fica funcional. E para que não suba para o repositorio no `commit` utilizei o `.gitignore`.  

<br/>

4. Tivemos êxito na consulta, que ficou disponível no próprio terminal através da função `display`.
![consulta API TMDB](../Sprint07/evidencias/ex6-TMDB/display-sucessp.png)

<br/><br/>

## 3 - Exercício: AWS Glue 🔻🔎📊

Neste exercício trabalhamos com diversos serviços AWS: IAM, S3, Lake Formation, CloudWatch, Athena - mas especialmente, o AWS Glue.

O exercício consistiu num exemplo de ETL, desde um `.csv` com particionamento em diretórios e sub-diretórios temáticos, conversões de texto, conversões para `.json`, até a criação de tabela com `schema` adequado disponível para análise por *queries* em `SQL`. 

Vamos às etapas:

### 3.1 - Criação de bucket no S3

A primeira criação de um *bucket* no S3, afim de armazenar um `.csv` de diversas linhas, com frequencia de nomes registrados em cartório, num determinado espaço de tempo nos EUA.

### 3.2 - Criação de função (role) no IAM

Uma vez que o arquivo foi armazenado adequadamente, foi necessário criar uma funçao/ escopo no AWS IAM (Identity and Access Management) que nos valeu de acessos integrados entre os serviços que a seguir serão citados.

### 3.3 - Tratamento do arquivo e conversões

Já, então, no AWS Glue, criamos um script em `python` executado via `Spark`, com uso de determinadas sintaxes típicas de execução do código via `AWS Lambda`. O script objetivou a realização de tratamentos de palavras, particionamentos no momento de criação de diretórios, e quebras do conteúdo em diversos arquivos `.json`.

``` python
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
```

### 3.4 - Evidências do ETL + evidências das funççoes `print()` solicitadas no código

Como a execução via Glue não é idêntica à de um `terminal bash`, recorremos ao `AWS CloudWatch` para observar as respostas típicas de terminal, solciitadas no código, que responderam às perguntas elaboradas no exercício.

**Sucesso na execução do script**
![sucesso etl](../Sprint07/evidencias/ex7-awsglue/1-script-etl-sucesso.png)

**Diretórios, sub-duretórios, arquivo JSON (como exemplo, pois foram diversas pastas criadas semelhantes a esta)**
![json sucesso](../Sprint07/evidencias/ex7-awsglue/4-dir-gender-year-json.png)
> Obs: no topo da página é possível visualizar o caminho dos diretórios, conforme instrução do exercício, e um [exemplo de JSON gerado](../Sprint07/exercicios/7-AWSGlueLab/part-00001-fa44f7c2-2782-4a85-9300-9c500beae0d0.c000.json).

**Respostas geradas para visualização no "Terminal"**
![info schema](../Sprint07/evidencias/ex7-awsglue/5-info-schema.png)

![total de linhas dataframe](../Sprint07/evidencias/ex7-awsglue/7-info-df-lines.png)

![cotagem por sexo e ano](../Sprint07/evidencias/ex7-awsglue/8-show-count-per-gender-year.png)

![maiores valores de contagem para sexo feminino](../Sprint07/evidencias/ex7-awsglue/9-info-top-count-per-gender-F.png)

![maiores valores de contagem para sexo masculino](../Sprint07/evidencias/ex7-awsglue/10-info-top-count-per-gender-M.png)

![Top 10 por ano](../Sprint07/evidencias/ex7-awsglue/11-info-top10-count-per-year.png)

### 3.5 - Criação de Crawler de automação

Nesta ultima etapa do exercício criamos um Crawler (uma espécie de automação/ rastreador), que pode agir a cada interação do arquivo no S3, com agendamento ou manualmente. Neste exercício, manualmente, criamos uma tabela no Banco de dados, que pode ser acessado diretamente (e integradamente) via Athena, simulando uma consulta `SQL`.

![crawler criado sucesso](../Sprint07/evidencias/ex7-awsglue/12-Crawler-sucesso.png)

![teste acesso via Athena sucesso](../Sprint07/evidencias/ex7-awsglue/13-athena-sucesso.png)

<br/>

# 📜 Certificados

- [Formação Spark com Pyspark: o Curso Completo](../Sprint06/certificados/Analyticsp1.png)


<br/>  
  
# 🧠 Desafio
**TMDB, API JSON e Data Lake com AWS S3: Integração e Expansão de Dados**  
Nesta etapa do desafio, o foco principal foi a integração de dados externos, utilizando a API pública do TMDB (The Movie Database) para extrair informações detalhadas sobre filmes e séries. O objetivo é enriquecer os dados raw já existentes no bucket "desafio-filmes-series" no S3, consolidando-os em um Data Lake robusto e preparado para análises futuras.

A abordagem incluiu não apenas a extração de dados, mas também o início de uma estruturação automatizada de pipeline. Essa integração garante que os dados coletados sigam um padrão consistente e sejam organizados de forma escalável para as próximas etapas do projeto.

[Confira o 'readme' do desafio aqui!](Desafio/README.md)