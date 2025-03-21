import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.getcwd(), 'formule_1.db')
QUERY_PATH = os.path.join(os.getcwd(), 'app', 'queries.txt')


def get_query_as_df(query, params):
    connection = sqlite3.connect(DB_PATH)
    try:
        result = pd.read_sql_query(query, connection, params=[params])
        return result
    except sqlite3.Error as e:
        print(f"Erreur SQL : {e}\nRequête : {query}")

    connection.close()
