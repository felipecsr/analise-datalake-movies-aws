SELECT autor.codautor, autor.nome, COUNT (livro.titulo) as quantidade_publicacoes
from livro
join autor on autor.codautor = livro.autor
group by autor.nome
order by quantidade_publicacoes DESC
LIMIT 1;