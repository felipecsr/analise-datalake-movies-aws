primeirosNomes = ['Joao', 'Douglas', 'Lucas', 'José']
sobreNomes = ['Soares', 'Souza', 'Silveira', 'Pedreira']
idades = [19, 28, 25, 31]

for index, valor in enumerate(primeirosNomes, start=0):
    print(f'{index} - {primeirosNomes[index]} {sobreNomes[index]} está com {idades[index]} anos')