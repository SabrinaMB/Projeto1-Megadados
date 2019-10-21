# from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
import logging
import pymysql
import json
from starlette.requests import Request
import os
import datetime
from pydantic import BaseModel
from projeto import *

class acha_user(BaseModel):
    nomeUser: str

class acha_usuario_nomeModel(BaseModel):
    nome: str
    
class adiciona_usuarioModel(BaseModel):
    nome: str
    email: str
    cidade: str

class adiciona_preferenciaModel(BaseModel):
    user: str
    passaro: str

class adiciona_passaromanModel(BaseModel):
    passaroname: str

class PostCreate(BaseModel):
    iduser: int
    titulo: str
    URL: str = None
    texto: str = None

class likezinho(BaseModel):
    id_post: int
    likou: int

app = FastAPI()


with open('config_tests.json', 'r') as arq:
    config = json.load(arq)

conn = pymysql.connect(
    host= config['HOST'],
    user= config['USER'],
    password= config['PASS'],
    database='rede_passaros')
conn.autocommit(True)
#############################################3

##Usuario##

@app.get("/usuario/{nome}")
def acha_usuario_nome_API(nome: str ):
    result = acha_usuario_nome(conn, nome)
    return result

@app.get("/usuario/popular/{cidade}")
def acha_usuario_mais_popular(cidade: str):
    return usuario_mais_popular_cidade(conn, cidade)

@app.post("/usuario")
def adiciona_Usuario_API(usuario: adiciona_usuarioModel):
    adiciona_usuario(conn, nome = usuario.nome, email = usuario.email, cidade = usuario.cidade)
    return "Good"

@app.post("/preferencia")
def adiciona_preferencia_API(preferencia: adiciona_preferenciaModel):
    adiciona_preferencia(conn, preferencia.user, preferencia.passaro)
    return "Good"
    
##UsuarioEnd##
 
##Posts##

@app.post("/posts")
def cria_post(post: PostCreate):
    adiciona_post(conn, post.iduser, post.titulo, post.URL, post.texto)
    return "Good"

@app.get("/posts")
def get_posts(req: Request):
    
    return lista_post_ativo(conn)

@app.delete("/posts/{id_post}")
def delete_post(id_post: int):
    muda_ativo_post(conn, id_post)
    return "Good"

@app.get("/posts/{idpost}")
def acha_posts(req: Request, idpost: int):

    resultado = acha_post_por_ID(conn, idpost)

    IP = int(req.client.host.replace(".", ""))
    devicebrowserinfo = req.headers["user-agent"].split()
    
    browser = "".join(devicebrowserinfo[-3:-1])
    aparelho = devicebrowserinfo[1]

    adiciona_view_user_post(conn, idpost, rendomuser(conn), IP, browser, aparelho)

    return resultado

##PostsEnd##

##Passaros##

@app.post("/passaros")
def add_passaro(passaro: adiciona_passaromanModel):
    adiciona_passaros(conn, passaro.passaroname)
    return "Good"

@app.get("/passaros")
def get_passaros():
    return lista_passaros(conn)

##Passarosend##

### CURTIDAS

@app.post("/like")
def likeaetio(like: likezinho):
    muda_joinhas(conn, like.id_post, like.likou)
    return "Good"

### 

##Tabela Cruzada vizualizações##

@app.get("/crossTable")
def tabelaCross():
    return aparelhos_por_browser(conn)

##Tabela End##
#############################################3

# @app.get("/posts/{idpost}")
# def acha_posts(req: Request, idpost: int):

#     resultado = acha_post_por_ID(conn, idpost)

#     IP = req.client.host
#     devicebrowserinfo = req.headers["user-agent"].split()
    
#     browser = "".join(devicebrowserinfo[-3:-1]
#     aparelho = devicebrowserinfo[1]

#     adiciona_view_user_post(conn, id_post, 1, IP, browser, aparelho)

#     return resultado

# @app.get("/os_popular")
# def lista_os():
#     resultado = os_popular(conn)
#     return resultado

# @app.post("/posts")
# def cria_post(post: PostCreate):
#     adiciona_post(conn, PostCreate.idpost, PostCreate.titulo, PostCreate.URL, PostCreate.texto)

# @app.put("/posts")
# def atualiza_post(post: Post_Atualiza):
#     pass

# @app.delete("/posts")
# def deleta_post(post: Post_Apaga):
#     apaga_post(conn, post.id)
#     return "Post deletado com sucesso"

# @app.get("/all_posts")
# def todos_posts():
#     posts = lista_posts(conn)

