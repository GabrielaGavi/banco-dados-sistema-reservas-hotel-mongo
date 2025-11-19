SELECT
    status,
    COUNT(*) AS total_reservas,
    SUM(valor_total) AS soma_valores
FROM reserva
GROUP BY status
ORDER BY total_reservas DESC
