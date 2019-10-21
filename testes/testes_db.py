import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql
from random import randint

from projeto import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='rede_passaros' 
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

    def test_adiciona_view_user_post_e_aparelhos_browser(self):
        conn = self.__class__.connection

        nome = 'paulost'
        email = 'paulost@mememail.com'
        cidade = 'sao paulo'

        # Adiciona um perigo não existente.
        adiciona_usuario(conn, nome, email, cidade)

        passaro = 'beija-flor'

        # Adiciona um perigo não existente.
        adiciona_passaros(conn, passaro)
    
        titulo = 'meu primeiro post'
        texto = 'oi pessoal!! to postando aqui so pra dizer que fui passear pelo ibira e vi um #beija-flor oi'
        id_criador = acha_id_usuario(conn, email)

        adiciona_post(conn, id_criador, titulo, texto=texto)

        nome = 'matteo'
        email = 'matteo@mememail.com'
        cidade = 'tokyo'

        # Adiciona um perigo não existente.
        adiciona_usuario(conn, nome, email, cidade)

        id_post = acha_post(conn, id_criador, titulo)
        id_usuario = acha_id_usuario(conn, email)
        IP = 10
        browser = "banana"
        aparelho = "iphone 6s"

        adiciona_view_user_post(conn, id_post, id_usuario, IP, browser, aparelho)

        lista_views = lista_view_user_post_id_usuario(conn, id_post)

        self.assertEqual(lista_views, (id_usuario,))
        a, b = aparelhos_por_browser(conn)
        self.assertEqual((aparelho,), a)
        self.assertEqual((browser,), b)

    def test_adiciona_e_muda_joinha(self):
        conn = self.__class__.connection

        nome = 'paulost'
        email = 'paulost@mememail.com'
        cidade = 'sao paulo'

        # Adiciona um perigo não existente.
        adiciona_usuario(conn, nome, email, cidade)

        passaro = 'beija-flor'

        # Adiciona um perigo não existente.
        adiciona_passaros(conn, passaro)
    
        titulo = 'meu primeiro post'
        texto = 'oi pessoal!! to postando aqui so pra dizer que fui passear pelo ibira e vi um #beija-flor oi'
        id_criador = acha_id_usuario(conn, email)

        adiciona_post(conn, id_criador, titulo, texto=texto)

        nome = 'matteo'
        email = 'matteo@mememail.com'
        cidade = 'tokyo'

        # Adiciona um perigo não existente.
        adiciona_usuario(conn, nome, email, cidade)


        id_post = acha_post(conn, id_criador, titulo)
        id_usuario = acha_id_usuario(conn, email)
        IP = 10
        browser = "banana"
        aparelho = "iphone 6s"

        adiciona_joinhas(conn, id_post, id_usuario, gosta=1)
        # adiciona_view_user_post(conn, id_post, id_usuario, IP, browser, aparelho)

        lista_views = lista_joinhas_id_usuario(conn, id_post)

        self.assertEqual(lista_views[0], id_usuario)
        self.assertEqual(lista_joinhas_id_post(conn, id_usuario, 1), (id_post,))
        muda_joinhas(conn, id_post, id_usuario, 0)
        self.assertEqual(lista_joinhas_id_post(conn, id_usuario, 0), (id_post,))


    def test_adiciona_preferencia(self):
        conn = self.__class__.connection
    
        nome = 'paulost'
        email = 'paulost@mememail.com'
        cidade = 'sao paulo'

        # Adiciona um usuario não existente.
        adiciona_usuario(conn, nome, email, cidade)

        passaro = 'beija-flor'

        # Adiciona um perigo não existente.
        adiciona_passaros(conn, passaro)

        id_usuario = acha_id_usuario(conn, email)
        id_passaro = acha_passaros(conn, passaro)

        adiciona_preferencia(conn, id_usuario, id_passaro)

        # Checa se o usuario existe.
        
        lista = lista_preferencias_id_passaro(conn, id_usuario)

        self.assertEqual(lista[0], id_passaro)

    def test_adiciona_usuario(self):
        conn = self.__class__.connection
    
        nome = 'paulost'
        email = 'paulost@mememail.com'
        cidade = 'sao paulo'

        # Adiciona um usuario não existente.
        adiciona_usuario(conn, nome, email, cidade)

        # Checa se o usuario existe.
        id = acha_id_usuario(conn, email)
        self.assertIsNotNone(id)

        # Tenta achar um usuario inexistente.
        id = acha_id_usuario(conn, 'mailzinho@pompom.com')
        self.assertIsNone(id)
