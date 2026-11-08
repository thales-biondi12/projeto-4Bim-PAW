create database Web;
use web;

create table usuarios(
id_usuarios int primary key auto_increment,
nome varchar(255) not null,
email varchar(255) not null unique,
senha varchar(255) not null,
tel varchar(255) unique,
data_nasc date,
tipo_usuario varchar(255) not null
);

create table ministerios(
id_ministerios int primary key auto_increment,
nome varchar(255) not null,
descricao varchar(255),
dia_reuniao varchar(255) not null,
id_coordenador int,
foreign key (id_coordenador) references usuarios(id_usuarios)
);

create table usuarios_ministerios(
id_usuarios_ministerios int primary key auto_increment,
id_usuario int,
id_ministerio int,
data_entrada date not null,
funcao varchar(255) not null,
foreign key (id_usuario) references usuarios(id_usuarios),
foreign key (id_ministerio) references ministerios(id_ministerios)
);

create table eventos(
id_evento int primary key auto_increment,
titulo varchar(255) not null,
descricao varchar(255) not null,
data_evento date not null,
local_evento varchar(255) not null,
limite_vagas int not null,
status_evento varchar(255) not null
);

create table inscricoes(
id_inscricoes int primary key auto_increment,
usuario_id int,
evento_id int,
data_inscricao date not null,
presenca varchar(255) not null,
foreign key (usuario_id)
references usuarios(id_usuarios),
foreign key (evento_id) references eventos(id_evento),
unique(usuario_id, evento_id)
);

create table mensagens(
id_mensagens int primary key auto_increment,
titulo varchar(255) not null,
conteudo varchar(255) not null,
usuario_id int,
data_postagem date not null,
foreign key (usuario_id) references usuarios(id_usuarios)
);

-- tabela usuarios
insert into usuarios (nome,email,senha,tel,data_nasc,tipo_usuario)values 
("Thales" , "thales@gmail.com",12345,"(12)988139975","2009-07-29","ADM"),
("Pedro" , "Pedro@gmail.com",87459,"(12)98759845","2009-07-21","ADM"),
("Italo" , "italo@gmail.com",97200,"(12)99584575","2009-08-25","ADM"),
-- MEMBROS
("Lucas" , "lucas@gmail.com",45612,"(12)991234567","2008-03-15","MEMBRO"),
("Mariana" , "mariana@gmail.com",78945,"(12)992345678","2007-11-02","MEMBRO"),
("Gabriel" , "gabriel@gmail.com",32178,"(12)993456789","2009-01-19","MEMBRO"),

-- COORDENADORES
("Fernanda" , "fernanda@gmail.com",65487,"(12)994567890","1998-06-10","COORDENADOR"),
("Ricardo" , "ricardo@gmail.com",95124,"(12)995678901","1995-09-27","COORDENADOR"),
("Patricia" , "patricia@gmail.com",75319,"(12)996789012","1992-12-05","COORDENADOR"),

-- VISITANTES
("Joao" , "joao@gmail.com",14785,"(12)997890123","2010-04-08","VISITANTE"),
("Beatriz" , "beatriz@gmail.com",25896,"(12)998901234","2008-08-30","VISITANTE"),
("Carlos" , "carlos@gmail.com",36914,"(12)999012345","2007-05-14","VISITANTE");

-- tabela ministerios
insert into ministerios (nome, descricao, dia_reuniao, id_coordenador) values
("Ministerio de Musica", "Responsavel pelos louvores e cantos das celebracoes", "Sexta-feira", 7),
("Ministerio Jovem", "Organiza encontros e eventos para os jovens", "Sabado", 8),
("Ministerio Infantil", "Cuida das atividades voltadas para as criancas", "Domingo", 9),
("Ministerio de Oracao", "Grupo dedicado a momentos de oracao e intercessao", "Quarta-feira", 7),
("Ministerio de Acolhida", "Recepciona os visitantes e membros da comunidade", "Domingo", 8);

-- usuarios_ministerios
insert into usuarios_ministerios
(id_usuario, id_ministerio, data_entrada, funcao) values

-- Ministério de Música
(1, 1, "2024-01-10", "Vocalista"),
(7, 1, "2024-02-15", "Guitarrista"),

-- Ministério Jovem
(5, 2, "2024-03-05", "Lider Jovem"),
(8, 2, "2024-03-20", "Participante"),

-- Ministério Infantil
(6, 3, "2024-04-12", "Professor"),
(9, 3, "2024-04-18", "Auxiliar"),

-- Ministério de Oração
(10, 4, "2024-05-01", "Intercessor"),
(1, 4, "2024-05-08", "Coordenador"),

-- Ministério de Acolhida
(12, 5, "2024-06-02", "Recepcionista"),
(13, 5, "2024-06-10", "Visitante");

--  tabela eventos
insert into eventos
(titulo, descricao, data_evento, local_evento, limite_vagas, status_evento) values

("Retiro Espiritual Jovem", "Encontro de espiritualidade e integracao dos jovens", "2026-07-15", "Sitio Esperanca", 80, "ABERTO"),

("Noite de Louvor", "Evento com musicas, oracoes e adoracao", "2026-06-20", "Salao Paroquial", 150, "ABERTO"),

("Catequese Infantil", "Atividades religiosas voltadas para criancas", "2026-06-10", "Centro Comunitario", 40, "ENCERRADO"),

("Campanha do Agasalho", "Arrecadacao de roupas para familias carentes", "2026-07-01", "Igreja Matriz", 100, "ABERTO"),

("Formacao de Lideres", "Treinamento para coordenadores e liderancas", "2026-08-05", "Auditorio Sao Jose", 30, "PLANEJADO");

-- tabela inscriçoes
insert into inscricoes
(usuario_id, evento_id, data_inscricao, presenca) values

(1, 1, "2026-06-01", "CONFIRMADA"),
(5, 1, "2026-06-02", "CONFIRMADA"),
(6, 1, "2026-06-02", "PENDENTE"),

(7, 2, "2026-06-03", "CONFIRMADA"),
(8, 2, "2026-06-03", "CONFIRMADA"),
(9, 2, "2026-06-04", "AUSENTE"),

(10, 3, "2026-06-05", "CONFIRMADA"),
(11, 3, "2026-06-05", "PENDENTE"),

(12, 4, "2026-06-06", "CONFIRMADA"),
(13, 4, "2026-06-06", "CONFIRMADA"),

(14, 5, "2026-06-07", "PENDENTE"),
(15, 5, "2026-06-07", "CONFIRMADA");

-- tabela msg
insert into mensagens
(titulo, conteudo, usuario_id, data_postagem) values

("Bem-vindos", "Sejam todos bem-vindos a comunidade paroquial.", 1, "2026-06-01"),

("Ensaio do Ministerio", "O ensaio de musica sera realizado sexta-feira as 19h.", 10, "2026-06-02"),

("Retiro Espiritual", "As inscricoes para o retiro espiritual continuam abertas.", 11, "2026-06-03"),

("Campanha do Agasalho", "Doe roupas e cobertores para ajudar familias carentes.", 12, "2026-06-04"),

("Encontro Jovem", "Neste sabado teremos encontro especial para os jovens.", 5, "2026-06-05"),

("Aviso Catequese", "As aulas da catequese infantil foram remarcadas.", 6, "2026-06-06");








