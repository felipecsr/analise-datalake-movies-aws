SELECT 
	livro.cod,
    livro.titulo,
    autor.codautor,
    autor.nome,
    livro.valor,
    editora.codeditora,
    editora.nome
    
FROM livro
join autor on autor.codautor = livro.autor
join editora on editora.codeditora = livro.editora

order by livro.valor DESC
limit 10;