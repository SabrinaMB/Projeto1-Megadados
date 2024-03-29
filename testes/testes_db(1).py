import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql

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

################################## TABELAS PRIMARIAS ##################################
# ADICIONA
#
    def test_adiciona_usuario(self):
        conn = self.__class__.connection
    
        nome = 'paulost'
        email = 'paulost@mememail.com'
        cidade = 'sao paulo'

        # Adiciona um perigo não existente.
        adiciona_usuario(conn, nome, email, cidade)

        # Tenta adicionar o mesmo perigo duas vezes.
        try:
            adiciona_usuario(conn, nome, email, cidade)
            self.fail('Nao deveria ter adicionado o mesmo usuario duas vezes.')
        except ValueError as e:
            pass

        # Checa se o usuario existe.
        id = acha_usuario_email(conn, email)
        self.assertIsNotNone(id)

        # Tenta achar um usuario inexistente.
        id = acha_usuario_email(conn, 'mailzinho@pompom.com')
        self.assertIsNone(id)
#
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
        
            titulo = 'meu primeirp post'
            texto = 'oi pessoal!! to postando aqui so pra dizer que fui passear pelo ibira e vi um #beija-flor'
            id_criador = '0'

            # Adiciona um perigo não existente.
            adiciona_post(conn, id_criador, titulo, texto=texto)

            # Tenta adicionar o mesmo perigo duas vezes.
            try:
                adiciona_post(conn, id_criador, titulo, texto=texto)
                self.fail('Nao deveria ter adicionado o mesmo post duas vezes.')
            except ValueError as e:
                pass

            # Checa se o usuario existe.
            id = acha_post(conn, id_criador, titulo)
            self.assertIsNotNone(id)

            # Tenta achar um usuario inexistente.
            id = acha_post(conn, id, titulo)
            self.assertIsNone(id)
#
    def test_adiciona_passaro(self):
            conn = self.__class__.connection
        
            passaro = 'bem-te-vi'

            # Adiciona um perigo não existente.
            adiciona_passaros(conn, passaro)

            # Tenta adicionar o mesmo perigo duas vezes.
            try:
                adiciona_passaros(conn, passaro)
                self.fail('Nao deveria ter adicionado o mesmo passaro duas vezes.')
            except ValueError as e:
                pass

            # Checa se o usuario existe.
            id = acha_passaros(conn, passaro)
            self.assertIsNotNone(id)

            # Tenta achar um usuario inexistente.
            id = acha_passaros(conn, "mal-te-vi")
            self.assertIsNone(id)

# REMOVE

#
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
        texto = 'oi pessoal!! to postando aqui so pra dizer que fui passear pelo ibira e vi um #beija-flor'
        id_criador = '1'

        # Adiciona um perigo não existente.
        adiciona_post(conn, titulo, id_criador, texto=texto)
        id = acha_post(conn, titulo, id_criador)

        res = lista_post_ativo(conn)
        self.assertCountEqual(res, (id,))

        muda_ativo_post(conn, id)

        res = lista_post_ativo(conn)
        self.assertFalse(res)

