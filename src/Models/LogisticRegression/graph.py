"""Fichier contenant les graphiques de la régression logistique"""

import plotly.graph_objects as go
import numpy as np


def plot_confusion_matrix(cm: np.ndarray, labels: list[str]) -> go.Figure:
    """
    Affiche une matrice de confusion sous forme de heatmap avec pourcentages.

    Parameters
    ----------
    cm : np.ndarray
        Matrice de confusion (2D)
    labels : list of str
        Noms des classes à afficher sur les axes

    Returns
    -------
    go.Figure
        Heatmap avec pourcentages ligne par ligne
    """
    cm = np.array(cm)

    row_sums = cm.sum(axis=1, keepdims=True)
    cm_pct = cm / row_sums * 100
    text = [[f"{v:.1f}%" for v in row] for row in cm_pct]

    fig = go.Figure(
        data=go.Heatmap(
            z=cm_pct,
            x=labels,
            y=labels,
            text=text,
            texttemplate="%{text}",
            colorscale="Blues",
            showscale=True,
        )
    )
    fig.update_layout(
        title="Matrice de confusion (% par classe réelle)",
        title_x=0.5,
        xaxis_title="Prédit",
        yaxis_title="Réel",
    )
    return fig
