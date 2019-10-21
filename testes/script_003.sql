USE rede_passaros;

-- ALTER TABLE post
-- ADD localizacao point;

ALTER TABLE usuario ADD COLUMN ativo BOOLEAN DEFAULT 1;
ALTER TABLE passaros ADD COLUMN ativo BOOLEAN DEFAULT 1;

ALTER TABLE preferencias DROP COLUMN ativo;
ALTER TABLE mark_user_post DROP COLUMN ativo;
ALTER TABLE view_user_post DROP COLUMN ativo;
