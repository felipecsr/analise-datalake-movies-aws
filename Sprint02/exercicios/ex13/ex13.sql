SELECT
    tbestoqueproduto.cdpro,
    tbvendas.nmcanalvendas,
    tbvendas.nmpro,
    SUM(tbvendas.qtd) AS quantidade_vendas

FROM tbvendas
	JOIN tbestoqueproduto ON tbestoqueproduto.cdpro = tbvendas.cdpro

WHERE tbvendas.nmcanalvendas IN ('Matriz', 'Ecommerce')
	AND tbvendas.status = 'Concluído'

GROUP BY tbestoqueproduto.cdpro, tbvendas.nmcanalvendas 
ORDER BY quantidade_vendas ASC
LIMIT 10;