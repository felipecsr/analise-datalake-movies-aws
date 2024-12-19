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

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>



# 📜 Certificados

- [Fundamentals of Analytics - Part 1](../Sprint06/certificados/Analyticsp1.png)
- [Fundamentals of Analytics - Part 2](../Sprint06/certificados/Analyticsp2.png)
- [Introduction to Amazon Athena](../Sprint06/certificados/Athena.png)
- [Amazon EMR](../Sprint06/certificados/EMR.png)
- [AWS Glue Getting Started](../Sprint06/certificados/Glue.png)
- [Getting Started with Amazon Redshift](../Sprint06/certificados/Redshift.png)
- [Best Practices for Data Warehousing with Amazon Redshift](../Sprint06/certificados/Redshift-DW.png)
- [Serverless Analytics](../Sprint06/certificados/Analyticsp1.png)
- [Amazon QuickSight - Getting Started](../Sprint06/certificados/QuickSight.png)

<br/>  
  
# 🧠 Desafio
**AWS S3, Containers e Python 3.9: Automatizando o Pipeline de Dados**  
O desafio dessa sprint foi uma experiência interessante e desafiadora no uso de AWS S3 e containers, com um foco em automação e estruturação de dados na nuvem. O objetivo foi organizar e enviar dois arquivos CSV, movies.csv e series.csv, para um bucket no S3, seguindo uma estrutura específica que foi detalhada nos slides do desafio. Esses arquivos foram alocados em uma zona de raw data, criando um ponto inicial para análises futuras.

O que realmente me impressionou nesta sprint foi a orientação para utilizar um container com Python 3.9. Essa abordagem, ao invés de usar o ambiente local, foi uma maneira muito eficiente de garantir que o código tivesse as dependências necessárias e funcionasse de maneira consistente em diferentes ambientes. Além disso, ao utilizar um container, a solução ficou mais "flat", sem depender das configurações específicas da minha máquina, o que facilita a replicação em diferentes contextos, seja para testes ou produção.

Por fim, um script em Python foi criado para automatizar todo o processo: desde a criação do bucket no S3, passando pela estruturação das pastas, até o upload dos arquivos CSV. A simplicidade e a eficiência dessa automação não só simplificaram o processo como também ajudaram a entender melhor como integrar os diferentes componentes da AWS em um fluxo de trabalho coeso e bem estruturado.

Essa sprint, com sua combinação de serviços da AWS e containers, me mostrou como é possível trabalhar de maneira mais ágil e escalável, sem depender de configurações locais, garantindo flexibilidade e controle sobre os dados na nuvem.

[Confira o 'readme' do desafio aqui!](Desafio/README.md)