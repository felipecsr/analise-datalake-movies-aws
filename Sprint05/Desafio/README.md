
# 🎯 Objetivo

Este README documenta a resolução do desafio da Sprint 05.  
O desafio consistiu na manipulação de dados utilizando Python e a AWS S3 para armazenamento, processamento e análise. Foi dividido em duas etapas principais: envio e leitura de arquivos no S3, além do tratamento, filtragem e criação de indicadores a partir dos dados.

---

# Etapa 1

## 🗂️ Criação do Bucket e Upload de Arquivo

Nesta etapa, o objetivo foi criar um bucket na AWS S3 e realizar o upload de um arquivo CSV para este bucket.

### Criação do Bucket

```python
import boto3
from botocore.exceptions import ClientError

# Configurações iniciais
s3 = boto3.client('s3', region_name='us-east-1')
bucket_name = 'bucket-desafio-sprint05'

def create_bucket(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' criado com sucesso!")
    except ClientError as e:
        print(f"Erro ao criar o bucket: {e}")
```
**Função Utilizada:** `create_bucket` - Criação do bucket utilizando boto3, que pertence ao grupo de funções de interação com S3.

### Upload do Arquivo

```python
csv_file_path = 'CAT202306.csv'

def upload_file_to_s3(local_file_path, bucket_name, s3_key, content_type=None):
    try:
        extra_args = {'ContentType': content_type} if content_type else {}
        s3.upload_file(local_file_path, bucket_name, s3_key, ExtraArgs=extra_args)
        print(f"Arquivo '{local_file_path}' enviado para '{bucket_name}/{s3_key}'!")
    except ClientError as e:
        print(f"Erro ao enviar o arquivo: {e}")
```
**Função Utilizada:** `upload_file_to_s3` - Realiza o upload de arquivos locais para o bucket no S3.

### Execução Principal

```python
def main():
    create_bucket(bucket_name)
    upload_file_to_s3(csv_file_path, bucket_name, 'CAT202306.csv', content_type='text/csv')

if __name__ == '__main__':
    main()
```
Essa estrutura organiza a execução sequencial das tarefas principais.
<br/>

### Evidências da  criação do Bucket com suscesso!

![bucket criado com sucesso via terminal](../evidencias/desafio/3-bucket_criado_terminal.png)

![bucket criado com sucesso no console](../evidencias/desafio/1-bucket_criado.png)


<br/>


# Etapa 2

## 📊 Processamento, Filtragem e Geração de Indicadores

Nesta etapa, o foco foi na manipulação e tratamento dos dados armazenados no bucket S3, utilizando o pandas e o boto3. O objetivo foi criar dois novos arquivos (tratado e filtrado) e um relatório de indicadores em no formato `xlsx` - com abas e os indicadores separados.

### Carregamento de Arquivo no S3

```python
import pandas as pd
import boto3
from botocore.exceptions import ClientError

# Configurações iniciais
bucket_name = 'bucket-desafio-sprint05'
input_file_key = 'CAT202306.csv'
s3 = boto3.client('s3', region_name='us-east-1')

# Passos principais:
try:
    response = s3.get_object(Bucket=bucket_name, Key=input_file_key)
    df = pd.read_csv(response['Body'], encoding='utf-8', sep=';')
    print("Arquivo carregado com sucesso!")
except ClientError as e:
    raise Exception(f"Erro ao obter o arquivo do S3: {e}")
```
**Função Utilizada:** Leitura de arquivo com `get_object` (interação com S3) e `read_csv` (pandas) para carregar os dados no DataFrame.  

**Obs**: utilizando as funções acima, tivemos otimização sem a necessidade de salvar o arquivo localmente para depois realizar a leitura e criação do dataframe. O tamanho da base original propiciou realizar isso com o equipamento que tenho com suas limitações de processamento. Noutro cenário poderia ser diferente.

### Tratamento dos Dados

#### Conversão de Valores

```python
print("Realizando tratamentos nos dados...")
df = df.fillna('NULL')  # Substituição de células em branco
```
**Função Utilizada:** `fillna` (pandas) - Grupo de funções de conversão, utilizado para substituir valores nulos por "NULL".

<br/>

#### Manipulação de Strings

```python
df = df.replace(to_replace=r'\{ñ class\}|\{ñ Class\}', value='NULL', regex=True)
df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)  # Remoção de espaços
```
**Funções Utilizadas:** `replace` e `apply` - Grupo de funções de strings para substituições e remoção de espaços extras.

