import sqlalchemy


server = 'trackvisiondb.database.windows.net'
database = 'trackvisiondb'
username = 'CloudSA49c766d4'
password = 'Urubu1004'
driver = 'ODBC+DRIVER+17+for+SQL+Server'
engine_stmt = ("mssql+pyodbc://%s:%s@%s/%s?driver=%s" % (username, password, server, database, driver ))
conn = sqlalchemy.create_engine(engine_stmt)


def login(email, senha):
    syntax = ('select email,senha,fkBanco from Usuario where email = ? and senha = ?')
    values = [email, senha]
    valor = []
    rows = conn.execute(syntax, values)
    for row in rows:
        valor.append(row)
    if len(valor) != 1:
        return False
    return valor

def menu():
    while True:
                email = input("Digite seu Email \n")
                if email.find('@') == -1:
                    print('formato de email inválido')
                else:
                 senha = input("Digite sua Senha \n")
                 resposta = login(email, senha)
                 if resposta == False:
                    print("Houve um problema ao realizar o Login!!!")
                 else:
                     print('Login Realizado com Sucesso!')
                     return resposta
