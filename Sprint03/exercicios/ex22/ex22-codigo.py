#criação classe Pessoa
class Pessoa:
    def __init__(self, id): #construtor de atributos
        self.id = id       # Atributo público
        self.__nome = None  # Atributo privado

    # Método de acesso para o atributo __nome
    @property
    def nome(self):
        return self.__nome

    # Método de modificação para o atributo __nome
    @nome.setter
    def nome(self, nome):
        self.__nome = nome

pessoa = Pessoa(0)
pessoa.nome = 'Felipe Reis'  # Usa o método de modificação para definir o nome
print(pessoa.nome)  # Usa o método de leitura para acessar o nome
