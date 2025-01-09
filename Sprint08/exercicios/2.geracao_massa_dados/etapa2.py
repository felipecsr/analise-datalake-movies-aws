import csv  # Biblioteca para manipular arquivos CSV

# Passo 1: Declarar e inicializar a lista com 20 nomes de animais
animais = [
    "Cachorro", "Gato", "Elefante", "Tigre", "Leão", "Zebra", "Girafa", "Pinguim", "Urso", "Cavalo", 
    "Coelho", "Jacaré", "Peixe", "Coruja", "Arraia", "Golfinho", "Raposa", "Cervo", "Camelo", "Lobo"
]

# Passo 2: Ordenar a lista em ordem crescente
animais_ordenados = sorted(animais)

# Passo 3: Iterar sobre os itens da lista e imprimir cada um
[print(animal) for animal in animais_ordenados]  # List comprehension para iterar e imprimir

# Passo 4: Armazenar o conteúdo da lista em um arquivo CSV
with open("animais.csv", mode="w", newline="", encoding="utf-8") as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    for animal in animais_ordenados:
        writer.writerow([animal])  # Escrevendo um item por linha no CSV

print("Lista salva no arquivo 'animais.csv'.")
