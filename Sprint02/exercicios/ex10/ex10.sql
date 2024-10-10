select 
	tbvendedor.nmvdd as vendedor,
    sum(tbvendas.qtd * tbvendas.vrunt) as valor_total_vendas,
    ROUND((sum(tbvendas.qtd * tbvendas.vrunt) * tbvendedor.perccomissao / 100),2) as comissao
	
FROM tbvendas 
JOIN tbvendedor on tbvendas.cdvdd = tbvendedor.cdvdd

WHERE tbvendas.status = 'Concluído'

GROUP by vendedor
order by comissao DESC;