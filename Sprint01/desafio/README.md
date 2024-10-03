# 🎯 Objetivo

**Objetivo do desafio**: O desafio principal envolve o processamento de um arquivo CSV, onde as tarefas incluem extrair informações, consolidá-las em outro arquivo, gerar arquivos ZIP, remover arquivos antigos e criar pastas, tudo utilizando comandos em Shell com agendamento através do serviço de execução de tarefas do Linux.  

**Desafio secundário**: Além disso, foi necessário subir a estrutura de pastas para um repositório no GitHub, realizar versionamentos e garantir que o time técnico tenha acesso ao repositório, onde poderão corrigir os exercícios e observar a organização do projeto.  

**Contexto**: Este desafio, dentro da Sprint, agregou valor ao meu aprendizado, pois me permitiu executar tarefas básicas sem interfaces gráficas, utilizando terminal e IDEs, bem como criar scripts, automatizar processos simples e gerenciar repositórios Git com versionamento.


# 🤔 Planejamento  

**Planejamento e Estratégia**: Inicialmente, planejei a execução das tarefas dividindo o desafio em etapas menores e organizando tudo em um kanban simples no Trello (backlog, doing, blocked, done). No entanto, ao longo da Sprint, percebi que era necessário ajustar o planejamento conforme surgiam novas necessidades e desafios. Entendi que um planejamento perfeito é difícil de se fazer logo de primeira, e a revisão constante dos planos foi crucial para manter o projeto organizado e no prazo.  

**Organização no GitHub**: Criei minha conta no GitHub e configurei a estrutura de pastas no repositório, o que trouxe um grande alívio. Essa organização prévia me permitiu focar quase exclusivamente no desenvolvimento do script, sem a preocupação de refazer pastas ou ajustar a estrutura posteriormente. Ter as pastas organizadas conforme o solicitado pelo time técnico foi essencial para garantir que o script estivesse bem estruturado desde o início.  

**Foco nos Cursos**: Comecei os cursos de Linux e Git simultaneamente, mas logo percebi que seria mais eficiente focar primeiro no Linux, dado o prazo das quatro execuções do script agendadas para as 15h27 em dias diferentes. Decidi finalizar as tarefas relacionadas ao Linux e a criação dos scripts antes de concluir o curso de Git. Felizmente, o que aprendi de Git até aquele momento foi suficiente para a organização do repositório, permitindo-me completar as etapas sem atrasos.  


# 🛠️ Execução

### ➡️1️⃣ Script - "Processamento de Vendas" - Linha a Linha

```bash
#!/bin/bash
```
- Aprendi que essa sintaxe indica o início de todo script em Shell, com o interpretador Bash. 

---

```bash
# criar subdiretorio vendas dentro do diretorio ecommerce
mkdir -p vendas
```
- O comando `mkdir -p` cria o diretório `vendas` dentro do diretório atual `ecommerce'`. O parâmetro `-p` garante que, se o diretório já existir, o comando não retornará erro.

---

```bash
# copiar o arquivo csv proposto no exercicio para dentro do subdiretorio vendas
cp /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/dados_de_vendas.csv  /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas
```
- O comando `cp` copia o arquivo CSV do caminho descrito (`dados_de_vendas.csv`) para o diretório `vendas`. Esse arquivo contém os dados que foram processados no desafio.  
_**Obs**: o contepudo deste arquivo foi alterado manualmente para a 2a., 3a. e 4a. execuções do script._

---

```bash
# criar subdiretorio backup dentro do diretorio vendas
mkdir -p vendas/backup
```
- O comando cria o subdiretório `backup` dentro da pasta `vendas`, que será usado para armazenar os arquivos CSV copiados e processados.

---

```bash
# copiar o arquivo csv do diretório de vendas para o subdiretorio backup
cp /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/dados_de_vendas.csv  /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup
```
- Aqui, o arquivo `dados_de_vendas.csv` é copiado da pasta `vendas` para a pasta `backup`.

---

```bash
# renomear arquivo de vendas para dados-yyyymmdd.csv, sendo a data da execução do script
mv /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/dados_de_vendas.csv /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv
```
- O comando `mv` renomeia o arquivo copiado na pasta `backup`. Ele acrescenta uma data no formato `yyyymmdd` ao nome do arquivo.  
_**Obs1**: o comando `mv` também pode servir para mover arquivos ou diretórios para outros diretórios, o que não foi o caso aqui, seja na intenção e porconseguinte a sintaxe._  
_**Obs2**: a data utilizada com o comando, foi sempre a da execução do script / data de sistema._


---

```bash
# criar arquivo txt para relatório com conteúdo indicado no desafio
cat <<EOL > "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/relatorio_vendas-$(date +%Y%m%d-%H%M).txt"
```
- O comando `cat <<EOL` cria um arquivo de texto chamado `relatorio_vendas-yyyymmdd-HHMM.txt` (com data e hora, como a linha acima) contendo informações sobre a execução do script.  
_**Obs**: colocar a data também neste arquivo foi importante para que com execuções sucessivas, o arquivo não fosse sobrescrito._  


---

```bash
Relatório de Vendas
===================

Data do sistema operacional: 
$(date +"%Y/%m/%d %H:%M")
```
- Esse bloco de texto cria o cabeçalho do relatório com a data e a hora do sistema, formatada no estilo `AAAA/MM/DD HH:MM`.

---

```bash
Primeiro registro de venda:
$(head -n 2 "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv" | tail -n 1)
```
- O comando `head -n 2` obtém as duas primeiras linhas do arquivo CSV (cabeçalho e o primeiro registro de vendas). O comando `tail -n 1` extrai apenas a ultima linha dessas duas que foram capturadas (ignorando o cabeçalho e extraindo o primeiro registro - que é o que nos interessa nesse bloco).

