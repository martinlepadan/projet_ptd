"""
Requêtes pit stops
"""

from src.Analysis.utils import get_pd_df, get_python_df
import pandas as pd

# Dictionnaire de correspondance pour uniformiser les noms des écuries
constructor_merge_dict: dict[str, str] = {
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


def pit_stop(saison: int = 2020) -> pd.DataFrame:
    """
    Calcule le temps moyen de pit stop par écurie pour une saison donnée.

    Parameters
    ----------
    saison : int, optional
        Année de la saison (default: 2020).

    Returns
    -------
    pd.DataFrame
        DataFrame contenant les écuries et leur temps moyen de pit stop en secondes.
    """

    df = get_pd_df(
        ["pit_stops", "races", "results", "constructors"],
        ["raceId", "driverId", "constructorId"],
    )

    df = df[df["year"] == saison]
    df = df[df["milliseconds_x"] <= 300000]  # Filtrage valeurs aberrantes

    df["secondes"] = round(df["milliseconds_x"] / 1000, 3)
    df["constructor_unifie"] = df["constructorRef"].replace(constructor_merge_dict)
    df = df[~df["constructorRef"].isin(["hrt", "manor"])]

    df_final = (
        df.groupby("constructor_unifie")["secondes"]
        .mean()
        .reset_index()
        .rename(columns={"secondes": "pit_stop_moyen"})
        .sort_values("pit_stop_moyen")
        .reset_index(drop=True)
    )

    return df_final


def min_pit_stop(method: str) -> pd.DataFrame:
    """
    Renvoie le temps de pit stop minimal par saison.

    Parameters
    ----------
    method : str
        Méthode à utiliser : "pandas" ou "homemade".

    Returns
    -------
    pd.DataFrame
        DataFrame contenant le temps de pit stop minimal pour chaque saison.
    """
    if method not in {"pandas", "homemade"}:
        raise ValueError("La méthode doit être 'pandas' ou 'homemade'")

    if method == "pandas":
        df = get_pd_df(["pit_stops", "races"], ["raceId"])
        df = df[df["milliseconds"] <= 300000]
        df["secondes"] = round(df["milliseconds"] / 1000, 3)

        df_final = (
            df.groupby("year")["secondes"]
            .min()
            .reset_index()
            .rename(columns={"secondes": "Pit Stop Min"})
            .sort_values("year")
            .reset_index(drop=True)
        )
        return df_final

    # Version homemade (sans pandas)
    df = get_python_df(["pit_stops", "races"], ["raceId"])

    # Conversion du dict en liste de lignes
    rows = [dict(zip(df.keys(), vals)) for vals in zip(*df.values())]
    valid_rows = [r for r in rows if int(r["milliseconds"]) <= 300000]

    for row in valid_rows:
        row["secondes"] = round(int(row["milliseconds"]) / 1000, 3)

    groupes = {}
    for row in valid_rows:
        year = int(row["year"])
        groupes.setdefault(year, []).append(row["secondes"])

    result = [{"year": y, "Pit Stop Min": min(secs)} for y, secs in groupes.items()]
    result.sort(key=lambda r: r["year"])

    return pd.DataFrame(result)
