lista = ['maça', 'arara', 'audio', 'radio', 'radar', 'moto']


for item in lista:
    if item == item[::-1]:
        print('A palavra: {} é um palíndromo' .format(item))
    else:
        print('A palavra: {} não é um palíndromo' .format(item))
