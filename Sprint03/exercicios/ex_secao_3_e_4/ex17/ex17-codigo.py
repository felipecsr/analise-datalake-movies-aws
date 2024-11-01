# Criação da função para dividir listas em 3 partes iguais
def dividir_lista_em_tres(lista):
    tamanho_parte = len(lista) // 3 #calcula o tamanho de cada uma das 3 partes iguais
    
    # Divide a lista em três partes usando fatiamento
    parte1 = lista[:tamanho_parte]
    parte2 = lista[tamanho_parte:2*tamanho_parte]
    parte3 = lista[2*tamanho_parte:]
    
    # Retorna as três partes como uma tupla
    return parte1, parte2, parte3

#Aplicação da função com a lista fornecida
lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
parte1, parte2, parte3 = dividir_lista_em_tres(lista)

print(parte1, parte2, parte3)
