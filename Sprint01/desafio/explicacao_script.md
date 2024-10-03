
# Explicação do Script - Linha a Linha

```bash
#!/bin/bash
```
- **Explicação**: Esta linha indica que o script será executado pelo interpretador `bash`, informando ao sistema qual programa utilizar para rodar o script.

---

```bash
# criar subdiretorio vendas dentro do diretorio ecommerce
mkdir -p vendas
```
- **Explicação**: O comando `mkdir -p` cria o diretório `vendas` dentro do diretório atual. A opção `-p` garante que, se o diretório já existir, o comando não retornará erro.

---

```bash
# copiar o arquivo csv proposto no exercicio para dentro do subdiretorio vendas
cp /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/dados_de_vendas.csv  /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas
```
- **Explicação**: O comando `cp` copia o arquivo CSV do caminho especificado (`dados_de_vendas.csv`) para o diretório `vendas`. Esse arquivo contém os dados que serão processados no desafio.

---

```bash
# criar subdiretorio backup dentro do diretorio vendas
mkdir -p vendas/backup
```
- **Explicação**: O comando cria o subdiretório `backup` dentro da pasta `vendas`, que será usado para armazenar os arquivos CSV copiados e processados.

---

```bash
# copiar o arquivo csv do diretório de vendas para o subdiretorio backup
cp /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/dados_de_vendas.csv  /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup
```
- **Explicação**: Aqui, o arquivo `dados_de_vendas.csv` é copiado da pasta `vendas` para a pasta `backup`, criando uma cópia de segurança.

---

```bash
# renomear arquivo de vendas para dados-yyyymmdd.csv, sendo a data da execução do script
mv /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/dados_de_vendas.csv /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv
```
- **Explicação**: O comando `mv` move e renomeia o arquivo copiado na pasta `backup`. Ele acrescenta a data atual ao nome do arquivo, no formato `yyyyMMdd` (ano, mês, dia), garantindo uma organização cronológica dos arquivos.

---

```bash
# criar arquivo txt para relatório com conteúdo indicado no desafio
cat <<EOL > "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/relatorio_vendas-$(date +%Y%m%d-%H%M).txt"
```
- **Explicação**: O comando `cat <<EOL` cria um arquivo de texto chamado `relatorio_vendas-yyyymmdd-HHMM.txt` contendo informações sobre a execução do script. A data e a hora são automaticamente adicionadas ao nome do relatório.

---

```bash
Relatório de Vendas
===================

Data do sistema operacional: 
$(date +"%Y/%m/%d %H:%M")
```
- **Explicação**: Esse bloco de texto cria o cabeçalho do relatório com a data e a hora do sistema, formatada no estilo `AAAA/MM/DD HH:MM`.

---

```bash
Primeiro registro de venda:
$(head -n 2 "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv" | tail -n 1)
```
- **Explicação**: O comando `head -n 2` obtém as duas primeiras linhas do arquivo CSV (cabeçalho e o primeiro registro de vendas). O comando `tail -n 1` extrai apenas o primeiro registro de venda, que é então inserido no relatório.

---

```bash
Último registro de venda:
$(tail -n 1 "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv")
```
- **Explicação**: O comando `tail -n 1` extrai a última linha do arquivo CSV, correspondente ao último registro de venda, que será incluído no relatório.

---

```bash
Quantidade total de itens diferentes vendidos: 
$(cut -d',' -f2 "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv" | tail -n +2 | sort -u | wc -l)
```
- **Explicação**: O comando `cut` seleciona a segunda coluna do CSV (supondo que seja a coluna de itens vendidos), `sort -u` organiza e remove duplicatas, e `wc -l` conta quantos itens únicos foram vendidos.

---

```bash
As primeiras 10 linhas do arquivo (incluindo o cabeçalho):
$(head -n 10 "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv")
EOL
```
- **Explicação**: O comando `head -n 10` exibe as primeiras 10 linhas do arquivo CSV, incluindo o cabeçalho, e insere essa informação no relatório.

---

```bash
# Zipar o arquivo CSV da pasta backup (sem incluir o caminho completo)
zip -q "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).zip" "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv"
```
- **Explicação**: O comando `zip -q` compacta o arquivo CSV dentro da pasta `backup` para economizar espaço. O arquivo zipado recebe o nome com a data, no formato `backup-dados-yyyymmdd.zip`.

---

```bash
# remover o arquivo csv da pasta backup (que ficará com o relatorio txt e o csv, agora zipado)
rm "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv"
```
- **Explicação**: Após a criação do arquivo compactado, o arquivo CSV original é removido da pasta `backup`, deixando apenas o arquivo zipado e o relatório `.txt`.

---

```bash
# remover o arquivo csv da pasta vendas (que ficará sem arquivos, apenas subdiretorio backup)
rm "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/dados_de_vendas.csv"
```
- **Explicação**: Finalmente, o arquivo CSV também é removido da pasta `vendas`, deixando o diretório limpo, exceto pela pasta `backup`.

---

