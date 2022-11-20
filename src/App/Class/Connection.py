import mysql.connector
import pyodbc

def inserir(consumo,plano):
    mysqlconn = mysql.connector.connect(user='root', password='root', host='localhost',
                                        database='projetoIND', port='3306');
    mysqlcursor = mysqlconn.cursor()
    syntax = "insert into dadoEnergia (consumo,plano,momento) values (%s,%s, NOW())"
    values = [consumo,plano]
    mysqlcursor.execute(syntax,values)
    mysqlconn.commit()
    mysqlconn.close()

def getFluxo():

    server = 'trackvisiondb.database.windows.net'
    database = 'trackvisiondb'
    username = 'CloudSA49c766d4'
    password = 'Urubu1004'
    driver = '{ODBC Driver 17 for SQL Server}'

    conn = pyodbc.connect('DRIVER=' + driver + ';'
                        'SERVER=tcp:' + server + ';'
                        'PORT=1433;'
                        'DATABASE=' + database + ';'
                        'UID=' + username + ';'
                        'PWD=' + password)

    cursor = conn.cursor()
    syntax = "select top 10 avg(cpuPorcentagem) from Leitura"
    cursor.execute(syntax)
    rows = cursor.fetchone()
    conn.close()
    return int(rows[0])


