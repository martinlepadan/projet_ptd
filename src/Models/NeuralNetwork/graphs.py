"""
Fichier contenant les fonctions de création de graphes.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_loss_curves(train_losses, test_metrics):
    fig, ax = plt.subplots()
    ax.set_xlabel("Époch")
    ax.set_ylabel("Loss")

    ax.plot(
        range(1, len(train_losses) + 1), train_losses, label="Train Loss", color="blue"
    )

    if test_metrics:
        epochs = list(test_metrics.keys())
        test_loss = [test_metrics[ep]["loss"] for ep in epochs]
        ax.plot(epochs, test_loss, label="Test Loss", color="red")

    ax.set_title("Évolution des pertes")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_accuracy_curves(train_accuracies, test_metrics):
    if all(np.isnan(train_accuracies)) and not test_metrics:
        return None

    fig, ax = plt.subplots()
    ax.set_xlabel("Époch")
    ax.set_ylabel("Accuracy (%)")

    if not all(np.isnan(train_accuracies)):
        acc_train_percent = [a * 100 for a in train_accuracies]
        ax.plot(
            range(1, len(acc_train_percent) + 1),
            acc_train_percent,
            label="Train Accuracy",
            color="green",
        )

    if test_metrics:
        epochs = list(test_metrics.keys())
        test_acc = [test_metrics[ep]["accuracy"] * 100 for ep in epochs]
        ax.plot(epochs, test_acc, label="Test Accuracy", color="orange")

    ax.set_title("Évolution des accuracies")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    return fig
