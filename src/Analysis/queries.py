"""Fichier avec les différentes requêtes."""

from Analysis.utils import get_pd_df, get_python_df
import pandas as pd


####################################################################################################
####################################    Questions imposées     #####################################
####################################################################################################



########## Nombre de courses gagnées par pilote :


def nombre_victoires_pilotes(method: str, nb_victoires: int = 0) -> pd.DataFrame:
    if method not in ["pandas", "homemade"]:

        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":
        df = get_pd_df(["drivers", "driver_standings"], ["driverId"])

        df["nom_pilote"] = df["forename"] + " " + df["surname"]
        df = df[["nom_pilote", "wins"]].groupby("nom_pilote").sum()
        df = df.loc[df["wins"] >= nb_victoires]
        df = df.sort_values("wins", ascending=False)
        df = df.reset_index()

    else:
        df = get_python_df(["drivers", "driver_standings"], ["driverId"])
        df["nom_pilote"] = df["forename"] + " " + df["surname"]

    return df

nombre_victoires_pilotes('pandas', 30)




########## Classement des pilotes selon la saison :


def classement_saison(method: str, saison: int = 2023) -> pd.DataFrame:

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")
    # On récupère les données que l'on filtre avec la saison désirée
    if method == "pandas":
        df = get_pd_df(["drivers", "driver_standings", "races"], ["driverId", "raceId"])
        print(df.columns)
        df = df.loc[df["year"] == saison]
        df["nom_pilote"] = df["forename"] + " " + df["surname"]

        # On calcule d'abord le nombre de points par pilote
        df_points = df[["nom_pilote", "points"]].groupby("nom_pilote").sum()

        # Puis le nombre de fois qu'un pilote est arrivé à chaque place
        df_rank = (
            df.groupby(["nom_pilote", "positionText"]).size().unstack(fill_value=0)
        )
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

classement_saison('pandas', 2023)



####################################################################################################
########################################    pilotes     ############################################
####################################################################################################



########## Temps de carrière de chaque pilote :






########## Liste des pilotes actifs chaque année :







########## Classement des pilotes en fonction du taux victoire/courses participée :


















####################################################################################################
########################################    écuries     ############################################
####################################################################################################


########### Classement des écuries par année (avec nombre de points) :

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
    
    # Requête SQL :
    query = "SELECT * FROM results INNER JOIN races USING(raceId) \
            LEFT JOIN constructors USING(constructorId) ;"
    
    if method == 'pandas':
        
        # On exécute la requête SQL pour créer le dataframe
        df = get_query_as_df(query)
        
        # On trie selon l'année
        df = df.loc[df["year"] == saison]
        
        # On crée une colonne points en attribuant les bons points
        df["points"] = df["positionOrder"].apply(lambda pos: points_bareme.get(pos, 0))
        
        # On regroupe les points par écurie
        classement = df.groupby("constructorRef")["points"].sum().sort_values(ascending=False).reset_index()

        # On affiche le classement final
        print(f"\nClassement des écuries pour la saison {saison} :")
        print(classement)
        
#ecuriesPoints('pandas')




########### Nombre de victoires par écuries :

def victoiresEcuries(method: str) -> pd.DataFrame:
    
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")
    
    # Requête SQL
    query = "SELECT * FROM results INNER JOIN races USING(raceId) \
            LEFT JOIN constructors USING(constructorId) ;"
            
    if method == 'pandas':
        
        # On exécute la requête SQL pour créer le dataframe
        df = get_query_as_df(query)
        
        
        
#victoiresEcuries('pandas')



########### Nombre de victoires par écurie en relatif :






####################################################################################################
########################################    pit-stops     ##########################################
####################################################################################################


########### Quelle est l'écurie ayant la meilleure moyenne de temps au pit-stop depuis 1950 ?






########### Top 7 des meilleurs temps aux pit-stops de chaque saison :






####################################################################################################
########################################    circuits    ############################################
####################################################################################################



########## Meilleure écurie par circuit (input circuit) :






########## Performance des écuries selon le type de circuit (front ou rear limited) :
















    

        









# Temps de pit-stop par écurie
# Temps de pit-stop par écurie
def pit_stop(method: str, saison: int = 2023) -> pd.DataFrame:

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")
    # On récupère les données que l'on filtre avec la saison désirée
    query = "SELECT duration, name , constructorId FROM pit_stops \
             LEFT JOIN results USING(driverId) LEFT JOIN  \
             constructors USING(constructorId) ;"

    if method == "pandas":
        df = get_python_df(query)

        # On trie d'abord le temps de pit-stop par écurie
        df_temps = df[["name", "duration"]].groupby("name").sum()

        # On trie selon les meilleurs temps de pit-stop
        df_final = df_temps.sort_values(["duration"])

        # On calcule le temps de pit stop moyen par écurie
        df_final["tmps_pit_stop_moyen"] = df_temps["duration"] / df_final.drop(
            "duration", axis=1
        ).sum(axis=1)

    else:
        pass

    return df_final


print(classement_saison("pandas", 2023))

# Classement par nationalité

# Statistiques par circuit


def get_question(question_id):
    functions = {
        "q1": nombre_victoires_pilotes,
        "q2": classement_saison,
    }
    return functions.get(question_id)
