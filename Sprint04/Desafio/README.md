
# 🎯 Objetivo

Este README documenta a resolução do desafio da Sprint 04.  
Trata-se da execução de scripts em linguagem Python, através de Containers criados pela ferramenta Docker 🐋. 

O Desafio está dividido em 3 etapas:

<br/>

# Etapa 1 

## Averiguação e entendimento do script "carguru.py"

``` python
import random

carros = ['Chevrolet Agile','Chevrolet C-10','Chevrolet Camaro','Chevrolet Caravan','Chevrolet Celta','Chevrolet Chevette','Chevrolet Corsa','Chevrolet Covalt','Chevrolet D-20','Chevrolet Monza','Chevrolet Onix','Chevrolet Opala','Chevrolet Veraneio','Citroën C3','Fiat 147','Fiat Argo','Fiat Cronos','Fiat Mobi','Fiat Panorama','Ford Corcel','Ford Escort','Ford F-1000','Ford Ka','Ford Maverick','Honda City','Honda Fit','Hyundai Azera','Hyundai HB20','Hyundai IX-35','Hyundai Veloster','Peugeot 2008','Peugeot 206','Peugeot 208','Peugeot 3008','Peugeot 306','Peugeot 308','Renault Kwid','Renault Logan','Renault Sandero','Renault Twingo','Renault Zoe','Toyota Etios','Toyota Yaris ','Volkswagen Apolo','Volkswagen Bora','Volkswagen Brasilia   ','Volkswagen Fusca','Volkswagen Gol','Volkswagen Kombi','Volkswagen Parati','Volkswagen Passat','Volkswagen Polo','Volkswagen SP2','Volkswagen Santana','Volkswagen Voyage','Volkswagen up!']

random_carros = random.choice(carros)

print('Você deve dirigir um '+ random_carros)
```
O script acima foi fornecido já pronto para ser executado, no desafio.
Seu funcionamento é simples: através da`função `random`, o script imprime uma frase que ao final seleciona um item da lista "carros" para completar a sentença, de forma aleatória.

## Criação de Dockerfile

```dockerfile
FROM python

WORKDIR /PB-FELIPE-REIS/Sprint04/Desafio/Etapa1

COPY carguru.py app/carguru.py

# RUN - sem necessidade dessa camada já que no executável py, nao pede a importação de nenhuma dependência/ biblioteca

COPY . .

EXPOSE 80

CMD [ "python", "carguru.py" ]
```
O arquivo Dockerfile se organiza por camadas, que ficam armazenadas em *cache* após a primeira execução. Vamos comentar cada uma das camadas, função e entendimento:  

**FROM**: é a camada que pede a informação da `imagem base` que pode ser observada no hub de imagens oficial da plataforma Docker. É importante sempre que seja utilizada uma imagem oficial, com bons números de avaliação e utilização pela comunidade.

**WORKDIR**: é a camada que criará diretórios dentro do container, conforme especificado na sintaxe.

**COPY**: essa é a camada que copia arquivos do seu ambiente local para dentro do container, conforme a estrutura de diretório da camada acima, e ainda com a possibilidade de apontamento de subpastas.

**RUN**: é a camada onde podemos solicitar a instalação/ importação de depedências para além da imagem base, como no caso do Python, novas bibliotecas que não sejam as nativdas - através, por exemplo, de comando `pip`.

**EXPOSE**: camada que trata de escolha da porta que o container deixará exposta para comunicação com o "mundo exterior", já que o container é fechado para segurança. Essa camada, apenas escolhe a porta que ficará exposta, sendo que a porta do ambiente local que fará a comunicação com o container é escolhida com sintaxe digitada no momento de criação do container.

**CMD**: nessa última camada, com todas escolhas de parâmetros acima, chega o momento da linha de comando que o terminal - dentro do container recém criado/ executado - realizará a execução; tal qual a minha própria digitação no terminal local.

## Criação de Imagem

## Criação de Container


# Etapa 2

## Avaliação se um container já utilizado, pode ser reutilziado


# Etapa 3

## Criação de script Python - Conversão de string em hexadecimal

## Criação de Dockerfile

## Criação de Imagem

## Criação de container - com flags -i e -t


<br/>

# 📌 Considerações finais sobre a sprint 04

Essa sprint, para mim, foi até aqui a mais desafiadora. 💪
Senti-me parcialmente pronto para as lógicas a serem aplicadas, seja no tema de ETL, seja nos aspectos mais analíticos dos dados. No entanto, ao lidar com a linguagem de programação e a possibilidade de orientação a objetos, percebi que meu poder de abstração precisa ser ainda mais desenvolvido. E achei ótima essa oportunidade! 🌱

A sprint foi cansativa, mas extremamente recompensadora, especialmente no que diz respeito ao desenvolvimento do mindset do cientista de dados. 🧠✨

Compreendi também a importância do ETL, um trabalho que, aparentemente, é mais designado aos Engenheiros de Dados. Com tratamentos bem realizados, a chance de realizar análises de dados com mais qualidade e assertividade é proporcionalmente maior! 📊

Por fim, senti uma inclinação maior pela análise de dados do que pela parte de engenharia. É algo que vou manter em mente e observar mais de perto conforme avanço na bolsa de estudos e nas próximas sprints. 🔍

---