-- Habilitar foreign_keys no SQLite (opcional, mas recomendado)
PRAGMA foreign_keys = ON;

-- (1) TABELAS DE DIMENSÃO
DROP TABLE IF EXISTS dim_artista;
CREATE TABLE dim_artista (
    id_artista           INTEGER  NOT NULL PRIMARY KEY,
    nomeArtista          TEXT,
    artista_genero       TEXT,
    artista_profissao    TEXT,
    artista_outrosTitulos TEXT,
    artista_ano_nascimento   INTEGER,
    artista_ano_falecimento  INTEGER
);

DROP TABLE IF EXISTS dim_colecao;
CREATE TABLE dim_colecao (
    id_colecao                INTEGER NOT NULL PRIMARY KEY,
    collection_id             INTEGER,
    collection_name           TEXT,
    colecao_quantidade_filmes INTEGER
);

DROP TABLE IF EXISTS dim_detalhes;
CREATE TABLE dim_detalhes (
    id_detalhes   INTEGER NOT NULL PRIMARY KEY,
    overview      TEXT,
    poster_path   TEXT,
    backdrop_path TEXT,
    homepage      TEXT,
    status        TEXT,
    tagline       TEXT,
    video         TEXT,
    source_file   TEXT
);

DROP TABLE IF EXISTS dim_genero;
CREATE TABLE dim_genero (
    id_genero   INTEGER NOT NULL PRIMARY KEY,
    genero_item TEXT
);

DROP TABLE IF EXISTS dim_idioma;
CREATE TABLE dim_idioma (
    id_idioma          INTEGER NOT NULL PRIMARY KEY,
    original_language  TEXT
);

DROP TABLE IF EXISTS dim_pais;
CREATE TABLE dim_pais (
    id_pais       INTEGER NOT NULL PRIMARY KEY,
    pais_producao TEXT
);

DROP TABLE IF EXISTS dim_produtora;
CREATE TABLE dim_produtora (
    id_produtora   INTEGER NOT NULL PRIMARY KEY,
    nome_produtora TEXT
);

-- (2) TABELA FATO PRINCIPAL
DROP TABLE IF EXISTS fato_principal;
CREATE TABLE fato_principal (
    id_fato                    INTEGER NOT NULL PRIMARY KEY,
    f_filme_id_imdb            TEXT,
    f_filme_id_tmdb            INTEGER,
    f_filme_tituloOriginal     TEXT,
    f_filme_tituloPincipal     TEXT,
    f_tempo_anoLancamento      INTEGER,
    f_tempo_dataLancamento     DATE,
    f_tempo_minutos            INTEGER,

    f_aval_notaMedia_imdb      REAL,
    f_aval_numeroVotos_imdb    INTEGER,
    f_aval_notaMedia_tmdb      REAL,
    f_aval_popularity_tmdb     REAL,
    f_filme_adult              INTEGER, -- 0 ou 1 se preferir
    f_filme_genero_analise     TEXT,

    f_fin_orcamento            INTEGER,
    f_fin_receita              INTEGER,
    f_fin_resultado            REAL,
    f_fin_roi                  REAL,
    f_release_decade           INTEGER,
    f_fin_lucro_por_minuto     REAL,
    f_fin_tempo_votos_por_minuto REAL,

    -- FK para colecao
    id_colecao    INTEGER REFERENCES dim_colecao(id_colecao),
    -- FK para detalhes
    id_detalhes   INTEGER REFERENCES dim_detalhes(id_detalhes),
    -- FK para idioma
    id_idioma     INTEGER REFERENCES dim_idioma(id_idioma)

    /* 
       Observação:
       Se você preferir "NOT NULL" em FK, inclua. 
       Aqui deixamos sem NOT NULL 
       pois alguns filmes podem não ter coleção/detalhes/idioma.
    */
);

-- (3) TABELAS DE PONTE (galaxy / link tables)

-- 3.1 Tabela link Filme x Artista
DROP TABLE IF EXISTS fact_film_artist;
CREATE TABLE fact_film_artist (
    id_fato    INTEGER NOT NULL,
    id_artista INTEGER NOT NULL,
    PRIMARY KEY (id_fato, id_artista),
    FOREIGN KEY (id_fato) REFERENCES fato_principal(id_fato),
    FOREIGN KEY (id_artista) REFERENCES dim_artista(id_artista)
);

-- 3.2 Tabela link Filme x Gênero
DROP TABLE IF EXISTS fact_film_genero;
CREATE TABLE fact_film_genero (
    id_fato   INTEGER NOT NULL,
    id_genero INTEGER NOT NULL,
    PRIMARY KEY (id_fato, id_genero),
    FOREIGN KEY (id_fato)   REFERENCES fato_principal(id_fato),
    FOREIGN KEY (id_genero) REFERENCES dim_genero(id_genero)
);

-- 3.3 Tabela link Filme x País
DROP TABLE IF EXISTS fact_film_pais;
CREATE TABLE fact_film_pais (
    id_fato INTEGER NOT NULL,
    id_pais INTEGER NOT NULL,
    PRIMARY KEY (id_fato, id_pais),
    FOREIGN KEY (id_fato) REFERENCES fato_principal(id_fato),
    FOREIGN KEY (id_pais) REFERENCES dim_pais(id_pais)
);

-- 3.4 Tabela link Filme x Produtora
DROP TABLE IF EXISTS fact_film_produtora;
CREATE TABLE fact_film_produtora (
    id_fato      INTEGER NOT NULL,
    id_produtora INTEGER NOT NULL,
    PRIMARY KEY (id_fato, id_produtora),
    FOREIGN KEY (id_fato)      REFERENCES fato_principal(id_fato),
    FOREIGN KEY (id_produtora) REFERENCES dim_produtora(id_produtora)
);

/*  
   FIM DO SCRIPT

   Para visualizar as relações graficamente em uma ferramenta
   que suporte diagrama ER, basta importar este script
   e habilitar "foreign_keys=ON" no SQLite.
*/
