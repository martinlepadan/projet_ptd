"""Fichier pour créer les graphes pour chaque question concernant les écuries"""

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def plot_classement_saison_ecuries(data: pd.DataFrame, methode: str) -> px.bar:
    """
    Affiche un graphique empilé représentant le classement des écuries
    triés par nombre de points décroissants.

    Parameters
    ----------
    data : pd.DataFrame


    Returns
    -------

    """
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    data = data.sort_values("points", ascending=True)

    if methode == "plotly":

    if methode == "plotly":
        fig = px.bar(
            data,
            x="points",
            y="constructorRef",
            orientation="h",
            title="Classement des écuries",
            labels={"constructorRef": "Ecurie", "points ": "points"},
            text_auto=True,
        )

        fig.update_layout(
            barmode="stack",
            yaxis=dict(title="Ecuries"),
            xaxis=dict(title="Total points"),
        )

        return fig


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
