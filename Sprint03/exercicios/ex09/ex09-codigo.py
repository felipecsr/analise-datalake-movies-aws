#criação de 3 listas com itens, sendo str e int
primeirosNomes = ['Joao', 'Douglas', 'Lucas', 'José']
sobreNomes = ['Soares', 'Souza', 'Silveira', 'Pedreira']
idades = [19, 28, 25, 31]

#impressão utilizando as listas a partir da sua posição dentro das listas
for index, valor in enumerate(primeirosNomes, start=0):
    print(f'{index} - {primeirosNomes[index]} {sobreNomes[index]} está com {idades[index]} anos')