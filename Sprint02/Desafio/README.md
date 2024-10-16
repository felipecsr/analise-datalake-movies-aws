
# 🎯 Objetivo

Este README documenta a criação de tabelas e views para dois tipos de modelagem de dados: **relacional** e **dimensional**.   
O objetivo aqui é explicar o racional e implementação de cada modelo, destacando ao final similaridades nos esquemas mas também suas diferenças teóricas.

---

# 📊 Modelagens

### 1️⃣ Modelagem Relacional

Para desenvolver o modelo relacional, analisei todas as colunas da tabela fornecida no desafio, organizando-as conforme os níveis de normalização exigidos. Depois de rascunhar a estrutura inicial, segui para o código e criei as tabelas de acordo com o esquema relacional. 

De forma um pouco mais detalhada, a normalização passou por entender os menores valores, pensar como telas de um ERP e separá-los pelas chaves primárias já informadas (o que facilitou a escolha das tabelas); também ligá-los através de chaves estrageiras.

#### SQL - Modelagem Relacional

```sql
-- Criar tabela Cliente
CREATE TABLE Cliente (
    idCliente INT PRIMARY KEY,
    nomeCliente VARCHAR(100),
    cidadeCliente VARCHAR(100),
    estadoCliente VARCHAR(50),
    paisCliente VARCHAR(50)
);

-- Criar tabela Carro
CREATE TABLE Carro (
    idCarro INT PRIMARY KEY,
    kmCarro INT,
    classiCarro VARCHAR(50),
    marcaCarro VARCHAR(50),
    modeloCarro VARCHAR(50),
    anoCarro INT
);

-- Criar tabela Combustivel
CREATE TABLE Combustivel (
    idcombustivel INT PRIMARY KEY,
    tipoCombustivel VARCHAR(50)
);

-- Criar tabela Vendedor
CREATE TABLE Vendedor (
    idVendedor INT PRIMARY KEY,
    nomeVendedor VARCHAR(100),
    sexoVendedor SMALLINT,
    estadoVendedor VARCHAR(50)
);

-- Criar tabela Locacao
CREATE TABLE Locacao (
    idLocacao INT PRIMARY KEY,
    idCliente INT,
    idCarro INT,
    idcombustivel INT,
    idVendedor INT,
    dataLocacao DATETIME,
    horaLocacao TIME,
    qtDiaria INT,
    vlrDiaria DECIMAL(10, 2),
    dataEntrega DATE,
    horaEntrega TIME,
    FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente),
    FOREIGN KEY (idCarro) REFERENCES Carro(idCarro),
    FOREIGN KEY (idcombustivel) REFERENCES Combustivel(idcombustivel),
    FOREIGN KEY (idVendedor) REFERENCES Vendedor(idVendedor)
);
```

A representação visual deste esquema relacional ficou a seguinte:

![visualização do esquema relacional após normalização](/PB-FELIPE-REIS/Sprint02/evidencias/normalizacao-mod-relacional.png)  
**OBS**: a `tb_locacao` à direita da imagem foi a tabela dada de início no desafio, ou seja, a origem para a normalização e relacionamento.

**OBS'**: nas sintaxes de criação das novas tabelas, já há a definição do formato de cada coluna, como hora, data, 2 casas decimais, inteiros, texto, etc.

---

### 2️⃣ Modelagem Dimensional (Esquema Estrela)

No esquema estrela, temos uma tabela de **fatos** que registra os eventos (neste caso, locações), enquanto as tabelas de **dimensão** descrevem entidades como clientes, carros, combustíveis e vendedores.

#### SQL - Modelo Dimensional (através de `VIEWS`)

```sql
-- View: Fato Locacao
CREATE VIEW Fato_Locacao AS
SELECT 
    l.idLocacao,
    l.idCliente,
    l.idCarro,
    l.idcombustivel,
    l.idVendedor,
    l.dataLocacao,
    l.horaLocacao,
    l.qtDiaria,
    l.vlrDiaria,
    l.dataEntrega,
    l.horaEntrega
FROM Locacao l;

-- View: Dimensão Cliente
CREATE VIEW Dim_Cliente AS
SELECT 
    c.idCliente,
    c.nomeCliente,
    c.cidadeCliente,
    c.estadoCliente,
    c.paisCliente
FROM Cliente c;

-- View: Dimensão Carro
CREATE VIEW Dim_Carro AS
SELECT 
    car.idCarro,
    car.kmCarro,
    car.classiCarro,
    car.marcaCarro,
    car.modeloCarro,
    car.anoCarro
FROM Carro car;

-- View: Dimensão Combustível
CREATE VIEW Dim_Combustivel AS
SELECT 
    comb.idcombustivel,
    comb.tipoCombustivel
FROM Combustivel comb;

-- View: Dimensão Vendedor
CREATE VIEW Dim_Vendedor AS
SELECT 
    v.idVendedor,
    v.nomeVendedor,
    v.sexoVendedor,
    v.estadoVendedor
FROM Vendedor v;
```
  
A representação visual deste esquema dimensional ficou a seguinte:

![visualização do esquema dimensional - estrela](/PB-FELIPE-REIS/Sprint02/evidencias/mod-dimensional_estrela.png)

---

## 📝 Similaridades e Diferenças Entre as Modelagens

Embora estejamos trabalhando com duas modelagens diferentes, o resultado final do SQL acabou ficando bastante parecido.  
Isso se deve ao fato de que as tabelas no modelo relacional foram bem normalizadas, e no esquema dimensional, as views espelham diretamente essas tabelas, o que manteve a estrutura organizada de forma semelhante.

A grande diferença entre os dois modelos está no propósito e na forma de uso:  

- na **modelagem relacional**, o foco é a normalização, com o objetivo de reduzir redundâncias e organizar os dados em entidades bem definidas, garantindo consistência e integridade ao longo do tempo.;   
- na **modelagem dimensional**, o foco é otimizar consultas analíticas e agregações, separando eventos (fatos) das entidades descritivas (dimensões), o que facilita análises rápidas e eficientes, especialmente em ambientes, por exemplo de BI.  

Mesmo com a semelhança no SQL, o uso de views no esquema dimensional serve justamente para simplificar a análise de dados, enquanto no modelo relacional o foco é a manutenção da integridade e consistência da informação.

---
