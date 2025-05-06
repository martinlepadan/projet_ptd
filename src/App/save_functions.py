"""Fonctions pour sauvegarder les graphes et dataframes"""

import os
import pandas as pd


def save_dataframe(df: pd.DataFrame, filename: str = "export.csv") -> str:
    """Enregistre un DataFrame en CSV dans un dossier temporaire."""
    output_path = os.path.join("temp_exports", filename)
    os.makedirs("temp_exports", exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def save_figure(fig, filename: str = "export.png") -> str:
    """Enregistre une figure Plotly en image PNG."""
    output_path = os.path.join("temp_exports", filename)
    os.makedirs("temp_exports", exist_ok=True)
    fig.write_image(output_path)
    return output_path
