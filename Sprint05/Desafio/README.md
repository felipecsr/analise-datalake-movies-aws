
Quantidade	Tipo de Função	Exemplo de Implementação	Usando no ETL			Objetivo
1	Função de Conversão (4.4)	PEGADA DE ETL: TRATAR OS NULLS, CONVERTER BINÁRIOS (SIM NAO PARA NUMERO), OU CONVERTER TEXTO PARA DATA, OU CONVERTER DATA PARA FORMATO ESPECÍFICO	Tratamento	em branco para NULL	conversão de formato de data	
1	Função de String (4.6)	pegada etl: BUSCA E EXTRAÇÃO DE PALAVRAS (CHAVES), CONCATENAR OU DIVIDIR, SUBSTITUIÇÃO, REMOÇÃO ESPAÇOS, CONVERSÃO DE MAIUSCULAS/ MINUSCULAS,	Tratamento	{ñ class} para NULL	remoção de espaços	
						
1	Função de Data (4.5)	DATADIF, OU PEGAR O DIA DA SEMANA DO ACIDENTE, 	Computação	criação de coluna de idade no momento do acidente		
						
1	Função Condicional (4.3)	CRIAR UMA COLUNA COM ALGUM ROTULO, COMO FAIXA ETARIA (SOBRE IDADE), OU ALGUM TIPO DE ROTULAÇÃO PARA ACIDENTE GRAVE, MODERADO, SIMPLES ... EM UM OU MAIS COLUNAS COM CONDICIONAIS	Computação	Calculo da média da amostragem e o rótulo se acima true or false		criar um tótulo que possibilite trabalharmos com a metade mais expressiva da base de dados, desprezando o restante
			Computação	Calculo do % de aparição na base do CBO, tendo o % ao lado		faremos um filtro do top 10, ou 20, algo assim
						
1 > 2	Cláusula com Operadores Lógicos (4.1)	AND, OR, NOT, XOR (uma e apenas uma condição)	Filtro	filtro de TRUE para "acima da média %, com o objetivo de captar o que é mais estatisticamente relevante na amostragem	Filtrar NOT NULL no campo CBO	Do que restou realizar um filtro com o TOP10 % da coluna de relevancia estatistica de CBO
						
2	Funções de Agregação (4.2)	SOMA, MÉDIA, MEDIANA, CONTAGEM, MINIMO, MAXIMO, DESVIO PADRÃO >> pode ser utilizada no geral ou num grupo (com GROUPBY)	Anaĺise			