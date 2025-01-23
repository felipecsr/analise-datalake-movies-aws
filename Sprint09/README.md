## 💻 Visão geral da sprint 

Nesta sprint 09, avançamos para a quarta etapa de construção do **Desafio Final do Programa de Bolsas da Compass UOL** - a etapa 4 de 5.

O foco principal nesta sprint seguiu sendo o uso do `Apache Spark`, explorando sua capacidade de manipulação de dados em larga escala e integração com o *Data Lake*. Entre os destaques estão o processamento distribuído e a análise avançada, utilizando tanto Python quanto SQL.
<br/>
<br/>  

# 📜 Certificados
Nesta sprint 09, não houve nenhum curso obrigatório com disponibilização de certificados.
<br/>  
<br/>  
  
# 🧠 Desafio
#### Camada Refined: Transformação de dados e Modelagem Multi-dimensional  

Nesta etapa do desafio, o foco principal foi a criação da  **camada Refined** no *Data Lake*, utilizando o `AWS Glue` para processar e transformar dados provenientes da camada Trusted. O objetivo foi garantir que os dados estejam limpos, confiáveis e prontos para análises em ferramentas como o `AWS Athena` e na próxima sprint, `Aws Quicksight`.

A abordagem envolveu o uso de `Apache Spark` no Glue para desenvolver *jobs* que consolidam os dados da **camada Refined** em um conjunto de tabelas, dentro de uma modelagem multi-dimensional - persistido os dados ainda em `parquet` no *bucket* do `AWS S3`. Com essa estrutura, o *Data Lake* será fortalecido para suportar consultas e visualizações otimizadas nas próximas fases do projeto.

[Confira o 'readme' do desafio aqui!](../Sprint09/desafio/README.md)