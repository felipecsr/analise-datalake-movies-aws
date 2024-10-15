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

