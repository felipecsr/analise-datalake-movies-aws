# Escreva uma função que recebe uma string de números separados por vírgula
# e retorne a soma de todos eles. 
# Depois imprima a soma dos valores.
# A string deve ter valor  "1,3,4,6,10,76"

# Criação da função
def soma_numeros (string_numeros):
    lista_numeros = string_numeros.split(",") #fatia a string em várias strings, com o separador ','

    lista_inteiros = [int(numero) for numero in lista_numeros] #transforma strings em inteiros

    return sum(lista_inteiros) #soma os inteiros

string_n = "1,3,4,6,10,76" #define a string inicial/ info fornecida pelo exercício
resultado = soma_numeros(string_n) #chama a função criada acima para a string informada acima
print(resultado)