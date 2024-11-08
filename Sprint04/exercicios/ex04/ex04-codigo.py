#função + função auxiliar para aplicar a operação
def calcular_valor_maximo(operadores, operandos):
    def aplicar_operacao(op, valores):
        if op == '+':
            return valores[0] + valores[1]
        elif op == '-':
            return valores[0] - valores[1]
        elif op == '*':
            return valores[0] * valores[1]
        elif op == '/':
            return valores[0] / valores[1]
        elif op == '%':
            return valores[0] % valores[1]

    #função map para processar cada operação e calculando o valor máximo
    resultados = map(lambda x: aplicar_operacao(x[0], x[1]), zip(operadores, operandos))
    return max(resultados)

#lista de operadores e operandos forneceida como exemplo
operadores = ['+', '-', '*', '/', '+']
operandos = [(3, 6), (-7, 4.9), (8, -8), (10, 2), (8, 4)]

resultado = calcular_valor_maximo(operadores, operandos)
print("Maior valor:", resultado)
