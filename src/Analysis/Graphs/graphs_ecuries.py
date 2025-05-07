"""Fichier pour créer les graphes pour chaque question concernant les écuries"""

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def plot_classement_saison_ecuries(data: pd.DataFrame, methode: str):
    """
    Affiche un graphique représentant le classement des écuries
    triées par nombre de points décroissants.

    Parameters
    ----------
    data : pd.DataFrame
        Doit contenir au moins les colonnes ["constructorRef", "points"]
    methode : str
        "plotly" ou "matplotlib"

    Returns
    -------
    fig : Figure Plotly ou Matplotlib
    """
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    data_sorted = data.sort_values("points", ascending=True)

    if methode == "plotly":
        fig = px.bar(
            data_sorted,
            x="points",
            y="constructorRef",
            orientation="h",
            title="Classement des écuries",
            labels={"constructorRef": "Écurie", "points": "Points"},
            text_auto=True,
        )
        fig.update_layout(
            barmode="stack",
            yaxis=dict(title="Écuries"),
            xaxis=dict(title="Total de points"),
        )
        return fig

    elif methode == "matplotlib":
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(data_sorted["constructorRef"], data_sorted["points"], color="#9467bd")
        ax.set_title("Classement des écuries")
        ax.set_xlabel("Points")
        ax.set_ylabel("Écurie")
        for i, (points, ecurie) in enumerate(
            zip(data_sorted["points"], data_sorted["constructorRef"])
        ):
            ax.text(points + 1, i, str(int(points)), va="center", fontsize=9)
        plt.tight_layout()
        return fig

    else:
        raise ValueError("La méthode doit être 'plotly' ou 'matplotlib'")


def plot_victoires_ecuries_saison(data: pd.DataFrame, methode: str = "plotly"):
    """
    Affiche un graphique en ligne représentant le nombre de victoires par saison
    pour chaque écurie sélectionnée.

    Parameters
    ----------
    data : pd.DataFrame
        Données avec les colonnes ["ecurie", "saison", "victoires"]
    methode : str
        "plotly" ou "matplotlib"

    Returns
    -------
    Figure Plotly ou Matplotlib
    """
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    if methode == "plotly":
        fig = px.line(
            data,
            x="saison",
            y="victoires",
            color="ecurie",
            markers=True,
            title="Évolution du nombre de victoires par écurie",
            labels={"saison": "Saison", "victoires": "Victoires", "ecurie": "Écurie"},
        )
        fig.update_layout(title_x=0.5)
        return fig

    elif methode == "matplotlib":
        fig, ax = plt.subplots(figsize=(10, 6))
        for ecurie in data["ecurie"].unique():
            subset = data[data["ecurie"] == ecurie]
            ax.plot(
                subset["saison"],
                subset["victoires"],
                marker="o",
                label=ecurie,
                linewidth=2,
            )
        ax.set_title("Évolution du nombre de victoires par écurie")
        ax.set_xlabel("Saison")
        ax.set_ylabel("Victoires")
        ax.legend(title="Écurie")
        ax.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        return fig

    else:
        raise ValueError("La méthode doit être 'plotly' ou 'matplotlib'")
