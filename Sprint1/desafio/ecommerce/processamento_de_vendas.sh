#!/bin/bash

# criar subdiretorio vendas dentro do diretorio ecommerce
mkdir -p vendas

# copiar o arquivo csv proposto no exercicio para dentro do subdiretorio vendas
cp /home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/dados_de_vendas.csv  /home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas

# criar subdiretórico backup dentro do diretorio vendas
mkdir -p vendas/backup

#copiar o arquivo csv do diretório de vendas para o subdiretorio backup
cp /home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/dados_de_vendas.csv  /home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup

#renomear arquivo de vendas para dados-yyyymmdd.csv, sendo a data da execução do script
mv /home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup/dados_de_vendas.csv /home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv

#criar arquivo txt para relatório com conteúdo indicado no desafio
cat <<EOL > "/home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup/relatorio_vendas-$(date +%Y%m%d-%H%M).txt"

Relatório de Vendas
===================

Data do sistema operacional: 
$(date +"%Y/%m/%d %H:%M")

Primeiro registro de venda:
$(head -n 2 "/home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv" | tail -n 1)

Último registro de venda:
$(tail -n 1 "/home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv")

Quantidade total de itens diferentes vendidos: 
$(cut -d',' -f2 "/home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv" | tail -n +2 | sort -u | wc -l)

As primeiras 10 linhas do arquivo (incluindo o cabeçalho):
$(head -n 10 "/home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv")
EOL

# Zipar o arquivo CSV da pasta backup (sem incluir o caminho completo)
zip -q "/home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).zip" "/home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv"

#remover o arquivo csv da pasta backup (que ficará com o relatorio txt e o csv, agora zipado)
rm "/home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv"

#remover o arquivo csv da pasta vendas (que ficará sem arquivos, apenas subdiretorio backup)
rm "/home/fcsr/Documentos/Nabucodonossor-workspace/bolsa-compass-sprints/Sprint1/desafio/ecommerce/vendas/dados_de_vendas.csv"


