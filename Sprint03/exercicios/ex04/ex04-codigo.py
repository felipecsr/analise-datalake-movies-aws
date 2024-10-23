lista = list(range(0,101))

resultado = [numero for numero in lista if 
          numero > 1 
          and 
          all(numero % i != 0 for i in range(2, numero -1))]

for numero in resultado:
    print (numero)