def maiores_que_media(conteudo: dict) -> list:
    #extração dos valores do dicionário 'conteudo' já em float
    valores_produtos = list(conteudo.values())
    
    #média dos valores
    media_valores = sum(valores_produtos) / len(valores_produtos)
    
    #criação de variável lista para armazenar os produtos que estiverem acima da média
    produto_valor_acima_med = []
    
    #filtro dos produtos acima da média
    for produto, preco in conteudo.items():
        if preco > media_valores:
            #recebe como tupla, produto e valor, os itens que estiverem acima da média
            produto_valor_acima_med.append((produto, preco))
    
    #ordenação da lista pelo preço em ordem crescente
    produto_valor_acima_med.sort(key=lambda x: x[1])
    
    return produto_valor_acima_med

#lista de preços do exemplo
conteudo = {
    "arroz": 4.99,
    "feijão": 3.49,
    "macarrão": 2.99,
    "leite": 3.29,
    "pão": 1.99
}

#chamada da função e armazenamento do resultado
resultado = maiores_que_media(conteudo)

print("Produtos acima da média:", resultado)
