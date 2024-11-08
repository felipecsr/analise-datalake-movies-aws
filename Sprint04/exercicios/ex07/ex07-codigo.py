def pares_ate(n: int):
    for i in range(2, n + 1, 2):  # Inicia em 2 e vai até n, com passo de 2
        yield i  # Retorna o número par e pausa a função
