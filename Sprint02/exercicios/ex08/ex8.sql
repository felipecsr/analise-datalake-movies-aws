select tbvendedor.cdvdd, tbvendedor.nmvdd
from tbvendedor
LEFT JOIN tbvendas on tbvendedor.cdvdd = tbvendas.cdvdd
group by tbvendedor.nmvdd
order by COUNT (tbvendas.cdven) desc
LIMIT 1;