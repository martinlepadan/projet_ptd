"""
Requêtes relatives aux statistiques des écuries de F1.
"""

import pandas as pd
from src.Analysis.utils import get_pd_df, get_python_df, points_bareme


def ecuries_points(saison: int) -> pd.DataFrame:
    """
    Calcule le total de points obtenus par chaque écurie pour une saison donnée.

    Parameters
    ----------
    saison : int
        Année de la saison.

    Returns
    -------
    pd.DataFrame
        Colonnes : ["constructorRef", "points"] triées par points décroissants.
    """
    df = get_pd_df(["results", "races", "constructors"], ["raceId", "constructorId"])
    df = df[df["year"] == saison].copy()
    df["points"] = df["positionOrder"].apply(lambda pos: points_bareme.get(pos, 0))

    classement = (
        df.groupby("constructorRef")["points"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return classement


def victoires_ecuries_saison(ecuries: list[str], saisons: tuple[int]) -> pd.DataFrame:
    """
    Calcule le nombre de victoires par écurie pour chaque saison d'une plage donnée.

    Parameters
    ----------
    ecuries : list[str]
        Liste des noms d'écuries à analyser.
    saisons : list[int]
        Période d'étude [année_début, année_fin].

    Returns
    -------
    pd.DataFrame
        Colonnes : ["ecurie", "saison", "victoires"] triées.
    """
    if not isinstance(ecuries, list) or not all(isinstance(e, str) for e in ecuries):
        raise TypeError("ecuries doit être une liste de chaînes de caractères.")

    if not isinstance(saisons, tuple) or len(saisons) != 2:
        raise ValueError("saisons doit être un tuple (début, fin).")

    df = get_pd_df(
        ["constructor_standings", "constructors", "races"], ["constructorId", "raceId"]
    )

    df = df[
        (df["year"] >= saisons[0])
        & (df["year"] <= saisons[1])
        & (df["name_x"].isin(ecuries))
        & (df["position"] == 1)
    ]

    grouped = (
        df.groupby(["name_x", "year"])
        .size()
        .reset_index(name="victoires")
        .rename(columns={"name_x": "ecurie", "year": "saison"})
        .sort_values(["ecurie", "saison"])
        .reset_index(drop=True)
    )

    return grouped


def victoires_ecurie_relatif(method: str, ecurie: str) -> tuple[int, int, float | str]:
    """
    Calcule le nombre de victoires d'une écurie, le nombre de saisons participées
    et la moyenne de victoires par saison.

    Parameters
    ----------
    method : str
        "pandas" ou "homemade"
    ecurie : str
        Nom exact de l'écurie à analyser.

    Returns
    -------
    tuple
        (nombre de victoires, nombre de saisons, moyenne par saison)
    """
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'.")

    if method == "pandas":
        df = get_pd_df(
            ["constructor_standings", "constructors", "races"],
            ["constructorId", "raceId"],
        )
        df_filtered = df[df["name_x"] == ecurie]

        nbr_wins = df_filtered[df_filtered["position"] == 1].shape[0]
        nbr_seasons = df_filtered["year"].nunique()
        moyenne = (
            round(nbr_wins / nbr_seasons, 2) if nbr_seasons else "Données manquantes"
        )

        return nbr_wins, nbr_seasons, moyenne

    else:  # homemade
        df = get_python_df(
            ["constructor_standings", "constructors", "races"],
            ["constructorId", "raceId"],
        )
        rows = [dict(zip(df.keys(), values)) for values in zip(*df.values())]
        wins = [row for row in rows if row["name"] == ecurie and row["position"] == "1"]
        seasons = {row["year"] for row in rows if row["name"] == ecurie}

        nbr_wins = len(wins)
        nbr_seasons = len(seasons)
        moyenne = (
            round(nbr_wins / nbr_seasons, 2) if nbr_seasons else "Données manquantes"
        )

        return nbr_wins, nbr_seasons, moyenne
