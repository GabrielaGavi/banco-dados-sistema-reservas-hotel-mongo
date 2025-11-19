SELECT
    r.id_reserva,
    h.nome AS nome_hospede,
    q.tipo AS tipo_quarto,
    r.data_checkin,
    r.data_checkout,
    r.valor_total,
    r.status
FROM reserva r
JOIN hospede h ON r.cpf = h.cpf
JOIN quarto q ON r.numero_quarto = q.numero_quarto
ORDER BY r.data_checkin
