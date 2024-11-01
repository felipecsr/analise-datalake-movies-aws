#criação de lista de numeros a
a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

#criação da variável impares que armazena resultado para o if, armazenando apenas os numeros impares
impares = [numero for numero in a 
           if numero % 2 != 0]

#impressão da lista de numeros impares armazenados na variavel
print (impares)