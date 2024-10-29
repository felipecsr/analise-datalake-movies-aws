# Criação da função para extrair valores, retirar valores duplicados, criar lista com itens únicos
def obter_valores_unicos(dicionario):
    valores = list(dicionario.values())
    valores_unicos = list(set(valores))
    return valores_unicos

# Declaração de variável, o dicionário speed informado no exercicio
speed = {'jan': 47, 'feb': 52, 'march': 47, 'April': 44, 'May': 52, 'June': 53, 'july': 54, 'Aug': 44, 'Sept': 54}

# Chamada da função acima, com o dicionario informado, imprimindo a lista de itens unicos ao final
resultado = obter_valores_unicos(speed)
print(resultado)
