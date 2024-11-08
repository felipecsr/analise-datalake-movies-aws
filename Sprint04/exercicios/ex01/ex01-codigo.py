#abre o arquivo number.txt no modo de leitura, aplicando função map para trannsformar a lista de números em inteiros, de forma iterativa
with open("number.txt", "r") as file:
    numeros = list(map(int, file.readlines()))

#filtra os números pares usando filter
pares = list(filter(lambda x: x % 2 == 0, numeros))

#ordena os números pares em ordem decrescente e pega os 5 maiores
maiores_pares = sorted(pares, reverse=True)[:5]

#Soma dos 5 maiores pares
soma_maiores_pares = sum(maiores_pares)

print(maiores_pares) #Lista dos 5 maiores pares
print(soma_maiores_pares) #Soma dos 5 maiores pares


