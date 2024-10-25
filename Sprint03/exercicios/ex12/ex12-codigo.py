# Função para percorrer a lista, aplicar a funcao2 e criar uma nova_lista
def my_map(lista, funcao2):
    nova_lista = []
    for elemento in lista:
        nova_lista.append(funcao2(elemento))
    return nova_lista

# Função que eleva um número ao quadrado
def potencia_de_2(x):
    return x ** 2

# Lista de entrada
lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Função my_map aplicada
resultado = my_map(lista, potencia_de_2)

print(resultado)
