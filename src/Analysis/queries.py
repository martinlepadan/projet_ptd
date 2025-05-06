"""Fichier avec les différentes requêtes."""

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
    df_rank = (
        df.groupby(["nom_pilote", "position"])
        .size()
        .unstack(fill_value=0)
    )

    # Tri des colonnes de position
    sorted_columns = sorted(df_rank.columns)
    df_rank = df_rank[sorted_columns]

    # Fusion des points et positions
    df_final = df_points.merge(df_rank, on="nom_pilote").fillna(0)

    # Tri : points décroissants, puis nombre de positions
    df_final = df_final.sort_values(
        ["points"] + sorted_columns,
        ascending=[False] * (1 + len(sorted_columns))
    )

    # Ratio points / nombre total de courses disputées
    total_courses = df_rank.sum(axis=1)
    df_final["pts_par_course"] = df_final["points"] / total_courses

    # Renommer colonnes pour le graphique (en str : "1", "2", ...)
    df_final.rename(columns={pos: str(pos) for pos in sorted_columns}, inplace=True)

    return df_final.reset_index()


print(classement_saison(2023))


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


def ecuriesPoints(method: str, saison = int(input("Choisir l'année de la saison : "))) -> pd.DataFrame:
    
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")
    
    # Barème de points FIA (valable pour la plupart des saisons modernes)
    points_bareme = {
        1: 25,
        2: 18,
        3: 15,
        4: 12,
        5: 10,
        6: 8,
        7: 6,
        8: 4,
        9: 2,
        10: 1
    }

    if method == 'pandas':
        
        # On exécute la requête pour créer le dataframe
        df = get_pd_df(["results", "races", "constructors"], ["raceId", "constructorId"])
        
        # On trie selon l'année
        df = df.loc[df["year"] == saison]
        
        # On crée une colonne points en attribuant les bons points
        df["points"] = df["positionOrder"].apply(lambda pos: points_bareme.get(pos, 0))
        
        # On regroupe les points par écurie
        classement = df.groupby("constructorRef")["points"].sum().sort_values(ascending=False).reset_index()

        # On affiche le classement final
        print(f"\nClassement des écuries pour la saison {saison} :")
        print(classement)
        
ecuriesPoints('pandas')

# Nombre de victoires par écuries :

def victoiresEcuries(method: str, ecurie = str(input("Choisir l'écurie : ")), saison = int(input("Choisir l'année : ")))  -> pd.DataFrame:
    
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")
            
    if method == 'pandas':

        df = get_pd_df(["constructor_standings", "constructors", "races"], ["constructorId", "raceId"])

        df = df.loc[(df["name_x"] == ecurie) & (df["year"] == saison)]

        df = df.loc[df["position"] == 1]
        
        print(f"Nombre de victoire de l'écurie {ecurie} lors de la saison {saison} :")
        print(df.shape[0])

victoiresEcuries('pandas')

# Nombre de victoires par écurie en absolue + en relatif + nbr de saisons participées :

def victoiresEcuriesRelatif(method: str, ecurie = str(input("Choisir l'écurie : ")))  -> pd.DataFrame:
    
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")
            
    if method == 'pandas':
        
        # On créé le dataframe correspondant au nombre de victoires totale de l'écurie :
        
        df = get_pd_df(["constructor_standings", "constructors", "races"], ["constructorId", "raceId"])

        df = df.loc[df["name_x"] == ecurie]

        df = df.loc[df["position"] == 1]
        
        nbrWins = df.shape[0]
        
        #On créé un second dataframe pour calculer le nombre d'années de participation de l'écurie (pour pouvoir calculer le relatif ensuite)
        
        df2 = get_pd_df(["constructor_standings", "constructors", "races"], ["constructorId", "raceId"])
        
        df2 = df2.loc[df2["name_x"] == ecurie]
        
        nbrParticipation = len(pd.unique(df2["year"]))
        
        #On effectue le calcul final et on affiche les résultats :
        
        print(f"\nNombre total de victoires de l'écurie {ecurie} :")
        print(nbrWins)
        print(f"\nNombre de saison auxquelles l'écurie {ecurie} a participée :")
        print(nbrParticipation)
        print(f"\nNombre moyen de victoires de l'écurie {ecurie} par saison :")
        print((nbrWins/nbrParticipation))
        
victoiresEcuriesRelatif('pandas')

# PITS-STOPS

# Quelle est l'écurie ayant la meilleure moyenne de temps au pit-stop depuis 1950 ?


# Temps de pit stop par écurie en 2020
def pit_stop(method: str, saison = 2020) -> pd.DataFrame:
    
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":
        
        df = get_pd_df(["pit_stops", "races", "results", "constructors"], ["raceId", "driverId", "constructorId"])
        
        # On filtre selon l'année de la saison
        df = df.drop(df[df.year != saison].index)
        
        #On supprime les valeurs abberantes 
        df = df.drop(df[df.milliseconds_x > 300000].index)
        
        constructor_merge_dict = {
            "force_india": "Aston Martin", # ex-Force India → Racing Point → Aston Martin
            "racing_point": "Aston Martin",
            "aston_martin": "Aston Martin",
            
            "minardi": "AlphaTauri", # ex-Minardi → Toro Rosso → AlphaTauri
            "toro_rosso": "AlphaTauri",  
            "alphatauri": "AlphaTauri",
            "rb": "AlphaTauri",
            
            "benetton": "Alpine", # ex-Toleman → Benetton → Renault → Lotus → Renault → Alpine
            "renault": "Alpine",
            "lotus_f1": "Alpine",
            "alpine": "Alpine",
            
            "bmw_sauber": "Alfa Romeo", # ex-BMW Sauber → Sauber → Alfa → Alfa Romeo
            "sauber": "Alfa Romeo",
            "alfa": "Alfa Romeo",
            "alfa_romeo": "Alfa Romeo",
            
            "red_bull":"Red Bull", # On renomme proprement
            
            "mercedes": "Mercedes",
            
            "mclaren": "McLaren",
            
            "williams": "Williams",
            
            "ferrari": 'Ferrari',
            
            "haas": "Hass"
            }
        
        df["constructor_unifie"] = df["constructorRef"].replace(constructor_merge_dict)
        
        #On supprime les écuries qui n'existent plus
        df = df[~df["constructorRef"].isin(["hrt", "manor"])]
    
        # Calcul du temps de pit stop moyen par écurie
        df_final = (
            df.groupby("constructor_unifie")["milliseconds_x"]
            .mean()
            .reset_index()
            .rename(columns={"milliseconds_x": "pit_stop_moyen"})
            .sort_values("pit_stop_moyen")
            .reset_index(drop=True)
        )

        print(df_final)

pit_stop('pandas')

# CIRCUITS

# Meilleure écurie par circuit (input circuit) :


# Performance des écuries selon le type de circuit (front ou rear limited) :

# Classement par nationalité

# Statistiques par circuit
