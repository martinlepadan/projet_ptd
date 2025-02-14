import sqlite3
import os

PATH = os.path.join(os.getcwd(), 'create_database')
PATH_DATA = os.path.join(PATH, 'donnees_formule_un')

connection = sqlite3.connect('formule_1.db')
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

with open(os.path.join(PATH, 'request.sql'), 'r') as sqlfile:
    request = sqlfile.read()

list_request = [r.strip() for r in request.split(';') if r.strip()]
for r in list_request:
    try:
        cursor.execute(r)
    except sqlite3.Error as e:
        print(f"Erreur SQL : {e}\nRequête : {r}")
        break

connection.commit()
connection.close()
