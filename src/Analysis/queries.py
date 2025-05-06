"""Fichier avec les différentes requêtes."""

from utils import get_pd_df, get_python_df
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

#nombre_victoires_pilotes('pandas', 30)




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

#classement_saison('pandas', 2023)



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





########### Nombre de victoires par écuries par an :

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





########### Nombre de victoires par écurie en relatif :

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
        
        #On effectue le calcul final :
        
        print(f"\nNombre total de victoires de l'écurie {ecurie} :")
        print(nbrWins)
        print(f"\nNombre de saison auxquelles l'écurie {ecurie} a participée :")
        print(nbrParticipation)
        print(f"\nNombre moyen de victoires de l'écurie {ecurie} par saison :")
        print((nbrWins/nbrParticipation))
        
victoiresEcuriesRelatif('pandas')




####################################################################################################
########################################    pit-stops     ##########################################
####################################################################################################


########### Quelle est l'écurie ayant la meilleure moyenne de temps au pit-stop depuis 1950 ?



def pit_stop(method: str, saison = int(input("Choisir la saison : "))) -> pd.DataFrame:
    
    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":
        
        df = get_pd_df(["pit_stops", "races", "results", "constructors"], ["raceId", "driverId", "constructorId"])
        
        # On filtre selon l'année de la saison
        df = df.drop(df[df.year != saison].index)
        
        #On supprime les valeurs abberantes 
        df = df.drop(df[df.milliseconds_x > 300000].index)
        
        # faut drop : manor ; hrt ; 
        
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
            
            "red_bull":"Red Bull",
            
            "mercedes": "Mercedes",
            
            "mclaren": "McLaren",
            
            "williams": "Williams",
            
            "ferrari": 'Ferrari',
            
            "haas": "Hass"
            }
        
        df["constructor_unifie"] = df["constructorRef"].replace(constructor_merge_dict)
        
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



########### Top 7 des meilleurs temps aux pit-stops de chaque saison :






####################################################################################################
########################################    circuits    ############################################
####################################################################################################



########## Meilleure écurie par circuit (input circuit) :






########## Performance des écuries selon le type de circuit (front ou rear limited) :
















    

        






























#print(classement_saison("pandas", 2023))

# Classement par nationalité

# Statistiques par circuit


def get_question(question_id):
    functions = {
        "q1": nombre_victoires_pilotes,
        "q2": classement_saison,
    }
    return functions.get(question_id)
