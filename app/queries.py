"""Fichier avec les différentes requêtes. """

from functions import get_query_as_df
import pandas as pd


# Nombre de courses gagnées par pilote
def nombre_victoires_pilotes(nb_victoires: int = 0) -> pd.DataFrame:
    query = "SELECT * FROM drivers INNER JOIN driver_standings USING(driverId) ;"
    df = get_query_as_df(query)
    df["nom_pilote"] = df["forename"] + " " + df["surname"]
    df = df[["nom_pilote", "wins"]].groupby("nom_pilote").sum()
    df = df.loc[df["wins"] >= nb_victoires]
    return df


# Classement des joueurs selon la saison.
def classement_saison(saison: int = 2023) -> pd.DataFrame:
    query = "SELECT * FROM drivers INNER JOIN driver_standings USING(driverId) \
             INNER JOIN races USING(raceId) ;"
    df = get_query_as_df(query)
    df = df.loc[df["year"] == saison]
    df["nom_pilote"] = df["forename"] + " " + df["surname"]
    df_points = df[["nom_pilote", "points"]].groupby("nom_pilote").sum()
    df_points = df_points.sort_values('points', ascending=False)
    # df_rank = df[["nom_pilote", "position"]].groupby('nom_pilote').value_counts()

    return df_points


df = classement_saison()
print(df)
