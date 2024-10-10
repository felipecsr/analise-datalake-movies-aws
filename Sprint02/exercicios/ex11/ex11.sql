SELECT
	tbvendas.cdcli,
    tbvendas.nmcli,
    ROUND(SUM(tbvendas.qtd * tbvendas.vrunt),2) as gasto
    
FROM tbvendas
group by tbvendas.cdcli
ORDER BY gasto DESC
LIMIT 1;