SELECT
	tbdependente.cddep,
    tbdependente.nmdep,
    tbdependente.dtnasc,
    round(sum(tbvendas.qtd * tbvendas.vrunt),2) as valor_total_vendas
    
from tbdependente
	left join tbvendedor on tbvendedor.cdvdd = tbdependente.cdvdd
    LEFT JOIN tbvendas on tbvendedor.cdvdd = tbvendas.cdvdd

WHERE tbvendas.status = 'Concluído'

group by tbvendedor.nmvdd
ORDER BY valor_total_vendas ASC
limit 1