#criação de listas a e b
a = [1, 1, 2, 3, 5, 8, 14, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

#criação das variaveis c e d que com set extraem os valores unicos das listas a e b
c = set (a)
d = set (b)

#impressão de c e d, no formato de lista, e seguidas na mesma 'expressão' de resultado
print (list(c & d))