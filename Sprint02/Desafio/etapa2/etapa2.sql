SELECT
	editora.codeditora,
    editora.nome,
    COUNT (livro.cod) AS QuantidadeLivros

from editora
left join livro on livro.editora = editora.codeditora

GROUP by editora.codeditora
order by QuantidadeLivros DESC
LIMIT 5;