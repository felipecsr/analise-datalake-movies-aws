#Criação da superclasse Pássaro
class Passaro:
    def voar(self):
        print("Voando...") # Método único para as duas subclasses
        
    def emitir_som(self):
        pass  # Método a ser sobrescrito pelas subclasses

#criação de subclasse Pato com método próprio de emissão de som
class Pato(Passaro):
    def emitir_som(self):
        print("Pato emitindo som...")
        print("Quack Quack")

#criação de subclasse Pardal com método próprio de emissão de som
class Pardal(Passaro):
    def emitir_som(self):
        print("Pardal emitindo som...")
        print("Piu Piu")


print("Pato")
pato = Pato()
pato.voar()
pato.emitir_som()

print("Pardal")
pardal = Pardal()
pardal.voar()
pardal.emitir_som()