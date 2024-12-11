WITH decadas AS (
    SELECT
        nome,
        total,
        ano,
        FLOOR((ano - 1950) / 10) * 10 + 1950 AS decada
    FROM meubanco.nomes_csv
    WHERE ano >= 1950
),
ContagemPorDecada AS (
    SELECT
        decada,
        nome,
        SUM(total) AS total_uso
    FROM Decadas
    GROUP BY decada, nome
),
RankedNomes AS (
    SELECT
        decada,
        nome,
        total_uso,
        RANK() OVER (PARTITION BY decada ORDER BY total_uso DESC) AS rank
    FROM ContagemPorDecada
)
SELECT
    decada,
    nome,
    total_uso
FROM RankedNomes
WHERE rank <= 3
ORDER BY decada, rank;