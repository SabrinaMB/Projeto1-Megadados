import pymysql


def passaro_parser(texto):
    lista = []
    start = 0
    end = 0

    if texto != None:
        while start < len(texto):

            if texto[start] != "#":
                start += 1
            else:
                end = start + 1

                while ((texto[end].isalpha()) or (texto[end] == "-")):
                    end += 1

                lista.append(texto[start + 1:end])

            end += 1
            start = end

    return lista

def pessoa_parser(texto):
    lista = []
    start = 0
    end = 0

    if texto != None:
        while start < len(texto):

            if texto[start] != "@":
                start += 1
            else:
                end = start + 1

                while texto[end] != " ":
                    end += 1

                lista.append(texto[start + 1:end])

            end += 1
            start = end

    return lista

def adiciona_post(conn, id_criador, titulo, URL='NULL', texto='NULL'):

    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post (titulo, id_criador, URL, texto) VALUES (%s, %s, %s, %s)', (titulo, id_criador, URL, texto))
            id_post = acha_post(conn, id_criador, titulo)

            passaros = passaro_parser(texto)
            if len(passaros) > 0:
                for passaro in passaros:
                    passarinho = acha_passaros(conn, passaro)
                    adiciona_post_passaro(conn, id_post, passarinho)

            pessoas = pessoa_parser(texto)
            if len(pessoas) > 0:
                for pessoa in pessoas:
                    pessoinha = acha_usuario_nome(conn, pessoa)
                    adiciona_mark_user_post(conn, id_post, pessoinha)

        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir titulo {titulo}, URL {URL}, texto {texto}, id_criador {id_criador} na tabela post')

def acha_usuario_nome(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario WHERE nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def acha_post(conn, id_criador, titulo):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post WHERE id_criador = %s and titulo = %s', (id_criador, titulo))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def acha_post_ativo(conn, id_criador, titulo):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post WHERE id_criador = %s and titulo = %s and ativo = 1', (id_criador, titulo))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def muda_titulo_post(conn, id_post, novo_titulo):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE post SET titulo=%s where id_post=%s', (novo_titulo, id_post))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar titulo do id {id_post} para {novo_titulo} na tabela post')

def muda_URL_post(conn, id_post, novo_URL):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE post SET URL=%s where id_post=%s', (novo_URL, id_post))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar URL do id {id_post} para {novo_URL} na tabela post')

def muda_texto_post(conn, id_post, novo_texto):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE post SET texto=%s where id_post=%s', (novo_texto, id_post))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar texto do id {id_post} para {novo_texto} na tabela post')

def muda_ativo_post(conn, id_post, ativo=0):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE post SET ativo=%s where id_post=%s', (ativo, id_post))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar ativo do id {id_post} para {ativo} na tabela post')

def lista_post(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from post')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def lista_post_ativo(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from post where ativo=1;')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def adiciona_passaros(conn, passaro):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO passaros (passaro) VALUES (%s)', (passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {passaro} na tabela passaros')

def acha_passaros(conn, passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM passaros WHERE passaro = %s', (passaro))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def muda_ativo_passaros(conn, id_passaro, ativo=0):
    with conn.cursor() as cursor:
        cursor.execute('UPDATE passaros SET ativo=%s WHERE id_passaro=%s', (ativo, id_passaro))

def muda_nome_passaros(conn, id_passaro, novo_passaro):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE passaros SET passaro=%s where id_passaro=%s', (passaro, id_passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do passaro do id {id_passaro} para {passaro} na tabela passaros')

def lista_passaros(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from passaros')
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

def lista_passaros_ativos(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from passaros WHERE ativo=1')
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

def adiciona_usuario(conn, nome, email, cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario (nome, email, cidade) VALUES (%s, %s, %s)', (nome, email, cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir nome {nome}, email {email} e cidade {cidade} na tabela usuario')

def muda_ativo_usuario(conn, id_usuario, ativo=0):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET ativo=%s where id_usuario=%s', (ativo, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar ativo para {ativo} na tabela usuario')


def acha_id_usuario(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario WHERE email = %s', (email))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def acha_info_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM usuario WHERE id_usuario = %s', (id_usuario))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def muda_nome_usuario(conn, id_usuario, novo_nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nome=%s where id_usuario=%s', (novo_nome, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do usuario {id_usuario} para {novo_nome} na tabela usuario')

def muda_email_usuario(conn, id_usuario, novo_email):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET email=%s where id_usuario=%s', (novo_email, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar email do usuario {id_usuario} para {novo_email} na tabela usuario')

def muda_cidade_usuario(conn, id_usuario, novo_cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET cidade=%s where id_usuario=%s', (novo_cidade, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar cidade do usuario {id_usuario} para {novo_cidade} na tabela usuario')