#     return posts

# @app.get("/posts_desc")
# def todos_posts_desc():
#     posts = lista_posts_desc(conn)

#     return posts

# @app.get("/passaros")
# def procura_passaros():

#     passaros = lista_passaros(conn)

#     return passaros

# @app.post("/passaros")
# def cria_passaro(passaro: Passaro):
#     adiciona_passaro(conn, passaro.especie)

# @app.put("/likes")
# def like_post(like : Likes):
#     likes(conn, like)

# @app.get("/tabela_cruzado")
# def tabela_cruzada():
#     return tabela_cruzado(conn)

# @app.get("/mencao/{login}")
# def lista_mencao(login: str):
#     res = list_received_mencao(conn, login)

#     return res 
    
# @app.get("/url_passaro")
# def url_passaro():
#     res = list_URL_passaros(conn) 
#     return res

# ###############################################################################################

# def passaro_parser(texto):
#     lista = []
#     start = 0
#     end = 0

#     if texto != None:
#         while start < len(texto):

#             if texto[start] != "#":
#                 start += 1
#             else:
#                 end = start + 1

#                 while ((texto[end].isalpha()) or (texto[end] == "-")):
#                     end += 1

#                 lista.append(texto[start + 1:end])

#             end += 1
#             start = end

#     return lista

# def pessoa_parser(texto):
#     lista = []
#     start = 0
#     end = 0

#     if texto != None:
#         while start < len(texto):

#             if texto[start] != "@":
#                 start += 1
#             else:
#                 end = start + 1

#                 while texto[end] != " ":
#                     end += 1

#                 lista.append(texto[start + 1:end])

#             end += 1
#             start = end

#     return lista

# def adiciona_post(conn, id_criador, titulo, URL='NULL', texto='NULL'):

#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('INSERT INTO post (titulo, id_criador, URL, texto) VALUES (%s, %s, %s, %s)', (titulo, id_criador, URL, texto))
#             id_post = acha_post(conn, id_criador, titulo)

#             passaros = passaro_parser(texto)
#             if len(passaros) > 0:
#                 for passaro in passaros:
#                     passarinho = acha_passaros(conn, passaro)
#                     adiciona_post_passaro(conn, id_post, passarinho)

#             pessoas = pessoa_parser(texto)
#             if len(pessoas) > 0:
#                 for pessoa in pessoas:
#                     pessoinha = acha_usuario_nome(conn, pessoa)
#                     adiciona_mark_user_post(conn, id_post, pessoinha)

#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso inserir titulo {titulo}, URL {URL}, texto {texto}, id_criador {id_criador} na tabela post')


