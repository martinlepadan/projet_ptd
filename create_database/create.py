import sqlite3
import os
import pandas as pd

PATH = os.path.join(os.getcwd(), "create_database")
PATH_DATA = os.path.join(PATH, "donnees_formule_un")
order = [
    "circuits",
    "constructors",
    "drivers",
    "seasons",
    "status",
    "races",
    "constructor_results",
    "constructor_standings",
    "driver_standings",
    "lap_times",
    "pit_stops",
    "qualifying",
    "results",
    "sprint_results",
]


def insert_csv(table_name, csv_file):
    file_path = os.path.join(PATH_DATA, csv_file)
    df = pd.read_csv(file_path)
    try:
        df.to_sql(table_name, connection, if_exists="append", index=False)
        print(f"Données insérées dans la table '{table_name}'.")
    except Exception as e:
        print(f"Erreur lors de l'insertion dans '{table_name}': {e}")


connection = sqlite3.connect("formule_1.db")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

with open(os.path.join(PATH, "request.sql"), "r") as sqlfile:
    request = sqlfile.read()

list_request = [r.strip() for r in request.split(";") if r.strip()]
for i, r in enumerate(list_request):
    try:
        cursor.execute(r)
        insert_csv(order[i], order[i] + ".csv")
    except sqlite3.Error as e:
        print(f"Erreur SQL : {e}\nRequête : {r}")
        break

connection.commit()
connection.close()
