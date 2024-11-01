#criação de lista de str sob a variavel lista
lista = ['maça', 'arara', 'audio', 'radio', 'radar', 'moto']

#laço que percorre a lista verificando/ imprimindo quais palavras são palíndromos, ou seja, que a palavra na ordem inversa de letras é igual a ordem inicial 
for item in lista:
    if item == item[::-1]:
        print('A palavra: {} é um palíndromo' .format(item))
    else:
        print('A palavra: {} não é um palíndromo' .format(item))
