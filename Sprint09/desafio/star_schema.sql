-- Criação da Dimensão Coleção
CREATE TABLE dim_colecao (
    id_colecao INTEGER PRIMARY KEY,
    collection_id_tmdb INTEGER,
    collection_name_tmdb TEXT
);

-- Criação da Dimensão Produtora
CREATE TABLE dim_produtora (
    id_producao INTEGER PRIMARY KEY,
    company_name_dim TEXT,
    company_id_dim INTEGER
);

-- Criação da Dimensão País
CREATE TABLE dim_pais (
    id_pais INTEGER PRIMARY KEY,
    country_iso_dim TEXT,
    country_name_dim TEXT
);

-- Criação da Dimensão Artista
CREATE TABLE dim_artista (
    id_artista INTEGER PRIMARY KEY,
    nomeArtista_imdb TEXT,
    generoArtista_imdb TEXT,
    personagem_imdb TEXT,
    anoNascimento_imdb INTEGER,
    anoFalecimento_imdb INTEGER,
    profissao_imdb TEXT,
    titulosMaisConhecidos_imdb TEXT
);

-- Criação da Dimensão Gênero
CREATE TABLE dim_genero (
    id_genero INTEGER PRIMARY KEY,
    genero TEXT,
    genre_tmdb TEXT
);

-- Criação da Dimensão Detalhes
CREATE TABLE dim_detalhes (
    id_detalhes INTEGER PRIMARY KEY,
    overview_tmdb TEXT,
    poster_path_tmdb TEXT,
    backdrop_path_tmdb TEXT,
    adult_tmdb BOOLEAN,
    homepage_tmdb TEXT,
    status_tmdb TEXT,
    tagline_tmdb TEXT,
    video_tmdb BOOLEAN,
    source_file_tmdb TEXT,
    popularity_tmdb REAL
);

-- Criação da Dimensão Idioma
CREATE TABLE dim_idioma (
    id_idioma INTEGER PRIMARY KEY,
    original_language TEXT
);

-- Criação da Tabela Fato
CREATE TABLE fato_principal (
    id_fato INTEGER PRIMARY KEY,
    id_imdb TEXT,
    id_tmdb_tmdb INTEGER,
    tituloPrincipal_imdb TEXT,
    tituloOriginal_imdb TEXT,
    anoLancamento_imdb INTEGER,
    release_date_tmdb DATE,
    release_decade INTEGER,
    tempoMinutos_imdb INTEGER,
    notaMedia_imdb REAL,
    numeroVotos_imdb INTEGER,
    vote_average_tmdb REAL,
    budget_tmdb INTEGER,
    revenue_tmdb INTEGER,
    financial_result INTEGER,
    ROI REAL,
    id_colecao INTEGER,
    id_producao INTEGER,
    id_pais INTEGER,
    id_artista INTEGER,
    id_genero INTEGER,
    id_detalhes INTEGER,
    id_idioma INTEGER,
    FOREIGN KEY (id_colecao) REFERENCES dim_colecao (id_colecao),
    FOREIGN KEY (id_producao) REFERENCES dim_produtora (id_producao),
    FOREIGN KEY (id_pais) REFERENCES dim_pais (id_pais),
    FOREIGN KEY (id_artista) REFERENCES dim_artista (id_artista),
    FOREIGN KEY (id_genero) REFERENCES dim_genero (id_genero),
    FOREIGN KEY (id_detalhes) REFERENCES dim_detalhes (id_detalhes),
    FOREIGN KEY (id_idioma) REFERENCES dim_idioma (id_idioma)
);
