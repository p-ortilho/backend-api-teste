create table usuarios(
    id INTEGER primary key autoincrement,
    nome varchar(255) not null,
    email varchar(255) not null unique,
    senha varchar(255) not null
);

create table servicos(
    id INTEGER primary key autoincrement,
    nome varchar(255) not null,
    preco decimal(10,2) not null
);

create table atendimentos(
    id INTEGER primary key autoincrement,
    usuario_id int not null,
    servico_id int not null,
    data datetime not null,
    foreign key (usuario_id) references usuarios(id),
    foreign key (servico_id) references servicos(id)
);

INSERT INTO servicos (nome, preco) VALUES
('Corte de Cabelo Feminino', 80.00),
('Hidratação Capilar', 120.00),
('Coloração', 150.00),
('Manicure', 45.00),
('Pedicure', 50.00),
('Escova Progressiva', 250.00),
('Design de Sobrancelhas', 40.00),
('Depilação Facial', 35.00),
('Maquiagem Social', 120.00),
('Penteado para Festa', 150.00);

SELECT * FROM servicos;

INSERT INTO atendimentos (usuario_id, servico_id, data) VALUES
(1, 1, '2025-02-01 10:00:00'),
(2, 2, '2025-02-01 11:00:00'),
(1, 3, '2025-02-01 12:00:00'),
(2, 4, '2025-02-01 13:00:00'),
(1, 5, '2025-02-01 14:00:00'),
(2, 6, '2025-02-01 15:00:00'),
(1, 7, '2025-02-01 16:00:00'),
(2, 8, '2025-02-01 17:00:00'),
(1, 9, '2025-02-01 18:00:00'),
(2, 10, '2025-02-01 19:00:00');