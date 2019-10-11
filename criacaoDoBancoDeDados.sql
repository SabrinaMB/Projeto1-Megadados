DROP DATABASE IF EXISTS rede_passaros;
CREATE DATABASE rede_passaros;
USE rede_passaros;


CREATE TABLE passaros (
    id_passaro INT NOT NULL AUTO_INCREMENT,
    passaro VARCHAR(80),
    PRIMARY KEY (id_passaro)
);


CREATE TABLE usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(80),
    email VARCHAR(80),
    cidade VARCHAR(160),
    PRIMARY KEY (id_usuario)
);


CREATE TABLE post (
    id_post INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(200),
    URL VARCHAR(160),
    texto VARCHAR(160),
    id_criador INT NOT NULL,
    ativo boolean,
    data_criacao timestamp,
    PRIMARY KEY (id_post),
    FOREIGN KEY (id_criador) REFERENCES usuario(id_usuario)
);



CREATE TABLE preferencias (
    id_usuario INT NOT NULL,
    id_passaro INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_passaro) REFERENCES passaros(id_passaro)
);



CREATE TABLE view_user_post (
    browser VARCHAR(160),
    aparelho VARCHAR(160),
    IP INT NOT NULL,
    instante_vizualizacao timestamp,
    id_usuario INT NOT NULL,
    id_post INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_post) REFERENCES post(id_post)
);

CREATE TABLE post_passaro (
    id_passaro INT NOT NULL,
    id_post INT NOT NULL,
    FOREIGN KEY (id_passaro) REFERENCES passaros(id_passaro),
    FOREIGN KEY (id_post) REFERENCES post(id_post)
);

CREATE TABLE mark_user_post (
    id_usuario INT NOT NULL,
    id_post INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_post) REFERENCES post(id_post)
);
