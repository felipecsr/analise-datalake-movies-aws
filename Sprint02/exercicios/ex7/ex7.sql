SELECT autor.nome
from autor
LEFT JOIN livro on autor.codautor = livro.autor
group by autor.nome
HAVING COUNT(livro.titulo) = 0;