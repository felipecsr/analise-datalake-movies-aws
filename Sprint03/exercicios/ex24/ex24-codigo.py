#criação de classe
class Ordenadora:
    def __init__(self,lista): #atributos da classe Ordenadora
        self.listaBaguncada = lista #atribui a lista fornecida ao atributo listaBaguncada

    def ordenacaoCrescente(self):
        return sorted(self.listaBaguncada) #função para ordenar a listaBaguncada

    def ordenacaoDecrescente(self):
        return sorted(self.listaBaguncada, reverse=True) #função para pegar a lista ordenada e retornar a lista inversa

#chama a classe e métodos aplicando as listas informadas no exercicio    
crescente = Ordenadora([3,4,2,1,5])
decrescente = Ordenadora([9,7,6,8])

#armazena os resultados dos métodos em novas variáveis
resultado_c = crescente.ordenacaoCrescente()
resultado_d = decrescente.ordenacaoDecrescente()

#imprime as variáveis/ resultados esperados
print(resultado_c)
print(resultado_d)