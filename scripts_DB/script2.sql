USE rede_passaros;

ALTER TABLE post
ADD localizacao point;

CREATE TABLE joinhas (
	id_usuario INT NOT NULL,
    id_post INT NOT NULL,
    gosta VARCHAR(80),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_post) REFERENCES post(id_post),
    PRIMARY KEY (id_usuario, id_post)
);


CREATE TABLE passaros (
    id_passaro INT NOT NULL AUTO_INCREMENT,
    passaro VARCHAR(80) NOT NULL,
    PRIMARY KEY (id_passaro)
);