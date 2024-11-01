#criação da classe Avião
class Aviao:
    def __init__(self, modelo, velocidade_maxima, capacidade): #utilização do construtor dos objetos, sendo a cor sempre azul para todos objetos
        self.modelo = modelo
        self.velocidade_maxima = velocidade_maxima
        self.capacidade = capacidade
        self.cor = "azul"

#criação dos objetos com seus atributos próprios - excluindo cor que sempre é azul
aviao1 = Aviao("BOIENG456", 1500, 400)
aviao2 = Aviao("Embraer Praetor 600", 863, 14)
aviao3 = Aviao("Antonov An-2", 258, 12)

#montagem de uma lista, com os objetos e seus atributos
lista = [aviao1, aviao2, aviao3]

#impressão em looping, para cada objeto da lista e seus respectivos atributos
for aviao in lista:
    print(f"O avião de modelo {aviao.modelo} possui uma velocidade máxima de {aviao.velocidade_maxima} km/h, capacidade para {aviao.capacidade} passageiros e é da cor {aviao.cor}.")