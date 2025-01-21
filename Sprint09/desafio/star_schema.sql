-- Tabela Fato: Fato_Principal
CREATE TABLE Fato_Principal (
    id_fato SERIAL PRIMARY KEY,
    id___imdb VARCHAR(20),
    imdb_id___tmdb VARCHAR(20),
    id_tmdb___tmdb VARCHAR(20),
    tituloPincipal___imdb VARCHAR(255),
    tituloOriginal___imdb VARCHAR(255),
    title___tmdb VARCHAR(255),
    anoLancamento___imdb INT,
    release_decade INT,
    release_date___tmdb DATE,
    tempoMinutos___imdb INT,
    budget___tmdb DECIMAL(18, 2),
    revenue___tmdb DECIMAL(18, 2),
    ROI DECIMAL(10, 2),
    financial_result VARCHAR(50),
    vote_average___tmdb DECIMAL(3, 1),
    notaMedia___imdb DECIMAL(3, 1),
    numeroVotos___imdb INT,
    popularity___tmdb DECIMAL(10, 2),
    id_idioma INT,
    id_genero INT,
    id_artista INT,
    id_producao INT,
    id_colecao INT,
    id_detalhes INT,
    FOREIGN KEY (id_idioma) REFERENCES Dim_Idioma(id_idioma),
    FOREIGN KEY (id_genero) REFERENCES Dim_Genero(id_genero),
    FOREIGN KEY (id_artista) REFERENCES Dim_Artista(id_artista),
    FOREIGN KEY (id_producao) REFERENCES Dim_Produção(id_producao),
    FOREIGN KEY (id_colecao) REFERENCES Dim_Coleção(id_colecao),
    FOREIGN KEY (id_detalhes) REFERENCES Dim_Detalhes(id_detalhes)
);

-- Tabela Dimensão: Dim_Genero
CREATE TABLE Dim_Genero (
    id_genero SERIAL PRIMARY KEY,
    genero___imdb VARCHAR(100),
    main_genre___tmdb VARCHAR(100)
);

-- Tabela Dimensão: Dim_Artista
CREATE TABLE Dim_Artista (
    id_artista SERIAL PRIMARY KEY,
    nomeArtista___imdb VARCHAR(255),
    generoArtista___imdb VARCHAR(50),
    personagem___imdb VARCHAR(255),
    anoNascimento___imdb INT,
    anoFalecimento___imdb INT,
    profissao___imdb VARCHAR(100),
    titulosMaisConhecidos___imdb TEXT
);

-- Tabela Dimensão: Dim_Produção
CREATE TABLE Dim_Produção (
    id_producao SERIAL PRIMARY KEY,
    production_companies__name VARCHAR(255),
    production_companies__id VARCHAR(50),
    production_countries__iso_3166_1 VARCHAR(5),
    production_countries__name VARCHAR(100)
);

-- Tabela Dimensão: Dim_Coleção
CREATE TABLE Dim_Coleção (
    id_colecao SERIAL PRIMARY KEY,
    collection_id___tmdb VARCHAR(50),
    collection_name___tmdb VARCHAR(255)
);

-- Tabela Dimensão: Dim_Detalhes
CREATE TABLE Dim_Detalhes (
    id_detalhes SERIAL PRIMARY KEY,
    overview___tmdb TEXT,
    poster_path___tmdb VARCHAR(255),
    backdrop_path___tmdb VARCHAR(255),
    adult___tmdb BOOLEAN,
    status___tmdb VARCHAR(50),
    tagline___tmdb VARCHAR(255),
    video___tmdb BOOLEAN,
    source_file___tmdb VARCHAR(255),
    homepage___tmdb VARCHAR(255)
);

-- Tabela Dimensão: Dim_Idioma
CREATE TABLE Dim_Idioma (
    id_idioma SERIAL PRIMARY KEY,
    original_language___tmdb VARCHAR(5),
    spoken_languages__iso_639_1 VARCHAR(5),
    spoken_languages__name VARCHAR(100)
);
