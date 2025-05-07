"""
Fichier pour créer le graphe de la question sur les pit-stops
"""

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def plot_temps_pit_stop(data, methode: str):
    """
    Affiche un graphique des temps moyens de pit-stop par écurie.

    Parameters
    ----------
    data : pd.DataFrame
        Doit contenir les colonnes ["constructor_unifie", "pit_stop_moyen"].
    methode : str
        "plotly" ou "matplotlib".

    Returns
    -------
    fig : Figure Plotly ou Matplotlib
    """
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    data_sorted = data.sort_values("pit_stop_moyen", ascending=True)

    if methode == "plotly":
        fig = px.bar(
            data_sorted,
            x="constructor_unifie",
            y="pit_stop_moyen",
            range_y=[
                min(data_sorted["pit_stop_moyen"]) - 0.1,
                max(data_sorted["pit_stop_moyen"]) + 0.1,
            ],
            title="Temps moyen de pit-stop par écurie",
            labels={
                "pit_stop_moyen": "Temps pit-stop (secondes)",
                "constructor_unifie": "Écurie",
            },
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig

    elif methode == "matplotlib":
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(
            data_sorted["constructor_unifie"],
            data_sorted["pit_stop_moyen"],
            color="#1f77b4",
        )
        ax.set_title("Temps moyen de pit-stop par écurie")
        ax.set_xlabel("Écurie")
        ax.set_ylabel("Temps pit-stop (secondes)")
        ax.set_ylim(
            [
                min(data_sorted["pit_stop_moyen"]) - 0.1,
                max(data_sorted["pit_stop_moyen"]) + 0.1,
            ]
        )
        ax.set_xticks(range(len(data_sorted)))
        ax.set_xticklabels(data_sorted["constructor_unifie"], rotation=45, ha="right")
        plt.tight_layout()
        return fig

    else:
        raise ValueError("La méthode doit être 'plotly' ou 'matplotlib'")


def plot_min_pit_stop(data, methode: str):
    """
    Affiche un graphique du pit-stop le plus rapide par saison.

    Parameters
    ----------
    data : pd.DataFrame
        Doit contenir les colonnes ["year", "Pit Stop Min"].
    methode : str
        "plotly" ou "matplotlib".

    Returns
    -------
    fig : Figure Plotly ou Matplotlib
    """
    data_sorted = data.sort_values("Pit Stop Min", ascending=True)

    if methode == "plotly":
        fig = px.bar(
            data_sorted,
            x="year",
            y="Pit Stop Min",
            range_y=[
                min(data_sorted["Pit Stop Min"]) - 0.2,
                max(data_sorted["Pit Stop Min"]) + 0.2,
            ],
            title="Temps minimal de pit-stop par saison",
            labels={"Pit Stop Min": "Temps pit-stop (secondes)", "year": "Année"},
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig

    elif methode == "matplotlib":
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(data_sorted["year"], data_sorted["Pit Stop Min"], color="#ff7f0e")
        ax.set_title("Temps minimal de pit-stop par saison")
        ax.set_xlabel("Année")
        ax.set_ylabel("Temps pit-stop (secondes)")
        ax.set_ylim(
            [
                min(data_sorted["Pit Stop Min"]) - 0.2,
                max(data_sorted["Pit Stop Min"]) + 0.2,
            ]
        )
        plt.tight_layout()
        return fig

    else:
        raise ValueError("La méthode doit être 'plotly' ou 'matplotlib'")
