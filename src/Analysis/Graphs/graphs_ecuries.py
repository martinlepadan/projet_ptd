"""Fichier pour créer les graphes pour chaque question concernant les écuries"""

import pandas as pd
import plotly.express as px

# Q8 :

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
    
    if methode == 'plotly':
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
    
# Q9 : Graphe du nombre de victoires par écurie et par saison
