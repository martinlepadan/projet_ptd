"""Fichier avec les différentes requêtes relatives aux pit stops."""

from src.Analysis.utils import get_pd_df, get_python_df
import pandas as pd

constructor_merge_dict = {
    "force_india": "Aston Martin",
    "racing_point": "Aston Martin",
    "aston_martin": "Aston Martin",
    "minardi": "AlphaTauri",
    "toro_rosso": "AlphaTauri",
    "alphatauri": "AlphaTauri",
    "rb": "AlphaTauri",
    "benetton": "Alpine",
    "renault": "Alpine",
    "lotus_f1": "Alpine",
    "alpine": "Alpine",
    "bmw_sauber": "Alfa Romeo",
    "sauber": "Alfa Romeo",
    "alfa": "Alfa Romeo",
    "alfa_romeo": "Alfa Romeo",
    "red_bull": "Red Bull",
    "mercedes": "Mercedes",
    "mclaren": "McLaren",
    "williams": "Williams",
    "ferrari": "Ferrari",
    "haas": "Hass",
}


# Temps moyen de pit stop par écurie en 2020
def pit_stop(method: str, saison=2020) -> pd.DataFrame:

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":

        df = get_pd_df(
            ["pit_stops", "races", "results", "constructors"],
            ["raceId", "driverId", "constructorId"],
        )

        # On filtre selon l'année de la saison
        df = df.drop(df[df.year != saison].index)

        # On supprime les valeurs abberantes
        df = df.drop(df[df.milliseconds_x > 300000].index)
        df["secondes"] = round(df.milliseconds_x / 1000, 3)

        df["constructor_unifie"] = df["constructorRef"].replace(constructor_merge_dict)

        # On supprime les écuries qui n'existent plus
        df = df[~df["constructorRef"].isin(["hrt", "manor"])]

        # Calcul du temps de pit stop moyen par écurie
        df_final = (
            df.groupby("constructor_unifie")["secondes"]
            .mean()
            .reset_index()
            .rename(columns={"secondes": "pit_stop_moyen"})
            .sort_values("pit_stop_moyen")
            .reset_index(drop=True)
        )

        return df_final

    else:
        pass


def min_pit_stop(method:str) -> pd.DataFrame:
    """Renvoie le temps de pit stop minimal par saison."""

    if method not in ["pandas", "homemade"]:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":
    
        df = get_pd_df(["pit_stops", "races"], ["raceId"])

        df = df.drop(df[df.milliseconds > 300000].index)
        df["secondes"] = round(df.milliseconds / 1000, 3)
        df_final = (
            df.groupby("year")["secondes"]
            .min()
            .reset_index()
            .rename(columns={"secondes": "Pit Stop Min"})
            .sort_values("year")
            .reset_index(drop=True)
        )
        return df_final
    
    else:
        # Version homemade :
        
        df = get_python_df(["pit_stops", "races"], ["raceId"])
        
        # Conversion du dict de colonnes en liste de lignes
        rows = [dict(zip(df.keys(), vals)) for vals in zip(*df.values())]

        # Filtrer pour supprimer les valeurs aberrantes
        filtrage = [row for row in rows if int(row["milliseconds"]) <= 300000]

        # Ajouter la colonne secondes
        for row in filtrage:
            row["secondes"] = round(int(row["milliseconds"]) / 1000, 3)
        
        # GroupBy des saisons (années) et récupération des secondes
        groupes = {}
        for row in filtrage:
            year = row["year"]
            secs = row["secondes"]
            groupes.setdefault(year, []).append(secs)
        
        # Pour chaque saison on calcule le temps minimal et on prépare la liste de dict
        result_rows = [
            {"year": year, "Pit Stop Min": min(secs)}
            for year, secs in groupes.items()
        ]
        # On trie par année croissante
        result_rows.sort(key=lambda x: x["year"])
        
        # On reconstruit le dict final
        df_final = {
            "year": [r["year"] for r in result_rows],
            "Pit Stop Min": [r["Pit Stop Min"] for r in result_rows],
        }
        
        return pd.DataFrame(df_final)
        
        
