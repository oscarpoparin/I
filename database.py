import sqlite3
from sqlite3.dbapi2 import Cursor, connect

#coneccion con la base de datos

def create_connection():
    connection = sqlite3.connect("brain.db") #archivo de BD a conectar 
    return connection

#crear la coneccion de la base de datos

def get_table():
    connection = create_connection()                       #contendra la conexion
    cursor = connection.cursor()                           #creacion de consultas
    cursor.execute("SELECT * FROM questions_answers")      #generacion de consulta
    return cursor.fetchall()                                

#creacion de lista

bot_list = list()

#

def get_questions_answers():
    rows = get_table()                  
    for row in rows:                    # recorrido de duplas                    
        bot_list.extend(list(row))      # creacion de super lista
    return bot_list


#get_questions_answers()