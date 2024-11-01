#criação de lista de numeros sob a variavel lista
lista = list(range(0,101))

#criação da variavel resultado que armazena numeros que obedecem o if
resultado = [numero for numero in lista if 
          numero > 1 
          and 
          all(numero % i != 0 for i in range(2, numero -1))]

#impressão do resultado, percorrendo a lista
for numero in resultado:
    print (numero)