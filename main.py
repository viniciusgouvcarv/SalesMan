import sqlite3 as sql
from time import sleep
from datetime import date, datetime
from tabulate import tabulate
import getpass
import hashlib

### INICIA O SISTEMA
def iniciar():
        global con
        global cur
        con = None
        cur = None

        print('')
        print('')
        print('Seja bem-vind@ ao gerenciador de estoque "FreeStock MEI"')
        print('')
        sleep(1)
        print('Criado por Vinícius de Carvalho')
        print('viniciusgouvcarv@gmail.com')
        print('')
        sleep(3)

    #try:
        con = sql.connect('loja.db')
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS estoque
                    (
                        cod_produto SERIAL PRIMARY KEY,
                        nome_produto VARCHAR(255) NOT NULL UNIQUE,
                        cod_barras VARCHAR(13),
                        ncm VARCHAR(8),
                        tipo_un VARCHAR(2) NOT NULL,
                        quant_estoque NUMERIC NOT NULL,
                        preco_un NUMERIC NOT NULL,
                        obs_produto VARCHAR(510)
                    );
        ''')

        cur.execute('''CREATE TABLE IF NOT EXISTS vendedores
                    (
                        cod_vendedor SERIAL PRIMARY KEY,
                        nome_vendedor VARCHAR(255) NOT NULL UNIQUE,
                        cargo VARCHAR(255) NOT NULL,
                        senha VARCHAR(1000) NOT NULL,
                        obs_vendedor VARCHAR(510)
                    );
        ''')

        cur.execute('''CREATE TABLE IF NOT EXISTS vendas
                    (
                        cod_venda SERIAL PRIMARY KEY,
                        data_venda DATE NOT NULL,
                        horario_venda TIME NOT NULL,
                        tipo_pgt VARCHAR(255) NOT NULL,
                        valor_sub_ttl NUMERIC NOT NULL,
                        valor_ttl NUMERIC NOT NULL,
                        desconto NUMERIC,
                        valor_pago NUMERIC NOT NULL,
                        troco NUMERIC NOT NULL,
                        obs_venda VARCHAR(510),
                        vendedor INTEGER,
                        produto INTEGER,
                        FOREIGN KEY (vendedor) REFERENCES vendedores (cod_vendedor) ON DELETE CASCADE,
                        FOREIGN KEY (produto) REFERENCES estoque (cod_produto) ON DELETE CASCADE
                    );
        ''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS log
                    (
                        cod_ato SERIAL PRIMARY KEY,
                        data_ato DATE NOT NULL,
                        horario_ato TIME NOT NULL,
                        nome_ato VARCHAR(255)
                    )
        ''')

        inicio()

    #except sql.OperationalError as e:
    #    print('Houve um erro ao tentar conexão com o banco de dados. Tente novamente.')
    #    print('')
    #    print(e)

### MENU INICIAL (PARA IR PARA O MENU DE VENDAS, ESTOQUE, VENDEDORES OU AJUDA)
def inicio():
    while True:
        print('-'*20)
        i = input('Digite "venda", "estoque", "vendedor", "relatório" ou "ajuda": ')
        print('')

        if "venda" in i:
            return venda()

        elif ("estoque" in i) or ("produto" in i):
            return estoque()

        elif "vendedo" in i:
            return vendedor()

        elif "aju" in i:
            ajuda()
            return inicio()

        elif "rel" in i:
            return relatorio()

        else:
            pass

### MENU DE VENDAS (PARA CRIAR, EDITAR, APAGAR E CONSULTAR VENDAS)
def venda():
    print('-'*20)
    print('VOCÊ ESTÁ NO MENU DE VENDAS')
    print('')
    i = input('Digite "nova", "editar", "apagar", "consultar", "ajuda" ou "retornar": ')
    print('')

    if "nov" in i:
        return nova_venda()

    elif "edit" in i:
        return editar_venda()

    elif "apag" in i:
        return apagar_venda()

    elif "cons" in i:
        return consultar_venda()

    elif "aju" in i:
        ajuda()
        return venda()

    elif "retornar" in i:
        inicio()

### MENU DE PRODUTOS (PARA CRIAR, EDITAR, APAGAR E CONSULTAR PRODUTOS)
def estoque():
    if "nov" in i:
        return novo_produto()

    elif "edit" in i:
        return editar_produto()

    elif "apag" in i:
        return apagar_produto()

    elif "cons" in i:
        return consultar_produto()

    elif "aju" in i:
        ajuda()
        return estoque()

    elif "retornar" in i:
        inicio()

### MENU DE VENDEDORES (PARA CRIAR, EDITAR, APAGAR E CONSULTAR VENDEDORES)
def vendedor():
    print('-'*20)
    print('VOCÊ ESTÁ NO MENU DE VENDEDORES')
    print('')
    i = input('Digite "novo", "editar", "apagar", "consultar", "ajuda" ou "retornar": ')
    print('')

    if "nov" in i:
        return novo_vendedor()

    elif "edit" in i:
        return editar_vendedor()

    elif "apag" in i:
        return apagar_vendedor()

    elif "cons" in i:
        return consultar_vendedor()

    elif "aju" in i:
        ajuda()
        return vendedor()

    elif "retornar" in i:
        inicio()

### AJUDA (TEXTO INFORMATIVO EXPLICANDO O SISTEMA)
def ajuda():
    ###
    print('Ajudando')
    print('')

def nova_venda():
    ###
    return

def editar_venda():
    ###
    return

def consultar_venda():
    ###
    return

def apagar_venda():
    ###
    return

def novo_vendedor():
        print('-'*20)
        global cur
        global con

        cur.execute("""
            SELECT * FROM vendedores
        """)

        if len(cur.fetchall()) == 0:
            print('Como não há vendedores cadastrados, vamos criar o administrador agora.')
            print('')
            nome = input('Qual o nome do administrador? Lembre-se de que ele deve ser único: ').capitalize()
            if nome == "":
                while True:
                    nome = input('Por favor, informe um nome ou digite "retornar" para voltar ao menu anterior: ').capitalize()
                    print('')
                    if nome == "Retornar":
                        return vendedor()
                    elif nome != "":
                        break
                    else:
                        pass

            obs = input('Há alguma observação sobre o administrador? Se não, só aperter "enter": ')
            senha = getpass.getpass('Agora, a senha: ')
            if senha == "":
                while True:
                    senha = getpass.getpass('Por favor, informe uma senha ou digite "retornar" para voltar ao menu anterior: ').capitalize()
                    print('')
                    if senha == "Retornar":
                        return vendedor()
                    elif senha != "":
                        break
                    else:
                        pass
            senha = hashlib.md5(senha.encode()).hexdigest()
            print('')

            comando = "INSERT INTO vendedores (cod_vendedor, nome_vendedor, cargo, obs_vendedor, senha) VALUES (0, '"+nome+"', 'admin','"+obs+"','"+senha+"');"
            
            try:
                cur.execute(comando)
                print('Administrador', nome, 'criado com sucesso!')
                print('')
                con.commit()
                hoje = date.today()
                agora = datetime.now().time()
                cur.execute('INSERT INTO log (nome_ato, data_ato, horario_ato) VALUES ("Administrador',nome,'criado pelo sistema.", %s, %s)', (hoje, agora))
                con.commit()

            except:
                print('Houve algum erro')
                print('')

        else:
            admin = input('Insira o código ou nome do administrador que irá criar o usuário: ')
            print('')

            cur.execute('SELECT nome_vendedor, senha, cargo FROM vendedores WHERE cargo = "administrador" AND (cod_vendedor = %s OR nome_vendedor = "%s");', (admin, admin))
            busca = cur.fetchone()
            if len(busca) == 0:
                print('Não encontramos nenhum administrador com esse código ou nome.')
                print('')
                return vendedor()
            
            else:
                admin = busca[0]
                senha_encontrada = busca[1]

            senha_admin = getpass.getpass('Insira a senha: ')
            print('')

            if senha_admin == senha_encontrada:
                cargo = input('Você está criando um "vendedor" ou um "administrador"? ')
                print('')
                if cargo == "":
                    while True:
                        cargo = input('Por favor, digite "vendedor" ou "administrador" para adicionar um cargo, ou "retornar" para voltar ao menu anterior: ')
                        print('')
                        if "torn" in cargo:
                            return vendedor()
                        elif "vend" in cargo:
                            cargo = "vendedor"
                            break
                        elif "adm" in cargo:
                            cargo = "administrador"
                            break
                        else:
                            pass

                nome = input('Qual o nome do '+cargo+'? Lembre-se de que ele deve ser único: ').capitalize()
                if nome == "":
                    while True:
                        nome = input('Por favor, informe um nome ou digite "retornar" para voltar ao menu anterior: ').capitalize()
                        print('')
                        if nome == "Retornar":
                            return vendedor()
                        elif nome != "":
                            break
                        else:
                            pass

                obs = input('Há alguma observação sobre o '+cargo+'? Se não, só aperter "enter": ')
                senha = getpass.getpass('Agora, a senha: ')
                if senha == "":
                    while True:
                        senha = getpass.getpass('Por favor, informe uma senha ou digite "retornar" para voltar ao menu anterior: ').capitalize()
                        print('')
                        if senha == "Retornar":
                            return vendedor()
                        elif senha != "":
                            break
                        else:
                            pass
                senha = hashlib.md5(senha.encode()).hexdigest()
                print('')

                comando = "INSERT INTO vendedores (nome_vendedor, cargo, obs_vendedor, senha) VALUES ('"+nome+"', 'admin','"+obs+"','"+senha+"');"
                
                try:
                    cur.execute(comando)
                    print(cargo.capitalize(), nome, 'criado com sucesso!')
                    print('')
                    con.commit()
                    hoje = date.today()
                    agora = datetime.now().time()
                    cur.execute('INSERT INTO log (nome_ato, data_ato, horario_ato) VALUES ("Administrador',nome,'criado pelo sistema.", %s, %s);', (hoje, agora))
                    con.commit()

                except sql.IntegrityError:
                    print('O nome do', cargo, 'deve ser único. Tente novamente, por favor.')
                    print('')
                    return novo_vendedor()

                except:
                    print('Houve algum erro.')
                    print('')
            
            else:
                print('Senha inválida.')
                print('')
                hoje = date.today()
                agora = datetime.now().time()
                cur.execute('INSERT INTO log (nome_ato, data_ato, horario_ato) VALUES ("Tentativa de criar usuário barrada por invalidade da senha.", %s, %s);', (hoje, agora))
                con.commit()

        return vendedor()

def editar_vendedor():
    ###
    return

def consultar_vendedor():
    global cur
    
    i = input('Qual o nome do vendedor/administrador que você quer consultar? Para listar todos, deixe em branco: ')
    print('')

    if i == 'retornar':
        return vendedor()

    elif i == "":
        comando = "SELECT cod_vendedor, nome_vendedor, cargo, obs_vendedor FROM vendedores;"

    else:
        comando = "SELECT cod_vendedor, nome_vendedor, cargo, obs_vendedor FROM vendedores WHERE nome_vendedor IN '"+i+"';"

    cur.execute(comando)
    vendedores = cur.fetchall()

    print('-'*20)

    if len(vendedores) == 0:
        print('Não há vendedores ou administradores que atinjam os requisitos desejados.')
        print('')
        return vendedor()

    else:
        nomes = []
        cods = []
        cargos = []
        obs = []

        for vendedor in vendedores:
            cods.append(vendedor[0])
            nomes.append(vendedor[1])
            if "vend" in vendedor[2]:
                cargos.append("Vendedor")
            else:
                cargos.append("Administrador")
            
            if vendedor[3] == "":
                obs.append("Nenhuma")
            else:
                obs.append(vendedor[3])

        lista = {'ID': cods, 'Nome': nomes, 'Cargo': cargos, 'Observações': obs}
        print('VENDEDORES/ADMINISTRADORES ENCONTRADOS')
        print(tabulate(lista, showindex=False, headers='keys', tablefmt='grid'))

        return inicio()

def apagar_vendedor():
    ###
    return

def novo_produto():
    ###
    return

def editar_produto():
    ###
    return

def consultar_produto():
    ###
    return

def apagar_produto():
    ###
    return

iniciar()