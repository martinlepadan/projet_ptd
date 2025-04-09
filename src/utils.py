"""Fichier contenant des fonctions transversales (je fais genre je connais des mots)."""

import sqlite3
import os
import pandas as pd
from functools import reduce
import csv

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


def check_dfs(dfs: list, keys: list):
    names = [
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

    if not (isinstance(dfs, list) and isinstance(keys, list)):
        raise TypeError("dfs et keys doivent être des listes")
    if len(dfs) == 0:
        raise ValueError("dfs ne peut pas être vide")
    if any(df not in names for df in dfs):
        raise ValueError("La liste de noms contient un/des noms invalides")

    if len(keys) != len(dfs) - 1:
        raise ValueError("Nombre de clés incorrectes")


def get_pd_df(dfs: list, keys: list) -> pd.DataFrame:
    """ """

    check_dfs(dfs, keys)

    df_to_merge = []
    for i, df in enumerate(dfs):
        exec(
            df + " = pd.read_csv('./create_database/donnees_formule_un/" + df + ".csv')"
        )
        exec("df_to_merge.append(" + df + ")")

        df_merged = reduce(
            lambda left, right: pd.merge(left, right, on=keys, how="inner"), df_to_merge
        ).fillna("void")

    return df_merged


def get_python_df(dfs: list, keys: list):
    """ """

    check_dfs(dfs, list)

    for df in dfs:
        with open('eggs.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                print(', '.join(row))
