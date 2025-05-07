"""Fichier avec les différentes requêtes relatives aux écuries."""

from src.Analysis.utils import get_pd_df, get_python_df
import pandas as pd


def ecuriesPoints(method: str, saison: int) -> pd.DataFrame:

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    # Barème de points FIA (valable pour la plupart des saisons modernes)
    points_bareme = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

    if method == "pandas":

        # On exécute la requête pour créer le dataframe
        df = get_pd_df(
            ["results", "races", "constructors"], ["raceId", "constructorId"]
        )

        # On trie selon l'année
        df = df.loc[df["year"] == saison]

        # On crée une colonne points en attribuant les bons points
        df["points"] = df["positionOrder"].apply(lambda pos: points_bareme.get(pos, 0))

        # On regroupe les points par écurie
        classement = (
            df.groupby("constructorRef")["points"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        return classement


# Nombre de victoires par écuries :


def victoires_ecuries_saison(ecuries: list[str], saisons: list[int]) -> pd.DataFrame:
    """
    Calcule le nombre de victoires d'une ou plusieurs écuries pour chaque saison donnée.

    Parameters
    ----------
    method : str
        "pandas" ou "homemade"
    ecuries : list[str]
        Liste des noms d'écuries à inclure
    saisons : list[int]
        Liste de début et de fin de saison

    Returns
    -------
    pd.DataFrame
        Colonnes : ["ecurie", "saison", "victoires"]
    """

    if not isinstance(ecuries, list) or not all(isinstance(e, str) for e in ecuries):
        raise ValueError("ecuries doit être une liste de chaînes de caractères")

    df = get_pd_df(
        ["constructor_standings", "constructors", "races"],
        ["constructorId", "raceId"],
    )

    # Filtrer selon la saison et les écuries
    df = df[
        (df["year"] >= saisons[0])
        & (df["year"] <= saisons[1])
        & (df["name_x"].isin(ecuries))
        & (df["position"] == 1)
    ]

    # Compter les victoires par écurie et saison
    grouped = (
        df.groupby(["name_x", "year"])
        .size()
        .reset_index(name="victoires")
        .rename(columns={"name_x": "ecurie", "year": "saison"})
        .sort_values(["ecurie", "saison"])
        .reset_index(drop=True)
    )

    return grouped


# Nombre de victoires par écurie en absolue + en relatif + nbr de saisons participées :


def victoiresEcuriesRelatif(method: str, ecurie: str) -> pd.DataFrame:

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":

        # On créé le dataframe correspondant au nombre de victoires totale de l'écurie :

        df = get_pd_df(
            ["constructor_standings", "constructors", "races"],
            ["constructorId", "raceId"],
        )

        df = df.loc[df["name_x"] == ecurie]

        df = df.loc[df["position"] == 1]

        nbrWins = df.shape[0]

        # On créé un second dataframe pour calculer le nombre d'années de participation
        # de l'écurie (pour pouvoir calculer le relatif ensuite)

        df2 = get_pd_df(
            ["constructor_standings", "constructors", "races"],
            ["constructorId", "raceId"],
        )

        df2 = df2.loc[df2["name_x"] == ecurie]

        nbrParticipation = len(pd.unique(df2["year"]))

        if nbrParticipation == 0:
            moyenne = "Données manquantes"
        else:
            moyenne = round(nbrWins / nbrParticipation, 2)

        return (nbrWins, nbrParticipation, moyenne)

    else:
        # Dataframe 1 (nombre total de victoires) :
        df = get_python_df(
            ["constructor_standings", "constructors", "races"],
            ["constructorId", "raceId"],
        )

        # On transforme le dict de colonnes en liste de lignes
        rows = [dict(zip(df.keys(), values)) for values in zip(*df.values())]

        # Filtrage des lignes par écurie et position = 1
        rows = [row for row in rows if row["name"] == ecurie]
        rows = [row for row in rows if row["position"] == "1"]

        nbrWins = len(rows)

        # Dataframe 2 (nombre total de participation à une saison) :
        df2 = get_python_df(
            ["constructor_standings", "constructors", "races"],
            ["constructorId", "raceId"],
        )
        rows2 = [dict(zip(df2.keys(), values)) for values in zip(*df2.values())]

        rows2 = [row for row in rows2 if row["name"] == ecurie]

        nbrParticipation = len(set(row["year"] for row in rows2))

        if nbrParticipation == 0:
            moyenne = "Données manquantes"
        else:
            moyenne = round(nbrWins / nbrParticipation, 2)

        return (nbrWins, nbrParticipation, moyenne)
