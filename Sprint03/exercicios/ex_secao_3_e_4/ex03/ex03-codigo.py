#criação de lista de numeros sob a variável lista
lista = list(range(0,21))

#criação de uma segunda lista de numeros (apenas pares), a partir da lista anterior, sob a variavel lista_par
lista_par = [numeros_pares for numeros_pares in lista if numeros_pares % 2 == 0 ]

#impressão dos numeros pares, percorrendo a lista_par
for numero_pares in lista_par:
    print(numero_pares)