#
    def test_adiciona_post_e_lista_URL_tag(self):
        conn = self.__class__.connection

        nome = 'paulost'
        email = 'paulost@mememail.com'
        cidade = 'sao paulo'

        # Adiciona um perigo não existente.
        adiciona_usuario(conn, nome, email, cidade)

        passaro = 'beija-flor'

        # Adiciona um perigo não existente.
        adiciona_passaros(conn, passaro)
    
        titulo = 'meu primeiro post'
        texto = 'oi pessoal!! to postando aqui so pra dizer que fui passear pelo ibira e vi um #beija-flor oi'

        id_criador = acha_id_usuario(conn, email)

        adiciona_post(conn, id_criador, titulo, texto=texto)

        id_post = acha_post(conn, id_criador, titulo)
        id_passaro = acha_passaros(conn, passaro)


        id = acha_post(conn, id_criador, titulo)
        self.assertIsNotNone(id)

        id = acha_post(conn, '90', titulo)
        self.assertIsNone(id)
        URL, p =  lista_URL_e_tag(conn)
        self.assertEqual(URL, ('NULL',))
        self.assertEqual(p, (passaro,))
#
    def test_adiciona_passaro(self):
        conn = self.__class__.connection
    
        passaro = 'bem-te-vi'

        adiciona_passaros(conn, passaro)

        id = acha_passaros(conn, passaro)
        self.assertIsNotNone(id)

        id = acha_passaros(conn, "mal-te-vi")
        self.assertIsNone(id)

# # REMOVE

    def test_remove_usuario(self):
        conn = self.__class__.connection
    
        nome = 'paulost'
        email = 'paulost@mememail.com'
        cidade = 'sao paulo'

        # Adiciona um perigo não existente.
        adiciona_usuario(conn, nome, email, cidade)
        id_usuario = acha_id_usuario(conn, email)

        res = lista_usuarios_ativos(conn)
        self.assertCountEqual(res, (id_usuario,))

        muda_ativo_usuario(conn, id_usuario)

        res = lista_usuarios_ativos(conn)
        self.assertFalse(res)

    def test_remove_passaro(self):
        conn = self.__class__.connection
        adiciona_passaros(conn, 'kestrel-one')
        id_passaro = acha_passaros(conn, 'kestrel-one')

        res = lista_passaros_ativos(conn)
        self.assertCountEqual(res, (id_passaro,))

        muda_ativo_passaros(conn, id_passaro)

        res = lista_passaros_ativos(conn)
        self.assertFalse(res)
# #
    def test_remove_post(self):
        conn = self.__class__.connection

        nome = 'paulost'
        email = 'paulost@mememail.com'
        cidade = 'sao paulo'

        # Adiciona um perigo não existente.
        adiciona_usuario(conn, nome, email, cidade)

        passaro = 'beija-flor'

        # Adiciona um perigo não existente.
        adiciona_passaros(conn, passaro)
    
        titulo = 'meu primeirp post'
        texto = 'oi pessoal!! to postando aqui so pra dizer que fui passear pelo ibira e vi um #beija-flor oi'
        id_criador = acha_id_usuario(conn, email)

        adiciona_post(conn, id_criador, titulo, texto=texto)

        id_post = acha_post(conn, id_criador, titulo)
        id_passaro = acha_passaros(conn, passaro)

        res = lista_post_ativo(conn)
        self.assertCountEqual(res, (id_post,))

        muda_ativo_post(conn, id_post, id_passaro)

        res = lista_post_ativo(conn)
        self.assertFalse(res)


