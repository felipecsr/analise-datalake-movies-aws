lista = list(range(0,21))

lista_par = [numeros_pares for numeros_pares in lista if numeros_pares % 2 == 0 ]

for numero_pares in lista_par:
    print(numero_pares)