# Criação da classe (molde) Lâmpada, com definição inicial de atributo e método
class Lampada:
    def __init__(self, ligada):
        self.ligada = ligada

# Altera o método (estado da lampada) para 'ligado'
    def liga(self):
        self.ligada = True 

# Altera o método (estado da lampada) para 'desligado'
    def desliga(self):
        self.ligada = False

# Verifica o método (estado da lampada) no momento
    def esta_ligada(self):
        return self.ligada

# Criação de objeto 'lamp' para a classe 'Lampada' (condição inicial desligada)
lamp = Lampada(True)

# Utilização do método para ligar a lampada, e consulta do estado atual
lamp.liga()
print("A lâmpada está ligada?", lamp.esta_ligada())

# Utilização do método para desligar a lampada, e consulta do estado atual
lamp.desliga()
print("A lâmpada ainda está ligada?", lamp.esta_ligada())
