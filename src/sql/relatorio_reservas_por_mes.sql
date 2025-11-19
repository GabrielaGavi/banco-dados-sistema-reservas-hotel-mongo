SELECT
    TO_CHAR(r.criado_em, 'MM/YYYY') AS mes_ano,
    COUNT(*) AS total_reservas,
    SUM(r.valor_total) AS soma_valores
FROM reserva r
GROUP BY TO_CHAR(r.criado_em, 'MM/YYYY')
ORDER BY TO_DATE(TO_CHAR(r.criado_em, 'MM/YYYY'), 'MM/YYYY')
