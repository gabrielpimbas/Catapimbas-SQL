import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",  # Endereço do servidor MySQL
        user="root",  # Usuário do banco de dados
        password="root@root",  # Senha do MySQL
        database="achados_perdidos",  # Nome do banco criado no Módulo 2
    )
