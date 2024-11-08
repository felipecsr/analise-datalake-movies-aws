from functools import reduce

#Utilização de map map para converter a lista de lançamentos em valores postivios e negativos, dentro da função de calculo do saldo

def calcula_saldo(lancamentos) -> float:
    valores_ajustados = map(lambda x: x[0] if x[1] == 'C' else -x[0], lancamentos)
    
    #reduce para somar todos os valores ajustados
    saldo_final = reduce(lambda x, y: x + y, valores_ajustados)
    
    return saldo_final

#lancamentos fornecidos no exercicio
lancamentos = [ (200, 'D'), (300, 'C'), (100, 'C')]

resultado = calcula_saldo(lancamentos)
print(resultado)
