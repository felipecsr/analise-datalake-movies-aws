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


