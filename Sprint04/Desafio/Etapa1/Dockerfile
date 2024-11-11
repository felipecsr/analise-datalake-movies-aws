FROM python

WORKDIR /PB-FELIPE-REIS/Sprint04/Desafio/Etapa1

COPY carguru.py app/carguru.py

# RUN - sem necessidade dessa camada já que no executável py, nao pede a importação de nenhuma dependência/ biblioteca

COPY . .

EXPOSE 80

CMD [ "python", "carguru.py" ]