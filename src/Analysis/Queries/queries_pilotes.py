"""Fichier avec les différentes requêtes relatives aux pilotes."""

from src.Analysis.utils import get_pd_df, get_python_df
import pandas as pd


# Barème de points FIA (valable pour la plupart des saisons modernes)
points_bareme = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}


# Nombre de courses gagnées par pilote :
def nombre_victoires_pilotes(method: str, nb_victoires: int = 30) -> pd.DataFrame:
    """
    Calcule le nombre total de victoires (positionText == '1') par pilote,
    puis filtre ceux avec au moins `nb_victoires`.

    Returns
    -------
    pd.DataFrame : Colonnes ["nom_pilote", "wins"] trié décroissant
    """
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":
        df = get_pd_df(["drivers", "results"], ["driverId"])

        df["nom_pilote"] = df["forename"] + " " + df["surname"]

        # Filtrer les victoires
        df_victoires = df[df["positionText"] == "1"]

        # Compter les victoires par pilote
        total_victoires = (
            df_victoires.groupby("nom_pilote").size().reset_index(name="wins")
        )

        # Filtrer selon seuil
        total_victoires = total_victoires[total_victoires["wins"] >= nb_victoires]

        # Tri décroissant
        total_victoires = total_victoires.sort_values(
            "wins", ascending=False
        ).reset_index(drop=True)

        return total_victoires

    else:
        # Version homemade
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
    # Fusion des données drivers + results + races
    df = get_pd_df(["drivers", "driver_standings", "races"], ["driverId", "raceId"])

    # Filtrage par saison
    df = df[df["year"] == saison].copy()

    print(df.head())

    # Créer le nom complet du pilote
    df["nom_pilote"] = df["forename"] + " " + df["surname"]

    # Garder les lignes avec position valide (entier positif)
    df = df[df["position"].apply(lambda x: isinstance(x, (int, float)) and x > 0)]
    df["position"] = df["position"].astype(int)

    # Appliquer le barème de points
    df["points"] = df["position"].apply(lambda p: points_bareme.get(p, 0))

    print(df["points"])

    # Points totaux par pilote
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


def temps_de_carriere_pilotes() -> pd.DataFrame:
    """
    Calcule le temps de carrière de chaque pilote

    Returns
    -------
    pd.DataFrame
        Contient :
        - nom_pilote
        - debut : première année de participation
        - fin : dernière année de participation
        - duree : durée de carrière en années
    """

    # Fusion des données nécessaires : standings + drivers + races
    df = get_pd_df(["driver_standings", "drivers", "races"], ["driverId", "raceId"])

    # Création du nom complet
    df["nom_pilote"] = df["forename"] + " " + df["surname"]

    # Groupe par pilote pour calculer début et fin
    carriere = (
        df.groupby("nom_pilote")["year"].agg(debut="min", fin="max").reset_index()
    )

    # Calcul de la durée de carrière (inclusif)
    carriere["duree"] = carriere["fin"] - carriere["debut"] + 1

    # Tri par durée décroissante
    carriere = carriere.sort_values("duree", ascending=False).reset_index(drop=True)

    return carriere


def statistiques_pilote(nom_pilote: str) -> pd.DataFrame:
    """
    Donne les statistiques d'un pilote :
    - nombre de courses
    - nombre de podiums (1er, 2e, 3e)
    - durée de carrière

    Parameters
    ----------
    nom_pilote : str
        Nom complet du pilote (ex: "Max Verstappen")

    Returns
    -------
    pd.DataFrame
        Une ligne avec les colonnes :
        - nom_pilote, nb_courses, nb_podiums_1, nb_podiums_2, nb_podiums_3
        - debut (année), fin (année), duree_carriere
    """

    df = get_pd_df(["drivers", "results", "races"], ["driverId", "raceId"])
    df["nom_pilote"] = df["forename"] + " " + df["surname"]

    # Filtrer le pilote choisi
    df_pilote = df[df["nom_pilote"] == nom_pilote].copy()

    if df_pilote.empty:
        raise ValueError(f"Aucune donnée trouvée pour le pilote : {nom_pilote}")

    nb_courses = len(df_pilote)
    podiums = df_pilote["position"].astype(str)

    nb_1 = (podiums == "1").sum()
    nb_2 = (podiums == "2").sum()
    nb_3 = (podiums == "3").sum()

    debut = df_pilote["year"].min()
    fin = df_pilote["year"].max()
    duree = fin - debut + 1

    stats = pd.DataFrame(
        [
            {
                "nom_pilote": nom_pilote,
                "nb_courses": nb_courses,
                "nb_podiums_1": nb_1,
                "nb_podiums_2": nb_2,
                "nb_podiums_3": nb_3,
                "debut": debut,
                "fin": fin,
                "duree_carriere": duree,
            }
        ]
    )

    return stats
