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
    Affiche un graphique empilé représentant la répartition des 3 premières positions
    (1ère place = or, 2e = argent, 3e = bronze) pour les pilotes,
    triés par nombre de points décroissants.
    Exclut les pilotes n'ayant aucun podium.

    Parameters
    ----------
    data : pd.DataFrame | dict
        Résultat de classement_saison, contenant les colonnes :
        - nom_pilote
        - points
        - "1", "2", "3"

    Returns
    -------
    plotly.graph_objects.Figure
        Graphique à barres horizontales empilées (or, argent, bronze)
    """
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    podium_cols = ["1", "2", "3"]

    # Supprimer les pilotes sans podium
    data["total_podiums"] = data[podium_cols].sum(axis=1)
    data = data[data["total_podiums"] > 0].copy()

    # Renommer les colonnes pour affichage
    data = data.rename(
        columns={"1": "Or", "2": "Argent", "3": "Bronze", "nom_pilote": "Nom"}
    )

    # Tri par points pour affichage
    data_sorted = data.sort_values("points", ascending=True)

    # Transformation en format long pour empilement
    melted = data_sorted.melt(
        id_vars="Nom",
        value_vars=["Or", "Argent", "Bronze"],
        var_name="Position",
        value_name="Nombre",
    )

    couleur_medaille = {"Or": "#FFD700", "Argent": "#C0C0C0", "Bronze": "#CD7F32"}

    fig = px.bar(
        melted,
        x="Nombre",
        y="Nom",
        color="Position",
        color_discrete_map=couleur_medaille,
        orientation="h",
        title="Nombre de podiums par pilote (or, argent, bronze)",
        labels={"Nom": "Pilote", "Nombre": "Podiums"},
        text_auto=True
    )

    fig.update_layout(
        barmode="stack",
        yaxis=dict(title="Pilote"),
        xaxis=dict(title="Total podiums"),
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
