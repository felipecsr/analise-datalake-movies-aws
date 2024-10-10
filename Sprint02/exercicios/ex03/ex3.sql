SELECT COUNT(l.cod) AS quantidade, e.nome, en.estado, en.cidade
FROM livro l
JOIN editora e ON l.editora = e.codEditora
JOIN endereco en ON e.endereco = en.codEndereco
GROUP BY e.nome, en.estado, en.cidade
ORDER BY quantidade DESC;