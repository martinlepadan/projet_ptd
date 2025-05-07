"""
Fichier contenant les fonctions de création de graphes.
"""

import plotly.graph_objects as go
import numpy as np


def plot_loss_curves(train_losses: list[float], test_metrics: dict) -> go.Figure:
    """
    Trace l'évolution de la perte (loss) pour l'entraînement et le test avec Plotly.

    Parameters
    ----------
    train_losses : list[float]
        Liste des pertes (loss) enregistrées à chaque ecpochs sur le jeu d'entraînement.
    test_metrics : dict
        Dictionnaire contenant les métriques de test toutes les 10 epochs

    Returns
    -------
    go.Figure
        Figure Plotly affichant les courbes de perte d'entraînement et de test.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(1, len(train_losses) + 1)),
            y=train_losses,
            mode="lines+markers",
            name="Loss (train)",
            line=dict(color="blue"),
        )
    )

    if test_metrics:
        epochs = list(test_metrics.keys())
        test_loss = [test_metrics[ep]["loss"] for ep in epochs]
        fig.add_trace(
            go.Scatter(
                x=epochs,
                y=test_loss,
                mode="lines+markers",
                name="Loss (test)",
                line=dict(color="red"),
            )
        )

    fig.update_layout(
        title="Évolution de la perte",
        xaxis_title="Époch",
        yaxis_title="Loss",
        legend=dict(x=0.01, y=0.99),
        template="plotly_white",
    )
    return fig


def plot_accuracy_curves(
    train_accuracies: list[float], test_metrics: dict
) -> go.Figure:
    """
    Trace l'évolution de la'accuracy' pour l'entraînement et le test avec Plotly.

    Parameters
    ----------
    train_accuracies : list[float]
        Liste des pertes (loss) enregistrées à chaque époque sur le jeu d'entraînement.
    test_metrics : dict
        Dictionnaire contenant les métriques de test à certaines époques
        (tous les 10 epochs),
        de la forme {epoch: {"loss": float, "accuracy": float}}.

    Returns
    -------
    go.Figure
        Figure Plotly affichant les courbes d'accuracy d'entraînement et de test.
    """
    fig = go.Figure()

    acc_train = [a * 100 for a in train_accuracies if not np.isnan(a)]
    fig.add_trace(
        go.Scatter(
            x=list(range(1, len(acc_train) + 1)),
            y=acc_train,
            mode="lines+markers",
            name="Accuracy (train)",
            line=dict(color="green"),
        )
    )

    if test_metrics:
        epochs = list(test_metrics.keys())
        test_acc = [
            test_metrics[ep]["accuracy"] * 100
            for ep in epochs
            if not np.isnan(test_metrics[ep]["accuracy"])
        ]
        fig.add_trace(
            go.Scatter(
                x=epochs,
                y=test_acc,
                mode="lines+markers",
                name="Accuracy (test)",
                line=dict(color="orange"),
            )
        )

    fig.update_layout(
        title="Évolution de l'accuracy",
        xaxis_title="Époch",
        yaxis_title="Accuracy (%)",
        legend=dict(x=0.01, y=0.99),
        template="plotly_white",
    )
    return fig