---

```bash
Último registro de venda:
$(tail -n 1 "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv")
```
- O comando `tail -n 1` extrai a última linha do arquivo CSV, correspondente ao último registro de venda, que foi incluído nos relatórios.

---

```bash
Quantidade total de itens diferentes vendidos: 
$(cut -d',' -f2 "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv" | tail -n +2 | sort -u | wc -l)
```
- O comando `cut` extrai uma determinada seção do csv, e o parâmetro `-d',` explicita que o delimitador do arquivo é a virgula, e o parâmetro `-f2` acena que a extração deve ser da coluna 2 - a coluna com os produtos vendidos no nosso caso. O comando `sort -u` organiza e remove duplicatas, e `wc -l` conta quantos itens únicos estão nessa seleção - o que pra nós é a resposta da pergunta de itens únicos vendidos.

---

```bash
As primeiras 10 linhas do arquivo (incluindo o cabeçalho):
$(head -n 10 "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv")
EOL
```
- O comando `head -n 10` exibe as primeiras 10 linhas do arquivo CSV, incluindo o cabeçalho, e insere essa informação no relatório.

---

```bash
# Zipar o arquivo CSV da pasta backup (sem incluir o caminho completo)
zip -q "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).zip" "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv"
```
- O comando `zip -q` compacta o arquivo CSV dentro da pasta `backup` para economizar espaço.  
_**Obs**: neste caso também foi importante que o zip tenha a data ao final do nome do arquivo para que não sobrescrevesse a cada execução do script._  

---

```bash
# remover o arquivo csv da pasta backup (que ficará com o relatorio txt e o csv, agora zipado)
rm "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv"
```
- Após a criação do arquivo compactado, o arquivo CSV original é removido da pasta `backup`, deixando apenas o arquivo zipado e o relatório `.txt`.

---

```bash
# remover o arquivo csv da pasta vendas (que ficará sem arquivos, apenas subdiretorio backup)
rm "/home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/dados_de_vendas.csv"
```
- Finalmente, o arquivo CSV também é removido da pasta `vendas`, deixando o diretório limpo, exceto pela pasta `backup`.

---
### ➡️2️⃣ Agendamento do executável
Foi utilizado o serviço nativo do Linux `contrab`, que funciona com uma sintaxe simples de data/horário seguido do comando que será executado de forma automática.

```bash
27 15 01 10 * cd /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce && bash processamento_de_vendas.sh > /home/fcsr/logs/processamento_de_vendas.log 2>&1

27 15 02 10 * cd /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce && bash processamento_de_vendas.sh > /home/fcsr/logs/processamento_de_vendas.log 2>&1

27 15 03 10 * cd /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce && bash processamento_de_vendas.sh > /home/fcsr/logs/processamento_de_vendas.log 2>&1

27 15 04 10 * cd /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce && bash processamento_de_vendas.sh > /home/fcsr/logs/processamento_de_vendas.log 2>&1

27 15 05 10 * cd /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce && bash processamento_de_vendas.sh > /home/fcsr/logs/processamento_de_vendas.log 2>&1

27 15 06 10 * cd /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce && bash processamento_de_vendas.sh > /home/fcsr/logs/processamento_de_vendas.log 2>&1

```
- A sintaxe do agendamento no `crontab` segue o padrão: minutos, hora, dia, mês e ano. Utilizei o `*` para indicar qualquer ano.
- Em seguida, utilizei o comando `cd` para acessar o diretório `ecommerce`, onde o script `processamento_de_vendas.sh` está salvo.
- O operador `&&` foi adicionado para conectar o comando de mudança de diretório com o próximo comando.
- O script é então executado com o comando `bash processamento_de_vendas.sh`.
- Para facilitar a identificação de erros, redirecionei a saída de log para o arquivo `processamento_de_vendas.log`. Isso foi importante, pois tive dificuldades ao configurar o `crontab`, e o log me ajudou a localizar os problemas que ocorriam durante a execução.
- De forma resumida, o serviço de agendamento executou o script todos os dias entre 01 e 06 de outubro, sempre às 15h27.
_**Obs**: Embora tenham sido configurados 6 agendamentos, apenas 4 arquivos de vendas foram processados, conforme solicitado no desafio. Isso ocorreu porque nem todos os agendamentos foram executados corretamente, exigindo tentativas adicionais até que as 4 extrações fossem concluídas com sucesso._  

---
### ➡️3️⃣ Script - "Consolidador de Relatórios de Venda"

```bash
# Concatenar todos os arquivos 'relatorio*.txt' de um diretório específico no arquivo 'relatorio_final.txt'
cat /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/relatorio_vendas*.txt > /home/fcsr/Documentos/Nabucodonossor-workspace/PB-FELIPE-REIS/Sprint01/desafio/ecommerce/vendas/backup/relatorio_final.txt
```
- Este segundo script é simple: ele varreu a pasta `backup` atrás dos relatórios de venda em `txt`(com o parâmetro * para buscar qualquer arquivo que inicie com "relatorio_de_venda" sem importar o final do nome do arquivo/ data descrita). Ao localizar estes arquivos, que são 4, o script gera um novo `txt`e empilha os conteudos.

---
# 🔁 Seções Relacionadas

[Confira o conteúdo da pasta exercícios com os scripts](/PB-FELIPE-REIS/Sprint01/exercicios/)  

[Confira o conteúdo da pasta evidências com prints de alguns momentos](/PB-FELIPE-REIS/Sprint01/evidencias/)


