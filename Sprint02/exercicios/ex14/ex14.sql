SELECT
	tbvendas.estado,
    ROUND(AVG(tbvendas.qtd * tbvendas.vrunt),2) as gastomedio


from tbvendas

WHERE tbvendas.status = 'Concluído'

GROUP by tbvendas.estado
ORDER by gastomedio DESC;