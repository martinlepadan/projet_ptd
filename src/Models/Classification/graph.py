"""
Fichier contenant la fonction de visualisation des clusters
"""

import plotly.express as px
import pandas as pd


def graph_classification(df_clustered: pd.DataFrame):
    """
    Affiche un nuage de points en 2D issu d'une ACP, coloré par cluster.

    Parameters
    ----------
    df_clustered : pd.DataFrame
        Le dataframe contenant les résultats de l'ACP et les clusters

    Returns
    -------
    px.Figure
        Scatterplot de l'ACP avec les clusters
    """
    fig = px.scatter(
            df_clustered,
            x="PC1",
            y="PC2",
            color=df_clustered["cluster"].astype(str),
            color_discrete_sequence=px.colors.qualitative.Plotly,
            hover_name="nom_pilote",
            title="Clustering des pilotes (ACP + k-means)",
            labels={"cluster": "Groupe"},
        )
    return fig
