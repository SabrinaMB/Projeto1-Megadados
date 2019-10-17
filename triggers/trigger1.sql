USE rede_passaros;

create trigger apagaUsuario_apagaPost
after
delete
on usuario
for each row
UPDATE post
SET ativo = 0
WHERE usuario.id_usuario = post.id_criador;

create trigger apagaPost_apagaMencaoPassaro
after
update
on post
for each row
update post_passaro set ativo = 0 where post_passaro.id_post = post.id_post and post.ativo = 0;

create trigger apagaPost_apagaMencaoUsuario
after
update
on post 
for each row
update mark_user_post set ativo = 0 where mark_user_post.id_post = post.id_post and post.ativo = 0;


create trigger apagaPost_apagaVisualizacao
after
update
on post 
for each row
update view_user_post set ativo = 0 where view_user_post.id_post = post.id_post and post.ativo = 0;

create trigger apagaPassaro_apagaPreferencia
after
delete
on passaros
for each row
delete from preferencias where preferencias.id_passaro = passaros.id_passaro;

create trigger apagaUsuario_apagaPreferencia
after
delete
on usuario
for each row
delete from usuario where usuario.id_usuario = preferencias.id_usuario;

create trigger apagaPassaro_apagaMencaoPassaro
after
delete
on passaros
for each row
delete from post_passaro where post_passaro.id_passaro = passaros.id_passaro;

create trigger apagaUsuario_apagaMencaoUsuario
after
delete
on usuario
for each row
delete from mark_user_post where mark_user_post.id_usuario = usuario.id_usuario;

create trigger apagaUsuario_apagaVisualizacao
after
delete
on usuario
for each row
delete from view_user_post where view_user_post.id_usuario = usuario.id_usuario;