<br/>

#### Conversão de Datas

```python
date_columns = ['Data Acidente', 'Data Nascimento']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')
```
**Função Utilizada:** `to_datetime` - Conversão de datas para o formato brasileiro, pertencente ao grupo de funções de manipulação de datas.

<br/>

#### Criação de Colunas

```python
if 'Data Nascimento' in df.columns and 'Data Acidente' in df.columns:
    df['Idade no momento do acidente'] = ((df['Data Acidente'] - df['Data Nascimento']).dt.days // 365).astype('Int64')
```
**Função Utilizada:** Cálculo de idade com base em datas utilizando operações entre colunas de DataFrame, grupo de funções de manipulação de datas.

<br/>

### Salvando Dados Tratados no S3

```python
output_treated_key = 'outputs/CAT202306-tratado.csv'
s3.put_object(Bucket=bucket_name, Key=output_treated_key, Body=df.to_csv(index=False, sep=';', encoding='utf-8'))
print("Arquivo tratado salvo no S3!")
```
**Função Utilizada:** `put_object` - Salva o arquivo tratado de volta ao S3.

<br/>

## Filtragem e Geração de Indicadores

### Filtragem

```python
# Exemplo de filtro por condições lógicas
filtered_df = df[df['CBO'].notnull() & (df['Relevância'] > df['Relevância'].mean())]
```
**Função Utilizada:** Expressões lógicas (`&`, `notnull`) - Grupo de cláusulas lógicas para aplicar filtros nas amostras.

<br/>

### Indicadores

```python
# Estatísticas e distribuição por sexo
sexo_distribuicao = df.groupby('Sexo').size().reset_index(name='Contagem')
```
**Função Utilizada:** `groupby` e `size` - Grupo de funções de agregação para calcular estatísticas e distribuição.

<br/>

### Exportação

```python
# Salvando indicadores em Excel
with pd.ExcelWriter('indicadores.xlsx') as writer:
    sexo_distribuicao.to_excel(writer, sheet_name='Distribuição Sexo', index=False)

s3.upload_file('indicadores.xlsx', bucket_name, 'outputs/indicadores.xlsx')
print("Indicadores exportados para Excel!")
```
**Função Utilizada:** `to_excel` (pandas) e `upload_file` (boto3) - Exportação e envio ao S3.

<br/>

### Evidências da análise realizada e outputs gerados com suscesso!

![bucket criado com sucesso via terminal](../evidencias/desafio/4-analise_gerada_terminal.png)

![bucket criado com sucesso no console](../evidencias/desafio/2-outputs.png)


<br/>

---

<br/>

# 📌 Considerações finais sobre a Sprint 05

Essa sprint foi desafiadora, especialmente pela integração entre Python, pandas e AWS S3, através do `AWSCLI` (AWS Command-line Interfae ). Com ela, pude aprofundar meus conhecimentos em:

- Manipulação de grandes volumes de dados utilizando pandas.
- Utilização do boto3 para interagir com a AWS.
- Criação de pipelines de dados eficientes e escaláveis.
- Pude seguir na utilização de python reforçando suas sintaxes, especilamente no uso de cada um dos grupos direcionados como obrigatórios nas instruções do desafio proposto, conforme a tabela abaixo.  

<br/>

| **Tipo de Função**                        | **Função no Código**                             | **Breve Explicação**                                                                 |
|-------------------------------------------|-------------------------------------------------|-------------------------------------------------------------------------------------|
| Função de Conversão (4.4)                 | `fillna` e `to_datetime`                        | Tratamento de valores nulos e conversão de dados para formato específico.          |
| Função de String (4.6)                    | `replace` e `apply`                             | Manipulação e limpeza de strings, incluindo substituição e remoção de espaços.     |
| Função de Data (4.5)                      | `to_datetime` e cálculo de diferença de datas   | Conversão de colunas de texto para datas e cálculo de idade.                       |
| Função Condicional (4.3)                  | Cálculo de médias e aplicação de condições      | Criação de rótulos e condições baseadas em cálculos específicos.                   |
| Cláusula com Operadores Lógicos (4.1)     | `&`, `notnull`                                  | Filtragem de dados utilizando expressões lógicas para selecionar amostras.         |
| Funções de Agregação (4.2)                | `groupby`, `size` e agregações diversas         | Agrupamento e cálculo de estatísticas descritivas.                                 |


<br/>

Estou animado para continuar aprendendo e aplicar esses conhecimentos em projetos futuros. 🚀
