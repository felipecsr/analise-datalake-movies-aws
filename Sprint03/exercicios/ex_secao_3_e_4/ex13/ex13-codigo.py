# Abrindo TXT e realizando leitura
with open('arquivo_texto.txt', 'r') as arquivo:
    texto = arquivo.read()

# Imprimindo o conteúdo do arquivo - detalhe especial para o end=' ' que permitiu avançar, por conta do comportamento padrão da funcao print, que quebra linha por padrão.
print(texto, end='')