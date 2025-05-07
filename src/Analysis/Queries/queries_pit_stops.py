"""Fichier avec les différentes requêtes relatives aux pit stops."""

from src.Analysis.utils import get_pd_df
import pandas as pd


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


pit_stop("pandas")
