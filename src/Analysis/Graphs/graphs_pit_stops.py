"""Fichier pour créer le graphe de la question sur les pit-stops"""

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def plot_temps_pit_stop(data, methode: str):
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    data_sorted = data.sort_values("pit_stop_moyen", ascending=True)

    if methode == "plotly":
        fig = px.bar(
            data_sorted,
            x="constructor_unifie",
            y="pit_stop_moyen",
            range_y=[min(data_sorted["pit_stop_moyen"])-0.1, max(data_sorted["pit_stop_moyen"])+0.1],
            title="Temps moyen de pit-stop par écurie",
            labels={"pit_stop_moyen": "Temps pit-stop (secondes)", "constructor_unifie": "Ecurie"},
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig