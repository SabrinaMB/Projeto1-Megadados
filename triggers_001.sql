USE rede_passaros;

-- IF APAGA usuario
DROP TRIGGER IF EXISTS apagaUsuario_apagaPost
create trigger apagaUsuario_apagaPost
after
update
on usuario
for each row
UPDATE post SET ativo = 0 WHERE usuario.id_usuario = post.id_criador and usuario.ativo = 0;


DROP TRIGGER IF EXISTS apagaUsuario_apagaPreferencia
-- create trigger apagaUsuario_apagaPreferencia
-- after
-- update
-- on usuario
-- for each row
-- update preferencias set ativo = 0 where usuario.id_usuario = preferencias.id_usuario and usuario.ativo = 0;


DROP TRIGGER IF EXISTS apagaUsuario_apagaMencaoUsuario
-- create trigger apagaUsuario_apagaMencaoUsuario
-- after
-- update
-- on usuario
-- for each row
-- update mark_user_post set ativo = 0 where mark_user_post.id_usuario = usuario.id_usuario and usuario.ativo = 0;


DROP TRIGGER IF EXISTS apagaUsuario_apagaVisualizacao
-- create trigger apagaUsuario_apagaVisualizacao
-- after
-- update
-- on usuario
-- for each row
-- update view_user_post set ativo = 0 where view_user_post.id_usuario = usuario.id_usuario and usuario.ativo = 0;

-- IF APAGA PASSARO

DROP TRIGGER IF EXISTS apagaPassaro_apagaPreferencia
-- create trigger apagaPassaro_apagaPreferencia
-- after
-- update
-- on passaros
-- for each row
-- update preferencias set ativo = 0 where preferencias.id_passaro = passaros.id_passaro and preferencias.ativo = 0;


DROP TRIGGER IF EXISTS apagaPassaro_apagaMencaoPassaro
-- create trigger apagaPassaro_apagaMencaoPassaro
-- after
-- update
-- on passaros
-- for each row
-- update post_passaro set ativo = 0 where post_passaro.id_passaro = passaros.id_passaro and preferencias.ativo = 0;