"""Fichier pour créer les graphes pour chaque question concernant les pilotes"""

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
        text_auto=True,
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


def plot_statistiques_pilote(df: pd.DataFrame) -> px.bar:
    """
    Affiche un graphique esthétique des statistiques d’un pilote :
    podiums et nombre de courses participées.
    """
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    pilot = df.iloc[0]["nom_pilote"]
    stats = {
        "🥇 Or (1er)": df.iloc[0]["nb_podiums_1"],
        "🥈 Argent (2e)": df.iloc[0]["nb_podiums_2"],
        "🥉 Bronze (3e)": df.iloc[0]["nb_podiums_3"],
        "🏁 Courses participées": df.iloc[0]["nb_courses"],
    }

    graph_df = pd.DataFrame(list(stats.items()), columns=["Statistique", "Valeur"])

    fig = px.bar(
        graph_df,
        x="Valeur",
        y="Statistique",
        orientation="h",
        text="Valeur",
        color="Statistique",
        color_discrete_map={
            "🥇 Or (1er)": "#FFD700",
            "🥈 Argent (2e)": "#C0C0C0",
            "🥉 Bronze (3e)": "#CD7F32",
            "🏁 Courses participées": "#7f7f7f",
        },
        title=f"Statistiques de carrière de {pilot}",
    )

    fig.update_traces(textposition="outside", marker_line_width=1.5)
    fig.update_layout(
        title_x=0.5,
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        height=400,
        margin=dict(l=50, r=20, t=50, b=30),
    )
    return fig

def plot_podium_ratio(df: pd.DataFrame) -> px.pie:
    """
    Graphe circulaire montrant la proportion de podiums vs autres arrivées.
    """
    pilot = df.iloc[0]["nom_pilote"]
    total = df.iloc[0]["nb_courses"]
    podiums = sum(df.iloc[0][f"nb_podiums_{i}"] for i in [1, 2, 3])
    autres = total - podiums

    pie_df = pd.DataFrame({
        "Catégorie": ["Podiums", "Autres"],
        "Valeur": [podiums, autres]
    })

    fig = px.pie(
        pie_df,
        values="Valeur",
        names="Catégorie",
        title=f"Proportion de podiums pour {pilot}",
        color="Catégorie",
        color_discrete_map={"Podiums": "#FFD700", "Autres": "#d3d3d3"},
    )
    fig.update_layout(title_x=0.5)
    return fig
