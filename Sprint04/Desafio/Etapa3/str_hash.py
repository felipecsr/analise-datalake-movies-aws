import hashlib

# Recebe a string via input
input_string = input("Digite uma string: ")

# Gera o hash SHA-1 da string
sha1_hash = hashlib.sha1(input_string.encode()).hexdigest()

# Imprime o hash gerado
print(f"Hash SHA-1: {sha1_hash}")
