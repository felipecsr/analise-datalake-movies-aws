# Passo 2: Importação das bibliotecas
import random  # Para gerar números pseudoaleatórios
import names   # Para gerar nomes de pessoas

# Passo 3: Definição dos parâmetros e da semente de aleatoriedade
random.seed(40)  # Define a semente para reproduzir os mesmos resultados
qtd_nomes_unicos = 3000  # Quantidade de nomes únicos
qtd_nomes_aleatorios = 10000000  # Quantidade total de nomes no dataset

# Passo 4: Gerar os nomes aleatórios
aux = []  # Lista para armazenar os nomes únicos
for i in range(qtd_nomes_unicos):
    aux.append(names.get_full_name())  # Gera um nome completo e adiciona na lista

print(f"Gerando {qtd_nomes_aleatorios} nomes aleatórios...")

dados = []  # Lista para armazenar todos os nomes (com repetições)
for i in range(qtd_nomes_aleatorios):
    dados.append(random.choice(aux))  # Adiciona um nome aleatório da lista `aux`

# Passo 5: Salvar os nomes gerados em um arquivo
with open("names_aleatorios.txt", "w") as arquivo:
    for nome in dados:
        arquivo.write(nome + "\n")  # Escreve cada nome em uma nova linha

print("Arquivo 'names_aleatorios.txt' gerado com sucesso!")