def acha_post_por_ID(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM post WHERE id_post = %s', (id_post))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

# def acha_usuario_nome(conn, nome):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_usuario FROM usuario WHERE nome = %s', (nome))
#         res = cursor.fetchone()
#         if res:
#             return res[0]
#         else:
#             return None

# def acha_post(conn, id_criador, titulo):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_post FROM post WHERE id_criador = %s and titulo = %s', (id_criador, titulo))
#         res = cursor.fetchone()
#         if res:
#             return res[0]
#         else:
#             return None

# def acha_post_ativo(conn, id_criador, titulo):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_post FROM post WHERE id_criador = %s and titulo = %s and ativo = 1', (id_criador, titulo))
#         res = cursor.fetchone()
#         if res:
#             return res[0]
#         else:
#             return None

# def muda_titulo_post(conn, id_post, novo_titulo):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE post SET titulo=%s where id_post=%s', (novo_titulo, id_post))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar titulo do id {id_post} para {novo_titulo} na tabela post')

# def muda_URL_post(conn, id_post, novo_URL):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE post SET URL=%s where id_post=%s', (novo_URL, id_post))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar URL do id {id_post} para {novo_URL} na tabela post')

# def muda_texto_post(conn, id_post, novo_texto):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE post SET texto=%s where id_post=%s', (novo_texto, id_post))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar texto do id {id_post} para {novo_texto} na tabela post')

# def muda_ativo_post(conn, id_post, ativo=0):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE post SET ativo=%s where id_post=%s', (ativo, id_post))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar ativo do id {id_post} para {ativo} na tabela post')

# def lista_post(conn):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT * from post')
#         res = cursor.fetchall()
#         posts = tuple(x[0] for x in res)
#         return posts

# def lista_post_ativo(conn):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT * from post where ativo=1;')
#         res = cursor.fetchall()
#         posts = tuple(x[0] for x in res)
#         return posts

# def adiciona_passaros(conn, passaro):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('INSERT INTO passaros (passaro) VALUES (%s)', (passaro))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso inserir {passaro} na tabela passaros')

# def acha_passaros(conn, passaro):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_passaro FROM passaros WHERE passaro = %s', (passaro))
#         res = cursor.fetchone()
#         if res:
#             return res[0]
#         else:
#             return None

# def muda_ativo_passaros(conn, id_passaro, ativo=0):
#     with conn.cursor() as cursor:
#         cursor.execute('UPDATE passaros SET ativo=%s WHERE id_passaro=%s', (ativo, id_passaro))

# def muda_nome_passaros(conn, id_passaro, novo_passaro):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE passaros SET passaro=%s where id_passaro=%s', (passaro, id_passaro))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar nome do passaro do id {id_passaro} para {passaro} na tabela passaros')

# def lista_passaros(conn):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT * from passaros')
#         res = cursor.fetchall()
#         passaros = tuple(x[0] for x in res)
#         return passaros

# def lista_passaros_ativos(conn):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT * from passaros WHERE ativo=1')
#         res = cursor.fetchall()
#         passaros = tuple(x[0] for x in res)
#         return passaros

# def adiciona_usuario(conn, nome, email, cidade):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('INSERT INTO usuario (nome, email, cidade) VALUES (%s, %s, %s)', (nome, email, cidade))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso inserir nome {nome}, email {email} e cidade {cidade} na tabela usuario')

# def muda_ativo_usuario(conn, id_usuario, ativo=0):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE usuario SET ativo=%s where id_usuario=%s', (ativo, id_usuario))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar ativo para {ativo} na tabela usuario')

# def acha_id_usuario(conn, email):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_usuario FROM usuario WHERE email = %s', (email))
#         res = cursor.fetchone()
#         if res:
#             return res[0]
#         else:
#             return None

# def acha_info_usuario(conn, id_usuario):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id_usuario))
#         res = cursor.fetchone()
#         if res:
#             return res[0]
#         else:
#             return None

# def muda_nome_usuario(conn, id_usuario, novo_nome):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE usuario SET nome=%s where id_usuario=%s', (novo_nome, id_usuario))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar nome do usuario {id_usuario} para {novo_nome} na tabela usuario')

# def muda_email_usuario(conn, id_usuario, novo_email):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE usuario SET email=%s where id_usuario=%s', (novo_email, id_usuario))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar email do usuario {id_usuario} para {novo_email} na tabela usuario')

# def muda_cidade_usuario(conn, id_usuario, novo_cidade):
#     with conn.cursor() as cursor:
#         try:
#             cursor.execute('UPDATE usuario SET cidade=%s where id_usuario=%s', (novo_cidade, id_usuario))
#         except pymysql.err.IntegrityError as e:
#             raise ValueError(f'Não posso alterar cidade do usuario {id_usuario} para {novo_cidade} na tabela usuario')

# def lista_usuario(conn):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT * from usuario')
#         res = cursor.fetchall()
#         usuario = tuple(x[0] for x in res)
#         return usuario

# def lista_usuarios_ativos(conn):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT * from usuario WHERE ativo=1')
#         res = cursor.fetchall()
#         usuario = tuple(x[0] for x in res)
#         return usuario

# def adiciona_preferencia(conn, id_usuario, id_passaro):
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO preferencias (id_usuario, id_passaro) VALUES (%s, %s)', (id_usuario, id_passaro))

# def lista_preferencias_id_usuario(conn, id_passaro):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_usuario FROM preferencias WHERE id_passaro=%s', (id_passaro))
#         res = cursor.fetchall()
#         id_usuario = tuple(x[0] for x in res)
#         return id_usuario

# def lista_preferencias_id_passaro(conn, id_usuario):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_passaro FROM preferencias WHERE id_usuario=%s', (id_usuario))
#         res = cursor.fetchall()
#         id_passaro = tuple(x[0] for x in res)
#         return id_passaro

# def adiciona_post_passaro(conn, id_post, id_passaro):
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO post_passaro (id_post, id_passaro) VALUES (%s, %s)', (id_post, id_passaro))

# def lista_post_passaro_id_post(conn, id_passaro):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_post FROM post_passaro WHERE id_passaro=%s', (id_passaro))
#         res = cursor.fetchall()
#         id_post = tuple(x[0] for x in res)
#         return id_post

# def lista_post_passaro_id_passaro(conn, id_post):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_passaro FROM post_passaro WHERE id_post=%s', (id_post))
#         res = cursor.fetchall()
#         id_passaro = tuple(x[0] for x in res)
#         return id_passaro

# def adiciona_mark_user_post(conn, id_post, id_usuario):
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO mark_user_post (id_post, id_usuario) VALUES (%s, %s)', (id_post, id_usuario))

# def lista_mark_user_post_id_post(conn, id_usuario):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_post FROM mark_user_post WHERE id_usuario=%s', (id_usuario))
#         res = cursor.fetchall()
#         id_post = tuple(x[0] for x in res)
#         return id_post

# def lista_mark_user_post_id_usuario(conn, id_post):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_usuario FROM mark_user_post WHERE id_post=%s', (id_post))
#         res = cursor.fetchall()
#         id_usuario = tuple(x[0] for x in res)
#         return id_usuario

# def adiciona_view_user_post(conn, id_post, id_usuario, IP, browser, aparelho):
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO view_user_post (id_post, id_usuario, IP, browser, aparelho) VALUES (%s, %s, %s, %s, %s)', (id_post, id_usuario, IP, browser, aparelho))

# def lista_view_user_post_id_post(conn, id_usuario):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_post FROM view_user_post WHERE id_usuario=%s', (id_usuario))
#         res = cursor.fetchall()
#         id_post = tuple(x[0] for x in res)
#         return id_post

# def lista_view_user_post_id_usuario(conn, id_post):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_usuario FROM view_user_post WHERE id_post=%s', (id_post))
#         res = cursor.fetchall()
#         id_usuario = tuple(x[0] for x in res)
#         return id_usuario
# #### queries
# def ve_posts_usuario_nao_cronologica(conn, id_usuario):
#     with conn.cursor() as cursor:
#         cursor.execute('''  SELECT titulo, URL, texto  FROM post
#                             INNER JOIN (usuario)
#                             WHERE id_criador=%s
#                             ORDER BY data_criacao''', (id_usuario))
#         res = cursor.fetchall()
#         titulo, URL, texto = tuple(x[0] for x in res)
#         return titulo, URL, texto

# def usuario_mais_popular_cidade(conn, cidade):
#     with conn.cursor() as cursor:
#         cursor.execute('''  SELECT id_criador FROM usuario
#                             INNER JOIN (view_user_post)
#                             INNER JOIN (post)
#                             WHERE cidade=%s
#                             GROUP BY id_criador
#                             ORDER BY count(id_criador)
#                             LIMIT 1''', cidade)
#         res = cursor.fetchall()
#         id_usuario = tuple(x[0] for x in res)
#         return id_usuario

# def usuarios_referenciados_por_usuario(conn, id_criador):
#     with conn.cursor() as cursor:
#         cursor.execute('''  SELECT nome FROM usuario
#                             INNER JOIN (mark_user_post)
#                             INNER JOIN (post)
#                             WHERE id_criador=%s
#                             GROUP BY id_criador
#                             ''', id_criador)
#         res = cursor.fetchall()
#         nome = tuple(x[0] for x in res)
#         return nome

# def aparelhos_por_browser(conn):
#     with conn.cursor() as cursor:
#         cursor.execute(''' SELECT aparelho, browser FROM view_user_post 
#                            GROUP BY aparelho, browser; ''')
#         res = cursor.fetchall()
#         aparelho = tuple(x[0] for x in res)
#         browser = tuple(x[1] for x in res)
#         return aparelho, browser

# def lista_URL_e_tag(conn):
#     with conn.cursor() as cursor:
#         cursor.execute('''  SELECT URL, passaro FROM passaros
#                             INNER JOIN post_passaro
#                             INNER JOIN (post)''')
#         res = cursor.fetchall()
#         URL = tuple(x[0] for x in res)
#         passaro = tuple(x[1] for x in res)
#         return URL, passaro

# def adiciona_joinhas(conn, id_post, id_usuario, gosta='NULL'):
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO joinhas (id_post, id_usuario, gosta) VALUES (%s, %s, %s)', (id_post, id_usuario, gosta))

# def lista_joinhas_id_post(conn, id_usuario):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_post FROM joinhas WHERE id_usuario=%s', (id_usuario))
#         res = cursor.fetchall()
#         id_post = tuple(x[0] for x in res)
#         return id_post

# def lista_joinhas_id_usuario(conn, id_post):
#     with conn.cursor() as cursor:
#         cursor.execute('SELECT id_usuario FROM joinhas WHERE id_post=%s', (id_post))
#         res = cursor.fetchall()
#         id_usuario = tuple(x[0] for x in res)
#         return id_usuario
