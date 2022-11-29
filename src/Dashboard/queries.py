import mysql.connector
def conectar():
 conn = mysql.connector.connect(user='root',password='root',database='Customizacao',port='3306')
 return conn
