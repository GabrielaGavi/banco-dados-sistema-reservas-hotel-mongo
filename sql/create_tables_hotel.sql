CREATE TABLE hospede (
    cpf VARCHAR2(14) PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    telefone VARCHAR2(20) NOT NULL,
    data_cadastro DATE NOT NULL
);

CREATE TABLE quarto (
    numero_quarto NUMERIC(4,0) PRIMARY KEY,
    tipo VARCHAR2(20) NOT NULL,
    valor_diaria NUMERIC(10,2) NOT NULL,
    status VARCHAR2(20) NOT NULL CHECK (
        status IN ('Disponível', 'Ocupado', 'Em Limpeza')
    )
);

CREATE TABLE reserva (
    id_reserva NUMERIC(6,0) PRIMARY KEY,
    cpf VARCHAR2(14) NOT NULL,
    numero_quarto NUMERIC(4,0) NOT NULL,
    data_checkin DATE NOT NULL,
    data_checkout DATE NOT NULL,
    qtd_hospedes NUMERIC(2,0) NOT NULL,
    valor_total NUMERIC(10,2) NOT NULL,
    status VARCHAR2(20) NOT NULL CHECK (
        status IN ('Ativa', 'Cancelada', 'Finalizada')
    ),
    criado_em TIMESTAMP DEFAULT SYSTIMESTAMP,
    CONSTRAINT fk_reserva_hospede FOREIGN KEY (cpf)
        REFERENCES hospede(cpf),
    CONSTRAINT fk_reserva_quarto FOREIGN KEY (numero_quarto)
        REFERENCES quarto(numero_quarto)
);

CREATE SEQUENCE reserva_seq
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;