"""
Fichier contenant des fonctions et variables transversales
"""

import os
import pandas as pd
from functools import reduce
import csv


def get_pd_df(dfs: list, keys: list, columns: dict = None) -> pd.DataFrame:
    """
    Combine plusieurs DataFrames à partir de fichiers CSV en un seul DataFrame.

    Parameters
    ----------
        dfs (list): Liste des noms de fichiers CSV (sans extension) à charger
                    et fusionner.
        keys (list): Liste des colonnes clés utilisées pour effectuer les jointures.
        columns (dict, optional): Dictionnaire {nom_fichier: [colonnes]} pour restreindre
            les colonnes chargées de chaque fichier.

    Returns
    -------
        pd.DataFrame: DataFrame fusionné.
    """
    if not (isinstance(dfs, list) and isinstance(keys, list)):
        raise TypeError("dfs et keys doivent être des listes")
    if len(dfs) == 0:
        raise ValueError("dfs ne peut pas être vide")
    if len(keys) != len(dfs) - 1:
        raise ValueError("Nombre de clés incorrectes")

    loaded_dfs = []
    for df_name in dfs:
        df_path = os.path.join("data", df_name + ".csv")
        if columns and df_name in columns:
            loaded_dfs.append(pd.read_csv(df_path, usecols=columns[df_name]))
        else:
            loaded_dfs.append(pd.read_csv(df_path))

    df_merged = reduce(
        lambda left, right: pd.merge(left, right[1], on=right[0], how="inner"),
        zip(keys, loaded_dfs[1:]),
        loaded_dfs[0],
    ).fillna("NA")

    return df_merged


def csv_to_rows(file_name: str) -> tuple[list[str], list[dict[str, str]]]:
    """
    Convertit un fichier CSV en un dictionnaire.

    Parameters
    ----------
        file_name (str): Le nom du fichier CSV (sans l'extension) à convertir.

    Return
    ------
        tuple[list[str], list[dict[str, str]]]: Une paire contenant :
            - Une liste des en-têtes du fichier CSV.
            - Une liste contenant un dictionnaire par ligne avec comme clé
              la variable
    """

    df_path = os.path.join(os.getcwd(), "data", file_name + ".csv")
    if not os.path.exists(df_path):
        raise FileNotFoundError(f"Le fichier {df_path} n'existe pas")

    with open(df_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)

        data = []
        for row in reader:
            data.append({header: value for header, value in zip(headers, row)})

    return headers, data


def inner_join(left: list[dict[str, str]], right: list[dict[str, str]], key: str):
    """
    Fusionne deux listes de dictionnaires en fonction d'une clé commune.

    Cette fonction effectue une opération de jointure entre deux listes de dictionnaires
    (`left` et `right`) en utilisant la clé spécifiée `key`. Pour chaque dictionnaire
    dans la liste `left`, elle trouve les dictionnaires correspondants dans la liste
    `right` en fonction de la valeur de la clé `key`. Les dictionnaires fusionnés
    résultants sont retournés sous forme de dictionnaire de listes.
    Si une colonne du dictionnaire `right` entre en conflit avec une colonne du
    dictionnaire `left` (autre que la clé), la colonne en conflit du dictionnaire `right`
    est renommée en ajoutant `_y` à son nom.

    Parameters
    ----------
        left (list[dict[str, str]]): La liste gauche de dictionnaires à fusionner.
        right (list[dict[str, str]]): La liste droite de dictionnaires à fusionner.
        key (str): La clé utilisée pour faire correspondre les dictionnaires entre les
                   listes `left` et `right`.

    Return
    -------
        dict[str, list]: Un dictionnaire où chaque clé correspond à un nom de colonne,
            et les valeurs
        sont des listes contenant les données fusionnées pour cette colonne.
    """

    if not isinstance(key, str):
        raise TypeError("La clé doit être une chaîne de caractère.")

    if not (key in left[0] and key in right[0]):
        raise ValueError(f"La clé {key} n'existe pas dans les deux listes.")

    index = {}
    for right_row in right:
        key_value = right_row[key]
        if key_value not in index:
            index[key_value] = []
        index[key_value].append(right_row)

    result = []
    for left_row in left:
        key_value = left_row.get(key)
        if key_value in index:
            for right_row in index[key_value]:
                merged = left_row.copy()
                for col in right_row:
                    if col == key:
                        continue
                    if col in merged:
                        merged[col + "_y"] = right_row[col]
                    else:
                        merged[col] = right_row[col]
                result.append(merged)

    return result


def rows_to_dict(rows: list[dict[str, str]]) -> dict[str, list]:

    table = {col: [] for col in rows[0]}
    for row in rows:
        for col, val in row.items():
            table[col].append(val)

    return table


def get_python_df(dfs: list, keys: str | list) -> dict[str, list]:
    """
    Fusionne plusieurs ensembles de données CSV en un dictionnaire Python.
    Parameters
    ----------
        dfs (list): Liste des chemins de fichiers CSV ou des objets contenant les
                    données à fusionner.
        keys (str | list): Clé(s) utilisée(s) pour effectuer les jointures.
            - Si une chaîne de caractères est fournie, elle est utilisée pour une
              jointure entre deux ensembles de données.
            - Si une liste est fournie, elle doit contenir les clés pour chaque jointure
              entre les ensembles de données.
    Return
    -------
        dict[str, list]: Un dictionnaire où les clés sont les noms des colonnes et les
                         valeurs sont des listes contenant les données correspondantes.
    """

    if not isinstance(dfs, list):
        raise TypeError("Les données à fusionner doivent être contenues dans une liste")

    if not (isinstance(keys, str) or isinstance(keys, list)):
        raise TypeError("Type de clés invalides")

    if not all(isinstance(key, str) for key in keys):
        raise TypeError("Les clés doivent être des chaînes de caractère")

    if isinstance(keys, list) and len(dfs) != len(keys) + 1:
        raise ValueError("Nombre de clés invalides")

    if isinstance(keys, str) and len(dfs) > 2:
        raise ValueError("Nombre de clés invalides")

    rows = [csv_to_rows(df)[1] for df in dfs]

    row_merged = reduce(
        lambda left, right_key: inner_join(left, right_key[0], right_key[1]),
        zip(rows[1:], keys),
        rows[0],
    )

    data = rows_to_dict(row_merged)

    return data


# Barème de points FIA (valable pour la plupart des saisons modernes)
points_bareme = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