# # LISTA
# # NEEDS FIX

    def test_usuarios_referenciados_por_usuario(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem perigos no sistema.
        res = lista_usuario(conn)
        self.assertFalse(res)

        # Adiciona alguns perigos.
        usuarios_id = []
        nome = 'salomao'
        email = 'salomao@gmail.com'
        cidade = 'sao paulo'
        adiciona_usuario(conn, nome, email, cidade)
        usuarios_id.append(acha_id_usuario(conn, email))

        nome = 'pedro'
        email = 'pedroer@gmail.com'
        cidade = 'sao paulo'
        adiciona_usuario(conn, nome, email, cidade)
        usuarios_id.append(acha_id_usuario(conn, email))

        adiciona_post(conn, usuarios_id[0], "e ae pedro", texto="@pedro , e ae??")
        adiciona_post(conn, usuarios_id[1], "e ae salomao", texto="@salomao , e ae??")

        # Verifica se os perigos foram adicionados corretamente.
        res = usuarios_referenciados_por_usuario(conn, usuarios_id[0])
        self.assertEqual(res[0], "salomao")

        res = usuarios_referenciados_por_usuario(conn, usuarios_id[1])
        self.assertEqual(res[0], "salomao")

    def test_lista_post(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem perigos no sistema.
        res = lista_post_ativo(conn)
        self.assertFalse(res)

        passaro = 'sabia'
        adiciona_passaros(conn, passaro)

        passaro = 'bem-te-vi'
        adiciona_passaros(conn, passaro)

        # Adiciona alguns perigos.
        posts_id = []
        nome = 'salomao'
        email = 'salomao@gmail.com'
        cidade = 'sao paulo'
        titulo = "post super post"
        adiciona_usuario(conn, nome, email, cidade)
        adiciona_post(conn, acha_id_usuario(conn, email), titulo, texto='todo o #bem-te-vi que eu vi hoje estava cantando')
        posts_id.append(acha_post(conn, acha_id_usuario(conn, email), titulo))

        nome = 'pedro'
        email = 'pedroer@gmail.com'
        cidade = 'sao paulo'
        titulo = "post super post"
        adiciona_usuario(conn, nome, email, cidade)
        adiciona_post(conn, acha_id_usuario(conn, email), titulo, texto='gente!!! quem viu o #sabia enorme que tinha no parque?? @salomao oi')
        posts_id.append(acha_post(conn, acha_id_usuario(conn, email), titulo))

        nome = 'carlos'
        email = 'carlitos@gmail.com'
        cidade = 'rio de janeiro'
        titulo = "post super post"
        adiciona_usuario(conn, nome, email, cidade)
        adiciona_post(conn, acha_id_usuario(conn, email), titulo, texto='foi lindo o dia hoje')
        posts_id.append(acha_post(conn, acha_id_usuario(conn, email), titulo))

        nome = 'santana'
        email = 'santanexx@gmail.com'
        cidade = 'sao paulo'
        titulo = "post super post"
        adiciona_usuario(conn, nome, email, cidade)
        adiciona_post(conn, acha_id_usuario(conn, email), titulo)
        posts_id.append(acha_post(conn, acha_id_usuario(conn, email), titulo))

        # Verifica se os perigos foram adicionados corretamente.
        res = lista_post_ativo(conn)
        self.assertCountEqual(res, posts_id)

        # Remove os perigos.
        for p in posts_id:
            muda_ativo_post(conn, p)

        # Verifica que todos os perigos foram removidos.
        res = lista_post_ativo(conn)
        self.assertFalse(res)

    def test_lista_usuario(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem perigos no sistema.
        res = lista_usuarios_ativos(conn)
        self.assertFalse(res)

        # Adiciona alguns perigos.
        usuarios_id = []
        nome = 'salomao'
        email = 'salomao@gmail.com'
        cidade = 'sao paulo'
        adiciona_usuario(conn, nome, email, cidade)
        usuarios_id.append(acha_id_usuario(conn, email))

        nome = 'pedro'
        email = 'pedroer@gmail.com'
        cidade = 'sao paulo'
        adiciona_usuario(conn, nome, email, cidade)
        usuarios_id.append(acha_id_usuario(conn, email))

        nome = 'carlos'
        email = 'carlitos@gmail.com'
        cidade = 'rio de janeiro'
        adiciona_usuario(conn, nome, email, cidade)
        usuarios_id.append(acha_id_usuario(conn, email))

        nome = 'santana'
        email = 'santanexx@gmail.com'
        cidade = 'sao paulo'
        adiciona_usuario(conn, nome, email, cidade)
        usuarios_id.append(acha_id_usuario(conn, email))

        # Verifica se os perigos foram adicionados corretamente.
        res = lista_usuarios_ativos(conn)
        self.assertCountEqual(res, usuarios_id)

        # Remove os perigos.
        for u in usuarios_id:
            muda_ativo_usuario(conn, u)

        # Verifica que todos os perigos foram removidos.
        res = lista_usuarios_ativos(conn)
        self.assertFalse(res)

# # NEEDS FIX
    def test_lista_passaros(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem perigos no sistema.
        res = lista_passaros_ativos(conn)
        self.assertFalse(res)

        # Adiciona alguns perigos.
        passaros_id = []
        passaro = 'beija-flor'
        adiciona_passaros(conn, passaro)
        passaros_id.append(acha_passaros(conn, passaro))

        passaro = 'bem-te-vi'
        adiciona_passaros(conn, passaro)
        passaros_id.append(acha_passaros(conn, passaro))

        passaro = 'sabia'
        adiciona_passaros(conn, passaro)
        passaros_id.append(acha_passaros(conn, passaro))

        passaro = 'tucano'
        adiciona_passaros(conn, passaro)
        passaros_id.append(acha_passaros(conn, passaro))

        passaro = 'tico-tico'
        adiciona_passaros(conn, passaro)
        passaros_id.append(acha_passaros(conn, passaro))

        # Verifica se os perigos foram adicionados corretamente.
        res = lista_passaros_ativos(conn)
        self.assertCountEqual(res, passaros_id)

        # Remove os perigos.
        for p in passaros_id:
            muda_ativo_passaros(conn, p)

        # Verifica que todos os perigos foram removidos.
        res = lista_passaros_ativos(conn)
        self.assertFalse(res)

    def test_adiciona_post(self):
        conn = self.__class__.connection

        nome = 'paulost'
        email = 'paulost@mememail.com'
        cidade = 'sao paulo'

        # Adiciona um perigo não existente.
        adiciona_usuario(conn, nome, email, cidade)

        passaro = 'beija-flor'

        # Adiciona um perigo não existente.
        adiciona_passaros(conn, passaro)
    
        titulo = 'meu primeiro post'
        texto = 'oi pessoal!! to postando aqui so pra dizer que fui passear pelo ibira e vi um #beija-flor oi'
        id_criador = acha_id_usuario(conn, email)
        adiciona_post(conn, id_criador, titulo, texto=texto)

        titulo = 'meu primeiro posto'
        adiciona_post(conn, id_criador, titulo, texto=texto)

        titulo = 'meu primeiro postu'
        adiciona_post(conn, id_criador, titulo, texto=texto)

        listinha = ve_posts_usuario_nao_cronologica(conn, id_criador)

        self.assertEqual(listinha[0], 'meu primeiro post')
        self.assertEqual(listinha[1], 'meu primeiro posto')
        self.assertEqual(listinha[2], 'meu primeiro postu')

    def test_usuario_mais_popular(self):
        conn = self.__class__.connection

        resto = 1

        # adicionando posts e usuarios
        nome = 'salomao'
        email = 'salomao@gmail.com'
        cidade = 'sao paulo'
        adiciona_usuario(conn, nome, email, cidade)
        id_criador = acha_id_usuario(conn, email)
        titulo = "A"
        texto = "A"
        url = "A"
        adiciona_post(conn, id_criador, titulo, texto=texto)

        nome = 'pedro'
        email = 'pedroer@gmail.com'
        cidade = 'sao paulo'
        adiciona_usuario(conn, nome, email, cidade)
        id_criador = acha_id_usuario(conn, email)
        titulo = "Bla"
        texto = "B"
        url = "B"
        adiciona_post(conn, id_criador, titulo, texto=texto)
        

        nome = 'carlos'
        email = 'carlitos@gmail.com'
        cidade = 'rio de janeiro'
        adiciona_usuario(conn, nome, email, cidade)
        id_criador = acha_id_usuario(conn, 'pedroer@gmail.com')
        post_id = acha_post(conn, id_criador, "Bla")
        adiciona_view_user_post(conn, post_id, acha_id_usuario(conn, email), resto, "resto", "resto")

        nome = 'santana'
        email = 'santanexx@gmail.com'
        cidade = 'sao paulo'
        adiciona_usuario(conn, nome, email, cidade)
        id_criador = acha_id_usuario(conn, 'pedroer@gmail.com')
        post_id = acha_post(conn, id_criador, "Bla")
        adiciona_view_user_post(conn, post_id, acha_id_usuario(conn, email), resto, resto, resto)



        self.assertEqual(acha_id_usuario(conn, 'pedroer@gmail.com'), usuario_mais_popular_cidade(conn, "sao paulo")[0])



def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u' + config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir() 
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)
    # run_sql_script('script1.sql')
    # run_sql_script('script2.sql')
    # run_sql_script('script3.sql')

def tearDownModule():
    run_sql_script('../scripts_DB/tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=3)