import csv

#criação da função
def processar_notas():
    with open('estudantes.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file) #leitura do csv
        
        #criação da variável que guardará os resultados finais, em formato de lista
        resultados = []

        for row in reader:
            #extração do nome do aluno e conversão das notas para uma lista de inteiros
            nome = row[0] #posição 0 de cada linha (primeira coluna)
            notas = list(map(int, row[1:]))  #conversão das notas para inteiros usando map, criando uma lista única (notas) da 2a. coluna até o final
            
            #ordenação das notas em decrescente e seleção das três maiores
            maiores_notas = sorted(notas, reverse=True)[:3]
            
            #média das três maiores notas com duas casas decimais
            media = round(sum(maiores_notas) / 3, 2)
            
            #formatação da variaǘel resultados, com as informações/ listas que desejamos
            resultados.append((nome, maiores_notas, media))

        #ordenação pelo nome
        resultados.sort(key=lambda x: x[0])  # Ordenação pelo nome

        #impressão dos resultados com f string
        for nome, maiores_notas, media in resultados:
            print(f"Nome: {nome} Notas: {maiores_notas} Média: {media}")

#execução da função toda, já incluso o print()
processar_notas()
