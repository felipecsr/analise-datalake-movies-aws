#exercício seção 5 - ETL

#Chamamento da biblioteca OS 
#Tive dificuldade de executar o script, por conta do local e forma da execução. 
#Com ajuda de Chat GPT e Fóruns e Documentação Oficial Python, essa foi a forma como contornei a questão do caminho, e me pareceu uma solução bem interessante, pois o script poderá assim ser executado do próprio diretório, ou direto do root, garantindo que ao clonar o repo, quem fizer a avaliação consiga executar sem problemas.
import os

# Definição caminho_base como o diretório onde o script está localizado
caminho_base = os.path.dirname(__file__) + '/'

# Função para Leitura Geral do CSV
def ler_csv(arquivo):
    dados = []  # Lista para armazenar cada linha como dicionário

    # Abre o arquivo em modo leitura
    with open(arquivo, 'r', encoding='utf-8') as file:
        # Pega o cabeçalho para usar como chave dos dicionários
        cabecalho = file.readline().strip().split(',')
        
        # Percorre cada linha do CSV
        for linha in file:
            valores = []
            acumulador = ""
            dentro_de_aspas = False
            
            # Itera por cada caractere da linha para tratar campos entre aspas com vírgulas internas
            for char in linha:
                if char == '"' and not dentro_de_aspas:
                    dentro_de_aspas = True
                elif char == '"' and dentro_de_aspas:
                    dentro_de_aspas = False
                elif char == ',' and not dentro_de_aspas:
                    valores.append(acumulador.strip())
                    acumulador = ""
                else:
                    acumulador += char
            
            valores.append(acumulador.strip())  # Adiciona o último valor
            
            if len(valores) != len(cabecalho):
                print(f"Linha ignorada por número inconsistente de colunas: {linha}")
                continue
            
            registro = {}
            for i, valor in enumerate(valores):
                coluna = cabecalho[i]
                try:
                    if coluna in ['Total Gross', 'Average per Movie', 'Gross']:
                        registro[coluna] = float(valor)
                    elif coluna == 'Number of Movies':
                        registro[coluna] = int(valor)
                    else:
                        registro[coluna] = valor.strip('"')
                except ValueError:
                    print(f"Erro de conversão na coluna '{coluna}' com o valor '{valor}' na linha: {linha.strip()}")
                    registro[coluna] = None  # Pode ser None ou algum valor padrão para sinalizar erro
            dados.append(registro)
    return dados

# ETAPA01
def etapa01(dados):
    maior_valor = max(dados, key=lambda x: x["Number of Movies"])
    maior_numero_filmes = maior_valor["Number of Movies"]
    atores_maiores = [dado for dado in dados if dado["Number of Movies"] == maior_numero_filmes]
    with open(caminho_base + 'etapa01.txt', 'w', encoding='utf-8') as file:
        for ator in atores_maiores:
            file.write(f"{ator['Actor']} é o ator/atriz com maior número de filmes gravados, sendo {ator['Number of Movies']}.\n")

# ETAPA02: Média de receita de bilheteria bruta de todos os principais filmes
def etapa02(dados):
    total_gross = sum(dado['Gross'] for dado in dados if 'Gross' in dado)
    media_gross = total_gross / len(dados)
    with open(caminho_base + 'etapa02.txt', 'w', encoding='utf-8') as file:
        file.write(f"A média de receita de bilheteria bruta dos principais filmes é: {media_gross:.2f}\n")

# ETAPA03: Ator/Atriz com a maior média de receita por filme (Average per Movie)
def etapa03(dados):
    maior_media = max(dados, key=lambda x: x["Average per Movie"])
    with open(caminho_base + 'etapa03.txt', 'w', encoding='utf-8') as file:
        file.write(f"{maior_media['Actor']} tem a maior média de receita de bilheteria por filme, com {maior_media['Average per Movie']:.2f}.\n")

# ETAPA04: Contagem de aparições de filmes na coluna #1 MOVIE
def etapa04(dados):
    from collections import Counter
    filmes = [dado["#1 Movie"] for dado in dados if "#1 Movie" in dado]
    contagem_filmes = Counter(filmes)
    filmes_ordenados = sorted(contagem_filmes.items(), key=lambda x: (-x[1], x[0]))
    with open(caminho_base + 'etapa04.txt', 'w', encoding='utf-8') as file:
        for filme, quantidade in filmes_ordenados:
            file.write(f"O filme {filme} aparece {quantidade} vez(es) no dataset.\n")

# ETAPA05: Lista de atores ordenada pela receita total de bilheteria (Total Gross)
def etapa05(dados):
    atores_ordenados = sorted(dados, key=lambda x: x["Total Gross"], reverse=True)
    with open(caminho_base + 'etapa05.txt', 'w', encoding='utf-8') as file:
        for ator in atores_ordenados:
            file.write(f"{ator['Actor']} - {ator['Total Gross']:.2f}\n")

# Carregar dados e executar todas as etapas
dados_csv = ler_csv(caminho_base + 'actors.csv')
etapa01(dados_csv)
etapa02(dados_csv)
etapa03(dados_csv)
etapa04(dados_csv)
etapa05(dados_csv)
