import mysql.connector

mysqlconn = mysql.connector.connect(user = 'root', password = 'root',
                               host = 'localhost', port='3306', database='Customizacao')
mysqlcursor = mysqlconn.cursor()

def login(email, senha):
    syntax = ('select u.email,u.senha,c.nome,a.numeroAgencia from usuario as u'
              ' join cargo as c on c.id = u.fkCargo join Agencia as A on u.fkAgencia = a.id where u.email = %s and senha = %s;')
    values = [email, senha]
    mysqlcursor.execute(syntax, values)
    rows = mysqlcursor.fetchall()

    email = rows[0][0]
    senha = rows[0][1]
    cargo = rows[0][2]
    agencia = rows[0][3]

    vetor = []
    vetor.append(email)
    vetor.append(senha)
    vetor.append(cargo)
    vetor.append(agencia)
    if mysqlcursor.rowcount != 1:
        return False
    return vetor

def cadastrar(email, senha, cargo, agencia):
 try:
    syntax = ('insert into Usuario(email,senha,fkCargo,fkAgencia)'
              ' values (%s,%s,(select id from cargo where codigo = %s),'
              '(select id from Agencia where numeroAgencia = %s))')
    values = [email, senha,cargo,agencia]
    mysqlcursor.execute(syntax, values)
    mysqlconn.commit()
    return True
 except:
    return False

def menu():
    print("Bem vindo ao menu Track Vision - GreenPower")
    while True:
        escolha = input("Selecione uma opção \n"
                        "1 - Desejo me Logar \n"
                        "2 - Desejo me Cadastrar\n")
        if escolha != "1" and escolha != "2":
            print("Opção Inválida")
        else:
            if escolha == '1':
                email = input("Digite seu Email \n")
                if email.find('@') == -1:
                    print('formato de email inválido')
                else:
                 senha = input("Digite sua Senha \n")
                 resposta = login(email, senha)
                 if not resposta:
                    print("Houve um problema ao realizar o Login!!!")
                 else:
                    print('Logado como ' + resposta[2])
                    return resposta
                    break
            else:
                cademail = input("Digite seu Email \n")
                if email.find('@') == -1:
                    print('formato de email inválido')
                else:
                 cadsenha = input("Digite sua Senha \n")
                 cadcargo = int(input("Digite o código do seu Cargo \n"))
                 cadagencia = int(input("Digite o código da sua Agencia \n"))

                 resposta = cadastrar(cademail, cadsenha, cadcargo, cadagencia)
                 if resposta:
                    break
                 else:
                    print("Houve um problema ao realizar o Cadastro!!!")