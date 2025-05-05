"""Fichier avec les différentes requêtes."""

from utils import get_pd_df, get_python_df
import pandas as pd


# Barème de points FIA (valable pour la plupart des saisons modernes)
points_bareme = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}


# Nombre de courses gagnées par pilote :
def nombre_victoires_pilotes(method: str, nb_victoires: int = 30) -> pd.DataFrame:
    """
    Calcule le nombre total de victoires par pilote sur l'ensemble de sa carrière,
    puis filtre les pilotes ayant remporté au moins `nb_victoires`.

    Parameters
    ----------
    method : str
        Méthode de traitement à utiliser : "pandas" ou "homemade" (Python pur)
    nb_victoires : int
        Seuil minimum de victoires pour qu'un pilote soit inclus dans le résultat

    Returns
    -------
    pd.DataFrame : Un tableau avec les colonnes ["nom_pilote", "wins"],
                   trié par victoires décroissantes
    """

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":
        df = get_pd_df(["drivers", "driver_standings"], ["driverId"])
        df["nom_pilote"] = df["forename"] + " " + df["surname"]

        total_victoires = df.groupby("nom_pilote")["wins"].sum().reset_index()
        total_victoires = total_victoires[total_victoires["wins"] >= nb_victoires]
        total_victoires = total_victoires.sort_values(
            "wins", ascending=False
        ).reset_index(drop=True)

        return total_victoires

    else:
        df = get_python_df(["drivers", "driver_standings"], ["driverId"])

        noms = [f"{prenom} {nom}" for prenom, nom in zip(df["forename"], df["surname"])]
        wins = [int(w) if w.isdigit() else 0 for w in df["wins"]]

        total_victoires = {}
        for nom, nb in zip(noms, wins):
            total_victoires[nom] = total_victoires.get(nom, 0) + nb

        filtered = {n: v for n, v in total_victoires.items() if v >= nb_victoires}
        sorted_list = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))

        return pd.DataFrame(sorted_list, columns=["nom_pilote", "wins"])


nombre_victoires_pilotes("pandas", 30)


def classement_saison(saison: int = 2023) -> pd.DataFrame:
    """
    Retourne le classement des pilotes pour une saison donnée, en triant selon :
    - le nombre total de points,
    - le nombre de premières places, deuxièmes, etc. (pour départager les ex aequo).

    Parameters
    ----------
    saison : int
        Année de la saison à analyser (ex : 2023)

    Returns
    -------
    pd.DataFrame
        Un tableau trié avec les colonnes :
        - nom_pilote
        - points
        - position 1, 2, 3, ... (selon les arrivées)
        - pts_par_course : ratio points / total de courses
    """

    # Chargement et fusion des données
    df = get_pd_df(["drivers", "driver_standings", "races"], ["driverId", "raceId"])

    # Filtrage par saison
    df = df[df["year"] == saison].copy()
    df["nom_pilote"] = df["forename"] + " " + df["surname"]

    # Total de points par pilote
    df_points = df.groupby("nom_pilote")[["points"]].sum()

    # Comptage des positions (1er, 2e, etc.)
    df_valid_positions = df[df["positionText"].str.isdigit()]
    df_rank = (
        df_valid_positions.groupby(["nom_pilote", "positionText"])
        .size()
        .unstack(fill_value=0)
    )

    # Tri des colonnes de positions (1, 2, 3, ...)
    sorted_columns = sorted(df_rank.columns, key=lambda x: int(x))
    df_rank = df_rank[sorted_columns]

    # Fusion des points et classements
    df_final = df_points.merge(df_rank, on="nom_pilote", how="left").fillna(0)

    # Tri global : points décroissants, puis par positions (plus de 1ères places, etc.)
    df_final = df_final.sort_values(
        ["points"] + sorted_columns, ascending=[False] * (1 + len(sorted_columns))
    )

    # Calcul du ratio points / courses
    total_courses = df_final.drop(columns=["points"]).sum(axis=1)
    df_final["pts_par_course"] = df_final["points"] / total_courses

    df_final = df_final.reset_index()

    return df_final


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


# ÉCURIES

# Classement des écuries par année (avec nombre de points) :

def ecuriesPoints(method: str, saison=2023) -> pd.DataFrame:

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":

        # On exécute la requête SQL pour créer le dataframe
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

        # On affiche le classement final
        print(f"\nClassement des écuries pour la saison {saison} :")
        print(classement)


# ecuriesPoints('pandas')


# Nombre de victoires par écuries :


def victoiresEcuries(method: str) -> pd.DataFrame:

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":

        # On exécute la requête SQL pour créer le dataframe
        df = get_pd_df(
            ["results", "races", "constructors"], ["raceId", "constructorId"]
        )

        return df


# victoiresEcuries('pandas')


# Nombre de victoires par écurie en relatif :

# PITS-STOPS

# Quelle est l'écurie ayant la meilleure moyenne de temps au pit-stop depuis 1950 ?


# Temps de pit stop par écurie
def pit_stop(method: str, saison: int = 2023) -> pd.DataFrame:
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":
        df = get_pd_df(
            ["pit_stops", "results", "constructors"], ["driverId", "constructorId"]
        )

        # On supprime les lignes sans données valides de pit stop
        df = df.dropna(subset=["milliseconds_x"])

        # Calcul du temps de pit stop moyen par écurie
        df_final = (
            df.groupby("name")["milliseconds_x"]
            .mean()
            .reset_index()
            .rename(columns={"milliseconds_x": "pit_stop_moyen"})
            .sort_values("pit_stop_moyen")
            .reset_index(drop=True)
        )

        return df_final

    else:
        pass


print(pit_stop("pandas", 2023))
# Top 7 des meilleurs temps aux pit-stops de chaque saison :

# CIRCUITS

# Meilleure écurie par circuit (input circuit) :


# Performance des écuries selon le type de circuit (front ou rear limited) :


# Temps de pit-stop par écurie
# Temps de pit-stop par écurie


# Classement par nationalité

# Statistiques par circuit
