#importação de biblioteca JSON
import json

#utilizei sem o caminho, exatamente como funcionou no ex da Udemy - porém para funcionar aqui no VSCode precisei colocar o caminho relativo
with open('person.json', 'r') as arquivo:
    dados = json.load(arquivo)

print(dados)



# # Exercício com Caminho Relativo do JSON
# # se quiser testar, pode selecionar o bloco e dar ctrl + / para tirar o # de comentários 

# import json
# with open('PB-FELIPE-REIS/Sprint03/exercicios/ex11/person.json', 'r') as arquivo:
#     dados = json.load(arquivo)
# print(dados)