-- Criação do datbase e comando para usar o database criado
create database achados_perdidos;
use achados_perdidos;

-- Criação da tabela de Itens.
create table itens(
id int auto_increment,
titulo varchar(100) not null,
descricao text,
local_encontrado varchar(100) not null,
data_encontro date not null,
status enum('Disponivel','Devolvido') not null default 'Disponivel',
retirado_por varchar(100) default null,
primary key (id)
);

-- Inserindo registros iniciais para testar a leitura (read).
insert into itens (titulo, descricao, local_encontrado, data_encontro) values
('Garrafa térmica azul','Marca Stanley com adesivo de foguete','Quadra de Esportes','2026-11-20'),
('Caderno de cálculo','Capa preta, espiral, sem nome','Laboratório 03','2026-11-21'),
('Casaco moletom cinza','Tamanho M, encontrado na cadeira','Auditório','2026-11-22'),
('Notebook Samsung','Notebook Samsung, Preto, Adesivo Hackatorion','Info 03','2026-11-23');

-- Comando para conferir as informações da tabela Itens.
select * from itens;