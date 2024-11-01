# Cria lista de 50 números aleatórios e desordenados e sem duplicidades
import random
random_list = random.sample(range(500), 50)

# Percorre a lista e extrai os valores mínimo e máximo
valor_minimo = min(random_list)
valor_maximo = max(random_list)

# Média = Total de todos itens dividido pela quantidade de itens da lista
media = sum(random_list) / len(random_list)

# Mediana = soma os dois números centrais da lista e divide por dois, após a ordenação
sorted_list = sorted(random_list)
mid1 = sorted_list[len(sorted_list) // 2 - 1]
mid2 = sorted_list[len(sorted_list) // 2]
mediana = (mid1 + mid2) / 2

print(f"Media: {media}, Mediana: {mediana}, Mínimo: {valor_minimo}, Máximo: {valor_maximo}")