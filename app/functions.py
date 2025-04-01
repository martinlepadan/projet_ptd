"""Fichier contenant des fonctions transversales (je fais genre je connais des mots)."""

import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.getcwd(), "formule_1.db")
QUERY_PATH = os.path.join(os.getcwd(), "app", "queries.txt")


def get_query_as_df(query: str, params: list = None) -> pd.DataFrame:
    """
    Exécute une requête SQL et retourne le résultat sous forme de DataFrame pandas.

    Params
    ------
        query (str): La requête SQL à exécuter.
        params (list): Une liste de paramètres à lier à la requête. Par défaut, None.

    Returns
    -------
        pandas.DataFrame: Le résultat de la requête sous forme de DataFrame.
    """

    connection = sqlite3.connect(DB_PATH)
    if not isinstance(params, list) and params is not None:
        raise TypeError("Les paramètres doivent être une liste ou None")
    try:
        if params is None:
            result = pd.read_sql_query(query, connection)
        else:
            result = pd.read_sql_query(query, connection, params=params)
        return result
    except sqlite3.Error as e:
        print(f"Erreur SQL : {e}\nRequête : {query}")

    connection.close()
