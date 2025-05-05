"""Fichier pour créer les graphes pour chaque question"""

import pandas as pd
import plotly.express as px


def plot_nombre_victoires_pilotes(data) -> px.bar:
    """
    Génère un graphique à barres représentant le nombre de victoires des pilotes.

    Parameters
    ----------
    data : pd.DataFrame | dict
        Données des pilotes avec les colonnes "nom_pilote" et "wins".
        Peut être un dictionnaire Python (homemade) ou un DataFrame (pandas).

    Returns
    -------
    plotly.graph_objects.Figure
        Graphique à barres trié décroissant
    """

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    fig = px.bar(
        data,
        x="nom_pilote",
        y="wins",
        title="Nombre de victoires par pilote",
        labels={"nom_pilote": "Pilote", "wins": "Victoires"},
    )
    fig.update_layout(xaxis_tickangle=-45)

    return fig


def plot_classement_saison(data: pd.DataFrame) -> px.bar:
    """
    Affiche un graphique empilé représentant la répartition des positions d'arrivée
    (1ère place, 2e, etc.) pour les pilotes, triés par nombre de points décroissants.

    Parameters
    ----------
    data : pd.DataFrame | dict
        Résultat de classement_saison, contenant les colonnes :
        - nom_pilote
        - points
        - colonnes "1", "2", "3", ..., représentant les positions

    Returns
    -------
    plotly.graph_objects.Figure
        Graphique à barres horizontales empilées
    """

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    # Identifier les colonnes de positions (entiers uniquement)
    position_cols = [col for col in data.columns if col.isdigit()]
    data_sorted = data.sort_values("points", ascending=True)

    # Transformation pour graphique empilé
    melted = data_sorted.melt(
        id_vars="nom_pilote",
        value_vars=position_cols,
        var_name="Position",
        value_name="Nombre",
    )

    fig = px.bar(
        melted,
        x="Nombre",
        y="nom_pilote",
        color="Position",
        orientation="h",
        title="Répartition des positions d'arrivée par pilote",
        labels={"nom_pilote": "Pilote", "Nombre": "Arrivées"},
    )

    fig.update_layout(
        barmode="stack",
        yaxis=dict(title="Pilote"),
        xaxis=dict(title="Nombre total de positions"),
    )
    return fig


def plot_temps_de_carriere_pilotes(data) -> px.bar:
    """
    Génère un graphique à barres représentant le temps de carrière des pilotes.

    Parameters
    ----------
    data : pd.DataFrame | dict
        Données des pilotes

    Returns
    -------
    plotly.graph_objects.Figure
        Graphique à barres trié décroissant
    """

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    fig = px.bar(
        data,
        x="nom_pilote",
        y="duree",
        title="Temps de carrière par pilote",
        labels={"nom_pilote": "Pilote", "duree": "Durée (années)"},
    )
    fig.update_layout(xaxis_tickangle=-45)

    return fig
