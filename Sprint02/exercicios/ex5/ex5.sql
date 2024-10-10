SELECT autor.nome
FROM autor
JOIN livro ON autor.codautor = livro.autor
JOIN editora ON livro.editora = editora.codeditora
JOIN endereco ON editora.endereco = endereco.codendereco
WHERE endereco.estado NOT IN ('PARANÁ', 'RIO GRANDE DO SUL', 'SANTA CATARINA')
GROUP by autor.nome
ORDER BY autor.nome asc;
