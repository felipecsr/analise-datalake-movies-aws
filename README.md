# Projeto: Movies Data Lake

- **Objetivo**: Criar um datalake para ETL (Extração, Transformação e Carga) e posterior análise de dados, com a criação de visualizações utilizando ferramentas de BI.
- **Fontes de Dados**: TMDB (The Movie Database) e IMDB (Internet Movie Database).
- **Processo**: O projeto envolve a coleta de dados das APIs TMDB e IMDB, o armazenamento em um datalake, a aplicação de um pipeline ETL e a modelagem dos dados em um banco relacional (star-schema), com posterior análise e visualização dos dados através de dashboards estáticos.
- **Linguagens**: 
   - Shell Script
   - SQL
   - Python (Pandas, Numpy, Matplotlib, Seaborn) 
   
- **Ferramentas**:
   - **AWS**: S3, Lambda, Glue, Athena, QuickSight
   - **Docker**: Para containerização e consistência de ambientes
   - **Jupyter Notebook**: Para exploração e análise interativa
   - **Boto3**: Integração programática com AWS
   - **Dbeaver e SQLite**: Banco de dados local para testes de modelagem relacional 




---
## Histórico
O projeto ocorreu durante um programa de bolsas oferecido pela Compass UOL e foi organizado por sprints semanais. Aqui abaixo teremos a possibilidade de enxergar estes conteúdos de 2 formas:

1. pela ordem cronológica das sprints
2. pelos temas técnicos abordados
---

## 🗂️ 1. Visão por Sprints Semanais (ordem cronológica)

01. [Sprint01 - Introdução ao Linux, Git e Shell Script](Sprint01/README.md)  
02. [Sprint02 - Introdução a SQL e Modelagem Relacional](Sprint02/README.md)  
03. [Sprint03 - Sintaxe Python e Introdução a ETL](Sprint03/README.md)  
04. [Sprint04 - Programação Funcional em Python e Docker](Sprint04/README.md)  
05. [Sprint05 - AWS S3 e Sites Estáticos](Sprint05/README.md)  
06. [Sprint06 - Lambda, Athena e Docker Layers](Sprint06/README.md)  
07. [Sprint07 - TMDB, Spark e Glue ETL](Sprint07/README.md)  
08. [Sprint08 - Criação da Camada Trusted e Dados Simulados](Sprint08/README.md)  
09. [Sprint09 - Modelagem Multidimensional na Camada Refined](Sprint09/README.md)  
10. [Sprint10 - Dashboards e Visualização com AWS QuickSight](Sprint10/README.md)  

---

## 🔍 2. Visão por Temas Técnicos Abordados

### 🐍 Python
- [Sprint03 - Sintaxe e Funções em Python](Sprint03/README.md)
- [Sprint04 - Programação Funcional e Orientação a Objetos](Sprint04/README.md)
- [Sprint07 - Integração com API (TMDB)](Sprint07/README.md)
- [Sprint08 - Geração de Dados Sintéticos com Python](Sprint08/README.md)

### 🧮 SQL
- [Sprint02 - Consultas SQL e Modelagem Relacional](Sprint02/README.md)
- [Sprint06 - Consultas com AWS Athena](Sprint06/README.md)

### ⚙️ ETL (Extração, Transformação e Carga)
- [Sprint03 - Pipeline ETL simples em Python](Sprint03/README.md)
- [Sprint06 - Lambda + Docker + S3 para processamento ETL](Sprint06/README.md)
- [Sprint07 - ETL com AWS Glue](Sprint07/README.md)
- [Sprint08 - Trusted Zone](Sprint08/README.md)
- [Sprint09 - Refined Zone com Modelagem Dimensional](Sprint09/README.md)

### 🐳 Docker
- [Sprint04 - Criação de Dockerfile e Imagens](Sprint04/README.md)
- [Sprint06 - Docker Layer para Lambda](Sprint06/README.md)
- [Sprint07 - PySpark via Docker](Sprint07/README.md)

### ☁️ AWS (por serviço)

#### 📦 S3 (armazenamento)
- [Sprint05 - Upload, Permissões e Site Estático](Sprint05/README.md)
- [Sprint06 - Criação e Estruturação para ETL](Sprint06/README.md)
- [Sprint07 - Uso no Data Lake (Glue + Athena)](Sprint07/README.md)

#### ⚡ Lambda
- [Sprint06 - Execução de Scripts Python com Camadas](Sprint06/README.md)

#### 🦉 Athena
- [Sprint06 - Criação de Tabela e Consultas](Sprint06/README.md)
- [Sprint07 - Integração com Glue e Crawlers](Sprint07/README.md)

#### 🧪 Glue
- [Sprint07 - ETL com Glue + PySpark](Sprint07/README.md)
- [Sprint08 - Camada Trusted](Sprint08/README.md)
- [Sprint09 - Camada Refined e Star Schema](Sprint09/README.md)

#### 📊 QuickSight
- [Sprint10 - Dashboards e Storytelling com Dados](Sprint10/README.md)

### 🔄 Spark (PySpark)
- [Sprint07 - Contador de Palavras com Spark](Sprint07/README.md)
- [Sprint08 - Análise de Pessoas por País e Geração](Sprint08/README.md)
- [Sprint09 - Transformações e Modelagem](Sprint09/README.md)

### 🔌 Integração de APIs e Dados Externos
- [Sprint07 - Extração de dados da API TMDB](Sprint07/README.md)
- [Sprint08 - Organização e Refino dos Dados TMDB](Sprint08/README.md)

### 📈 Visualização de Dados e Storytelling
- [Sprint10 - Fundamentos de Visualização + QuickSight](Sprint10/README.md)