def lista_usuario(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from usuario')
        res = cursor.fetchall()
        usuario = tuple(x[0] for x in res)
        return usuario

def lista_usuarios_ativos(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * from usuario WHERE ativo=1')
        res = cursor.fetchall()
        usuario = tuple(x[0] for x in res)
        return usuario

def adiciona_preferencia(conn, id_usuario, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO preferencias (id_usuario, id_passaro) VALUES (%s, %s)', (id_usuario, id_passaro))

def lista_preferencias_id_usuario(conn, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM preferencias WHERE id_passaro=%s', (id_passaro))
        res = cursor.fetchall()
        id_usuario = tuple(x[0] for x in res)
        return id_usuario

def lista_preferencias_id_passaro(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM preferencias WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        id_passaro = tuple(x[0] for x in res)
        return id_passaro

def adiciona_post_passaro(conn, id_post, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO post_passaro (id_post, id_passaro) VALUES (%s, %s)', (id_post, id_passaro))

def lista_post_passaro_id_post(conn, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post_passaro WHERE id_passaro=%s', (id_passaro))
        res = cursor.fetchall()
        id_post = tuple(x[0] for x in res)
        return id_post

def lista_post_passaro_id_passaro(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM post_passaro WHERE id_post=%s', (id_post))
        res = cursor.fetchall()
        id_passaro = tuple(x[0] for x in res)
        return id_passaro

def adiciona_mark_user_post(conn, id_post, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO mark_user_post (id_post, id_usuario) VALUES (%s, %s)', (id_post, id_usuario))

def lista_mark_user_post_id_post(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM mark_user_post WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        id_post = tuple(x[0] for x in res)
        return id_post

def lista_mark_user_post_id_usuario(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM mark_user_post WHERE id_post=%s', (id_post))
        res = cursor.fetchall()
        id_usuario = tuple(x[0] for x in res)
        return id_usuario

def adiciona_view_user_post(conn, id_post, id_usuario, IP, browser, aparelho):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO view_user_post (id_post, id_usuario, IP, browser, aparelho) VALUES (%s, %s, %s, %s, %s)', (id_post, id_usuario, IP, browser, aparelho))

def lista_view_user_post_id_post(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM view_user_post WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        id_post = tuple(x[0] for x in res)
        return id_post

def lista_view_user_post_id_usuario(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM view_user_post WHERE id_post=%s', (id_post))
        res = cursor.fetchall()
        id_usuario = tuple(x[0] for x in res)
        return id_usuario
#### queries
def ve_posts_usuario_nao_cronologica(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('''  SELECT titulo, URL, texto  FROM post
                            INNER JOIN (usuario)
                            WHERE id_criador=%s
                            ORDER BY data_criacao''', (id_usuario))
        res = cursor.fetchall()
        titulo, URL, texto = tuple(x[0] for x in res)
        return titulo, URL, texto

def usuario_mais_popular_cidade(conn, cidade):
    with conn.cursor() as cursor:
        cursor.execute('''  SELECT id_criador FROM usuario
                            INNER JOIN (view_user_post)
                            INNER JOIN (post)
                            WHERE cidade=%s
                            GROUP BY id_criador
                            ORDER BY count(id_criador)
                            LIMIT 1''', cidade)
        res = cursor.fetchall()
        id_usuario = tuple(x[0] for x in res)
        return id_usuario

def usuarios_referenciados_por_usuario(conn, id_criador):
    with conn.cursor() as cursor:
        cursor.execute('''  SELECT nome FROM usuario
                            INNER JOIN (mark_user_post)
                            INNER JOIN (post)
                            WHERE id_criador=%s
                            GROUP BY id_criador
                            ''', id_criador)
        res = cursor.fetchall()
        nome = tuple(x[0] for x in res)
        return nome

def aparelhos_por_browser(conn):
    with conn.cursor() as cursor:
        cursor.execute(''' SELECT aparelho, browser FROM view_user_post 
                           GROUP BY aparelho, browser; ''')
        res = cursor.fetchall()
        aparelho = tuple(x[0] for x in res)
        browser = tuple(x[1] for x in res)
        return aparelho, browser

def lista_URL_e_tag(conn):
    with conn.cursor() as cursor:
        cursor.execute('''  SELECT URL, passaro FROM passaros
                            INNER JOIN post_passaro
                            INNER JOIN (post)''')
        res = cursor.fetchall()
        URL = tuple(x[0] for x in res)
        passaro = tuple(x[1] for x in res)
        return URL, passaro

def adiciona_joinhas(conn, id_post, id_usuario, gosta='NULL'):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO joinhas (id_post, id_usuario, gosta) VALUES (%s, %s, %s)', (id_post, id_usuario, gosta))

def lista_joinhas_id_post(conn, id_usuario, gosta=1):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM joinhas WHERE id_usuario=%s AND gosta=%s', (id_usuario, gosta))
        res = cursor.fetchall()
        id_post = tuple(x[0] for x in res)
        return id_post

def lista_joinhas_id_usuario(conn, id_post, gosta=1):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM joinhas WHERE id_post=%s AND gosta=%s', (id_post, gosta))
        res = cursor.fetchall()
        id_usuario = tuple(x[0] for x in res)
        return id_usuario

def muda_joinhas(conn, id_post, id_usuario, novo_joinha):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE joinhas SET gosta=%s where id_post=%s AND id_usuario=%s', (novo_joinha, id_post, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar joinha do id {id_post} para {novo_joinha} na tabela post')
