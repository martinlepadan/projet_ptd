"""Fichier avec les différentes requêtes relatives aux écuries."""

from src.Analysis.utils import get_pd_df
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


def victoiresEcuries(method: str, ecurie: str, saison: int) -> pd.DataFrame:

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":

        df = get_pd_df(
            ["constructor_standings", "constructors", "races"],
            ["constructorId", "raceId"],
        )

        df = df.loc[(df["name_x"] == ecurie) & (df["year"] == saison)]

        df = df.loc[df["position"] == 1]

        """ print(f"Nombre de victoire de l'écurie {ecurie} lors de la saison {saison} :")
        print(df.shape[0]) """

        return df.shape[0]


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

        # On effectue le calcul final et on affiche les résultats :

        print(f"\nNombre total de victoires de l'écurie {ecurie} :")
        print(nbrWins)
        print(f"\nNombre de saison auxquelles l'écurie {ecurie} a participée :")
        print(nbrParticipation)
        print(f"\nNombre moyen de victoires de l'écurie {ecurie} par saison :")
        print((nbrWins / nbrParticipation))
        
        return(nbrWins,nbrParticipation,nbrWins/nbrParticipation)
