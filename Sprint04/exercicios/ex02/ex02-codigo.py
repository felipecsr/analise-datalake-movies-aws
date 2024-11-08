#criação da função e definição das vogais (letras a, e, i, o, u) que queremos contar
def conta_vogais(texto: str) -> int:
    vogais = "aeiouAEIOU"
    
    #filtrando só as letras que estão na lista de vogais
    apenas_vogais = list(filter(lambda x: x in vogais, texto))
    
    # Convertendo para lista e contando quantas letras passaram no filtro
    return len(apenas_vogais)

texto = "Qualquer frase que tenha algumas vogais como exemplo para o exercício da Compass UOL"
print(conta_vogais(texto))