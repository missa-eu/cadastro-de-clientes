
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco VARCHAR(255),
    rede_social VARCHAR(100),
    email VARCHAR(100) NOT NULL,
    data_cadastro DATE NOT NULL
);
