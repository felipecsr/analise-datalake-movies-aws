SELECT
	tbvendas.estado, 
    tbvendas.nmpro,
	ROUND(AVG(tbvendas.qtd),4) as quantidade_media
    
from tbvendas

WHERE tbvendas.status = 'Concluído'

group by tbvendas.estado, tbvendas.nmpro
ORDER BY tbvendas.estado, tbvendas.nmpro ASC