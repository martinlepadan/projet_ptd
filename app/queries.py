"""Fichier avec les différentes requêtes. """

from functions import get_query_as_df
import pandas as pd


# Nombre de courses gagnées par pilote
def nombre_victoires_pilotes(method: str, nb_victoires: int = 0) -> pd.DataFrame:
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == 'pandas':
        query = "SELECT * FROM drivers INNER JOIN driver_standings USING(driverId) ;"
        df = get_query_as_df(query)
        df["nom_pilote"] = df["forename"] + " " + df["surname"]
        df = df[["nom_pilote", "wins"]].groupby("nom_pilote").sum()
        df = df.loc[df["wins"] >= nb_victoires]

    else:
        pass
    return df


# Classement des joueurs selon la saison.
def classement_saison(method: str, saison: int = 2023) -> pd.DataFrame:

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")
    # On récupère les données que l'on filtre avec la saison désirée
    query = "SELECT * FROM drivers INNER JOIN driver_standings USING(driverId) \
             INNER JOIN races USING(raceId) ;"

    if method == 'pandas':
        df = get_query_as_df(query)
        df = df.loc[df["year"] == saison]
        df["nom_pilote"] = df["forename"] + " " + df["surname"]

        # On calcule d'abord le nombre de points par pilote
        df_points = df[["nom_pilote", "points"]].groupby("nom_pilote").sum()

        # Puis le nombre de fois qu'un pilote est arrivé à chaque place
        df_rank = df.groupby(["nom_pilote", "positionText"]).size().unstack(fill_value=0)
        sorted_columns = sorted([col for col in df_rank.columns], key=lambda x: int(x))
        df_rank = df_rank[sorted_columns]  # On trie les colonnes

        # On peut enfin fusionner les deux tableaux
        df_final = df_points.merge(df_rank, on="nom_pilote", how="left").fillna(0)

        # Puis trier les pilotes par points puis par le nombre de fois qu'ils
        # sont arrivés 1er, 2eme, etc..
        df_final = df_final.sort_values(
            ["points"] + sorted_columns, ascending=[False] * (len(sorted_columns) + 1)
        )

        # On calcule enfin le nombre de points moyen par course
        df_final["pts_par_course"] = df_final["points"] / df_final.drop(
            "points", axis=1
        ).sum(axis=1)

    else:
        pass

    return df_final


# Temps de pit-stop par écurie

# Classement par écurie par année et depuis 1950

# Classement par nationalité

# Statistiques par circuit
