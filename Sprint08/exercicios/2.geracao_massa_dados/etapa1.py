import random

# Gerar uma lista com 250 números inteiros aleatórios
# O intervalo de números pode ser ajustado conforme necessário (aqui está entre 1 e 1000)
numeros_aleatorios = [random.randint(1, 1000) for _ in range(250)]

# Aplicar o método reverse para inverter a lista
numeros_aleatorios.reverse()

# Imprimir o resultado
print("Lista invertida:")
print(numeros_aleatorios)