# MUDA

    
# LISTA
# NEEDS FIX
    def test_lista_usuario(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem perigos no sistema.
        res = lista_perigos(conn)
        self.assertFalse(res)

        # Adiciona alguns perigos.
        perigos_id = []
        for p in ('nuclear', 'moral', 'emocional'):
            adiciona_perigo(conn, p)
            perigos_id.append(acha_perigo(conn, p))

        # Verifica se os perigos foram adicionados corretamente.
        res = lista_perigos(conn)
        self.assertCountEqual(res, perigos_id)

        # Remove os perigos.
        for p in perigos_id:
            remove_perigo(conn, p)

        # Verifica que todos os perigos foram removidos.
        res = lista_perigos(conn)
        self.assertFalse(res)
# NEEDS FIX
    def test_lista_perigos(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem perigos no sistema.
        res = lista_perigos(conn)
        self.assertFalse(res)

        # Adiciona alguns perigos.
        perigos_id = []
        for p in ('nuclear', 'moral', 'emocional'):
            adiciona_perigo(conn, p)
            perigos_id.append(acha_perigo(conn, p))

        # Verifica se os perigos foram adicionados corretamente.
        res = lista_perigos(conn)
        self.assertCountEqual(res, perigos_id)

        # Remove os perigos.
        for p in perigos_id:
            remove_perigo(conn, p)

        # Verifica que todos os perigos foram removidos.
        res = lista_perigos(conn)
        self.assertFalse(res)

################################## TABELAS SECUNDARIAS ##################################

# ADICIONA
    
    # usar essa fnc
    #@unittest.skip('Em desenvolvimento.')
    def test_adiciona_perigo_a_comida(self):
        conn = self.__class__.connection

        # Cria algumas comidas.
        adiciona_comida(conn, 'coxinha')
        id_coxinha = acha_comida(conn, 'coxinha')

        adiciona_comida(conn, 'kibe')
        id_kibe = acha_comida(conn, 'kibe')

        # Cria alguns perigos.
        adiciona_perigo(conn, 'estomacal')
        id_estomacal = acha_perigo(conn, 'estomacal')
        
        adiciona_perigo(conn, 'moral')
        id_moral = acha_perigo(conn, 'moral')
        
        adiciona_perigo(conn, 'emocional')
        id_emocional = acha_perigo(conn, 'emocional')

        adiciona_perigo(conn, 'viral')
        id_viral = acha_perigo(conn, 'viral')

        # Conecta comidas e perigos.
        adiciona_perigo_a_comida(conn, id_estomacal, id_coxinha)
        adiciona_perigo_a_comida(conn, id_estomacal, id_kibe)
        adiciona_perigo_a_comida(conn, id_viral, id_coxinha)
        adiciona_perigo_a_comida(conn, id_viral, id_kibe)
        adiciona_perigo_a_comida(conn, id_moral, id_coxinha)
        adiciona_perigo_a_comida(conn, id_emocional, id_kibe)

        res = lista_comidas_de_perigo(conn, id_estomacal)
        self.assertCountEqual(res, (id_coxinha, id_kibe))

        res = lista_comidas_de_perigo(conn, id_viral)
        self.assertCountEqual(res, (id_coxinha, id_kibe))

        res = lista_comidas_de_perigo(conn, id_moral)
        self.assertCountEqual(res, (id_coxinha,))

        res = lista_comidas_de_perigo(conn, id_emocional)
        self.assertCountEqual(res, (id_kibe,))

        res = lista_perigos_de_comida(conn, id_coxinha)
        self.assertCountEqual(res, (id_estomacal, id_viral, id_moral))

        res = lista_perigos_de_comida(conn, id_kibe)
        self.assertCountEqual(res, (id_estomacal, id_viral, id_emocional))

        # Testa se a remoção de uma comida causa a remoção das relações entre essa comida e seus perigos.
        remove_comida(conn, id_kibe)

        res = lista_comidas_de_perigo(conn, id_estomacal)
        self.assertCountEqual(res, (id_coxinha,))

        res = lista_comidas_de_perigo(conn, id_viral)
        self.assertCountEqual(res, (id_coxinha,))

        res = lista_comidas_de_perigo(conn, id_emocional)
        self.assertFalse(res)

        # Testa se a remoção de um perigo causa a remoção das relações entre esse perigo e suas comidas.
        remove_perigo(conn, id_viral)

        res = lista_perigos_de_comida(conn, id_coxinha)
        self.assertCountEqual(res, (id_estomacal, id_moral))

        # Testa a remoção específica de uma relação comida-perigo.
        remove_perigo_de_comida(conn, id_estomacal, id_coxinha)

        res = lista_perigos_de_comida(conn, id_coxinha)
        self.assertCountEqual(res, (id_moral,))

    # NEEDS FIX
    def adiciona_preferencia(self):
        conn = self.__class__.connection

        comida = 'coxinha'

        # Adiciona comida não existente.
        adiciona_comida(conn, comida)

        # Tenta adicionar a mesma comida duas vezes.
        try:
            adiciona_comida(conn, comida)
            self.fail('Nao deveria ter adicionado a mesma comida duas vezes.')
        except ValueError as e:
            pass

        # Checa se a comida existe.
        id = acha_comida(conn, comida)
        self.assertIsNotNone(id)

        # Tenta achar uma comida inexistente.
        id = acha_comida(conn, 'esfiha')
        self.assertIsNone(id)

    # NEEDS FIX
    def adiciona_view_user_post(self):

# REMOVE

    def test_remove_comida(self):
        conn = self.__class__.connection
        adiciona_comida(conn, 'coxinha')
        id = acha_comida(conn, 'coxinha')

        res = lista_comidas(conn)
        self.assertCountEqual(res, (id,))

        remove_comida(conn, id)

        res = lista_comidas(conn)
        self.assertFalse(res)

# MUDA

    def test_muda_nome_comida(self):
        conn = self.__class__.connection

        adiciona_comida(conn, 'alface')
        adiciona_comida(conn, 'tomate')
        id = acha_comida(conn, 'tomate')

        # Tenta mudar nome para algum nome já existente.
        try:
            muda_nome_comida(conn, id, 'alface')
            self.fail('Não deveria ter mudado o nome.')
        except ValueError as e:
            pass

        # Tenta mudar nome para nome inexistente.
        muda_nome_comida(conn, id, 'azeitona')

# LISTA

    def test_lista_comidas(self):
        conn = self.__class__.connection

        # Verifica que ainda não tem comidas no sistema.
        res = lista_comidas(conn)
        self.assertFalse(res)

        # Adiciona algumas comidas.
        comidas_id = []
        for p in ('abacaxi', 'tomate', 'cebola'):
            adiciona_comida(conn, p)
            comidas_id.append(acha_comida(conn, p))

        # Verifica se as comidas foram adicionadas corretamente.
        res = lista_comidas(conn)
        self.assertCountEqual(res, comidas_id)

        # Remove as comidas.
        for c in comidas_id:
            remove_comida(conn, c)

        # Verifica que todos as comidas foram removidas.
        res = lista_comidas(conn)
        self.assertFalse(res)

# SIMULACAO DE DB

    def simula_db(self):
        conn = self.__class__.connection
                
        nome = 'paulost'
        email = 'paulost@mememail.com'
        cidade = 'Sao Paulo'
        adiciona_usuario(conn, nome=nome, email=email, cidade=cidade)
        idA = acha_usuario_email(conn, email)

        nome = 'mattobs'
        email = 'mattobers@mememail.com'
        cidade = 'Tokio'
        adiciona_usuario(conn, nome, email, cidade)
        idB = acha_usuario_email(conn, email)

        nome = 'leonidas'
        email = 'leozinho@mememail.com'
        cidade = 'Nova York'
        adiciona_usuario(conn, nome, email, cidade)

        id = acha_usuario_email(conn, email)

        titulo = "postinho"
        texto  = "Gente!! Olha só o #sabia e #corvo que eu vi no parque!! Super bem-acompanhada @elainerf @deborah.123 amo voces S2!!"
        adiciona_post(conn, id_criador=id, titulo=titulo, texto=texto)

        id = acha_post(conn, titulo=titulo, id_criador=id)
        adiciona_view_user_post(conn, id_post=id, id_usuario=idA, so="mac", ip="1", browser="chrome")
        adiciona_view_user_post(conn, id_post=id, id_usuario=idB, so="windows", ip="2", browser="matte")
        


def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
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

def tearDownModule():
    run_sql_script('tear_down.sql')

if _name_ == '_main_':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)