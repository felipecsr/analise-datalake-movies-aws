-- Criar tabela DimCliente
CREATE TABLE DimCliente (
    idCliente INT PRIMARY KEY,
    nomeCliente VARCHAR(100),
    cidadeCliente VARCHAR(100),
    estadoCliente VARCHAR(50),
    paisCliente VARCHAR(50)
);

-- Criar tabela DimCarro
CREATE TABLE DimCarro (
    idCarro INT PRIMARY KEY,
    kmCarro INT,
    classiCarro VARCHAR(50),
    marcaCarro VARCHAR(50),
    modeloCarro VARCHAR(50),
    anoCarro INT
);

-- Criar tabela DimCombustivel
CREATE TABLE DimCombustivel (
    idcombustivel INT PRIMARY KEY,
    tipoCombustivel VARCHAR(50)
);

-- Criar tabela DimVendedor
CREATE TABLE DimVendedor (
    idVendedor INT PRIMARY KEY,
    nomeVendedor VARCHAR(100),
    sexoVendedor SMALLINT,
    estadoVendedor VARCHAR(50)
);

-- Criar tabela FatoLocacao
CREATE TABLE FatoLocacao (
    idLocacao INT PRIMARY KEY,
    idCliente INT,
    idCarro INT,
    idcombustivel INT,
    idVendedor INT,
    dataLocacao DATE,
    horaLocacao TIME,
    qtDiaria INT,
    vlrDiaria DECIMAL(10, 2),
    dataEntrega DATE,
    horaEntrega TIME,
    FOREIGN KEY (idCliente) REFERENCES DimCliente(idCliente),
    FOREIGN KEY (idCarro) REFERENCES DimCarro(idCarro),
    FOREIGN KEY (idcombustivel) REFERENCES DimCombustivel(idcombustivel),
    FOREIGN KEY (idVendedor) REFERENCES DimVendedor(idVendedor)
);
