#criação de lista de numeros armazenada na variavel numeros
numeros = list(range (3, 6))

#loop para percorrer a lista verificando de numero par ou impar, e respectiva impressão como resposta
for item_list in numeros:
    if item_list % 2 == 0:
        print ('Par: {}' .format (item_list))
    else:
        print ('Ímpar: {}' .format (item_list))