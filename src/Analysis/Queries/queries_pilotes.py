"""
Requêtes relatives aux statistiques des pilotes de F1.
"""

from src.Analysis.utils import get_pd_df, get_python_df, points_bareme
import pandas as pd


def nombre_victoires_pilotes(method: str, nb_victoires: int = 30) -> pd.DataFrame:
    """
    Calcule le nombre total de victoires (positionText == '1') par pilote.

    Parameters
    ----------
    method : str
        "pandas" ou "homemade"
    nb_victoires : int
        Nombre minimum de victoires pour apparaître dans le tableau.

    Returns
    -------
    pd.DataFrame
        Colonnes ["nom_pilote", "wins"], trié par nombre de victoires décroissant.
    """
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":
        df = get_pd_df(["drivers", "results"], ["driverId"])
        df["nom_pilote"] = df["forename"] + " " + df["surname"]
        df_victoires = df[df["positionText"] == "1"]
        total_victoires = (
            df_victoires.groupby("nom_pilote").size().reset_index(name="wins")
        )
        total_victoires = total_victoires[total_victoires["wins"] >= nb_victoires]
        return total_victoires.sort_values("wins", ascending=False).reset_index(
            drop=True
        )

    else:
        df = get_python_df(["drivers", "results"], ["driverId"])
        noms = [f"{prenom} {nom}" for prenom, nom in zip(df["forename"], df["surname"])]
        positions = df["positionText"]

        total_victoires = {}
        for nom, pos in zip(noms, positions):
            if pos == "1":
                total_victoires[nom] = total_victoires.get(nom, 0) + 1

        filtered = {n: v for n, v in total_victoires.items() if v >= nb_victoires}
        sorted_list = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))
        return pd.DataFrame(sorted_list, columns=["nom_pilote", "wins"])


def classement_saison(saison: int = 2023) -> pd.DataFrame:
    """
    Retourne le classement des pilotes pour une saison donnée, en calculant les points
    via le barème FIA à partir de la colonne 'position' (entier).

    Returns
    -------
    pd.DataFrame
        Contient :
        - nom_pilote
        - points
        - colonnes "1", "2", "3", ... : nombre de positions obtenues
        - pts_par_course : ratio points / total de participations
    """

    df = get_pd_df(["drivers", "driver_standings", "races"], ["driverId", "raceId"])
    df = df[df["year"] == saison]
    df["nom_pilote"] = df["forename"] + " " + df["surname"]

    # Garder les lignes avec position valide (entier positif)
    df = df[df["position"].apply(lambda x: isinstance(x, (int, float)) and x > 0)]
    df["position"] = df["position"].astype(int)

    # Appliquer le barème de points
    df["points"] = df["position"].apply(lambda p: points_bareme.get(p, 0))
    df_points = df.groupby("nom_pilote")["points"].sum().to_frame()

    # Comptage des positions 1, 2, 3, etc.
    df_rank = df.groupby(["nom_pilote", "position"]).size().unstack(fill_value=0)

    # Tri des colonnes de position
    sorted_columns = sorted(df_rank.columns)
    df_rank = df_rank[sorted_columns]

    # Fusion des points et positions
    df_final = df_points.merge(df_rank, on="nom_pilote").fillna(0)

    # Tri : points décroissants, puis nombre de positions
    df_final = df_final.sort_values(
        ["points"] + sorted_columns, ascending=[False] * (1 + len(sorted_columns))
    )

    # Ratio points / nombre total de courses disputées
    total_courses = df_rank.sum(axis=1)
    df_final["pts_par_course"] = df_final["points"] / total_courses

    # Renommer colonnes pour le graphique (en str : "1", "2", ...)
    df_final.rename(columns={pos: str(pos) for pos in sorted_columns}, inplace=True)

    return df_final.reset_index()


def temps_de_carriere_pilotes(duree_min: int = 5) -> pd.DataFrame:
    """
    Calcule la durée de carrière des pilotes à partir de leur première
    et dernière saison.

    Parameters
    ----------
    duree_min : int
        Nombre d'années minimum de carrière.

    Returns
    -------
    pd.DataFrame
        Colonnes : nom_pilote, debut, fin, duree
    """
    df = get_pd_df(["driver_standings", "drivers", "races"], ["driverId", "raceId"])
    df["nom_pilote"] = df["forename"] + " " + df["surname"]

    carriere = (
        df.groupby("nom_pilote")["year"].agg(debut="min", fin="max").reset_index()
    )
    carriere["duree"] = carriere["fin"] - carriere["debut"] + 1

    return (
        carriere[carriere["duree"] >= duree_min]
        .sort_values("duree", ascending=False)
        .reset_index(drop=True)
    )


def statistiques_pilote(nom_pilote: str) -> pd.DataFrame:
    """
    Donne un résumé des performances d'un pilote.

    Parameters
    ----------
    nom_pilote : str
        Nom complet du pilote (ex : "Lewis Hamilton").

    Returns
    -------
    pd.DataFrame
        Une ligne avec : nb_courses, nb_podiums_1, nb_podiums_2, nb_podiums_3,
        debut, fin, duree_carriere
    """
    df = get_pd_df(["drivers", "results", "races"], ["driverId", "raceId"])
    df["nom_pilote"] = df["forename"] + " " + df["surname"]

    df_pilote = df[df["nom_pilote"] == nom_pilote].copy()

    if df_pilote.empty:
        raise ValueError(f"Aucune donnée trouvée pour le pilote : {nom_pilote}")

    nb_courses = len(df_pilote)
    podiums = df_pilote["position"].astype(str)

    stats = {
        "nom_pilote": nom_pilote,
        "nb_courses": nb_courses,
        "nb_podiums_1": (podiums == "1").sum(),
        "nb_podiums_2": (podiums == "2").sum(),
        "nb_podiums_3": (podiums == "3").sum(),
        "debut": df_pilote["year"].min(),
        "fin": df_pilote["year"].max(),
    }
    stats["duree_carriere"] = stats["fin"] - stats["debut"] + 1

    return pd.DataFrame([stats])
