# Função para imprimir parâmetros não-nomeados (tupla) e nomeados (dicionário)

def imprimir (*args, **kwargs): # *indica todos elementos
    for arg in args:
        print(arg)
    for valor in kwargs.values(): #aqui apenas values, conforme o exercício solicitou
        print(valor)

# chamamento da função com o conjunto de dados
imprimir(1, 3, 4, 'hello', parametro_nomeado='alguma coisa', x=20)
