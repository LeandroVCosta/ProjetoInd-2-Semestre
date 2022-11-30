import pandas as pd
import os


import sqlalchemy

server = 'trackvisiondb.database.windows.net'
database = 'trackvisiondb'
username = 'CloudSA49c766d4'
password = 'Urubu1004'
driver = 'ODBC+DRIVER+17+for+SQL+Server'
engine_stmt = ("mssql+pyodbc://%s:%s@%s/%s?driver=%s" % (username, password, server, database, driver ))
conn = sqlalchemy.create_engine(engine_stmt)


sql = "select * from dadoEnergia where fkCaixa = 1 and consumo <> 0;"
sqlframe = pd.read_sql(sql,conn)
sqlframe["momento"] = pd.to_datetime(sqlframe["momento"])
""" sqlframe["momento"] = sqlframe["momento"].apply(lambda x: x.date()) """

syntax = ("select AVG(consumo) from dadoEnergia where fkCaixa = 1")
result =conn.execute(syntax)
for row in result:
    media = int(row[0]) * 20 * 10

estimativa = round(float(((media * 24 * 30) / 1000) * 1.04),2)
print(estimativa)


syntax = ("select TOP 1 plano from dadoEnergia where fkCaixa=1 ")
result = conn.execute(syntax)
for row in result:
  plano = str(row[0])
print(plano)
