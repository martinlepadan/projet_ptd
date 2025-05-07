"""
Graphiques liés aux statistiques des pilotes de F1.
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def plot_nombre_victoires_pilotes(data: pd.DataFrame, methode: str = "plotly"):
    """
    Affiche un histogramme des pilotes selon leur nombre de victoires.

    Parameters
    ----------
    data : pd.DataFrame
        Doit contenir les colonnes ["nom_pilote", "wins"].
    methode : str
        "plotly" (par défaut) ou "matplotlib".

    Returns
    -------
    fig : Figure Plotly ou Matplotlib
    """
    data_sorted = data.sort_values("wins", ascending=False)

    if methode == "plotly":
        fig = px.bar(
            data_sorted,
            x="nom_pilote",
            y="wins",
            title="Nombre de victoires par pilote",
            labels={"nom_pilote": "Pilote", "wins": "Victoires"},
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig

    elif methode == "matplotlib":
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(data_sorted["nom_pilote"], data_sorted["wins"], color="#1f77b4")
        ax.set_title("Nombre de victoires par pilote")
        ax.set_ylabel("Victoires")
        ax.set_xticks(range(len(data_sorted)))
        ax.set_xticklabels(data_sorted["nom_pilote"], rotation=45, ha="right")
        plt.tight_layout()
        return fig

    raise ValueError("La méthode doit être 'plotly' ou 'matplotlib'")


def plot_classement_saison(data: pd.DataFrame, methode: str = "plotly"):
    """
    Affiche un graphique empilé des podiums (or, argent, bronze) pour chaque pilote.

    Parameters
    ----------
    data : pd.DataFrame
        Doit contenir ["nom_pilote", "1", "2", "3", "points"].
    methode : str
        "plotly" ou "matplotlib".

    Returns
    -------
    fig : Figure Plotly ou Matplotlib
    """
    podium_cols = ["1", "2", "3"]
    data["total_podiums"] = data[podium_cols].sum(axis=1)
    data = data[data["total_podiums"] > 0].copy()
    data_sorted = data.sort_values("points", ascending=True)

    if methode == "plotly":
        data_sorted = data_sorted.rename(
            columns={"1": "Or", "2": "Argent", "3": "Bronze", "nom_pilote": "Nom"}
        )
        melted = data_sorted.melt(
            id_vars="Nom",
            value_vars=["Or", "Argent", "Bronze"],
            var_name="Position",
            value_name="Nombre",
        )
        fig = px.bar(
            melted,
            x="Nombre",
            y="Nom",
            color="Position",
            orientation="h",
            title="Nombre de podiums par pilote (or, argent, bronze)",
            color_discrete_map={
                "Or": "#FFD700",
                "Argent": "#C0C0C0",
                "Bronze": "#CD7F32",
            },
            labels={"Nom": "Pilote", "Nombre": "Podiums"},
            text_auto=True,
        )
        fig.update_layout(barmode="stack", title_x=0.5)
        return fig

    elif methode == "matplotlib":
        noms = data_sorted["nom_pilote"]
        or_, argent, bronze = data_sorted["1"], data_sorted["2"], data_sorted["3"]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(noms, or_, color="#FFD700", label="Or")
        ax.barh(noms, argent, left=or_, color="#C0C0C0", label="Argent")
        ax.barh(noms, bronze, left=or_ + argent, color="#CD7F32", label="Bronze")
        ax.set_title("Nombre de podiums par pilote (or, argent, bronze)")
        ax.set_xlabel("Nombre de podiums")
        ax.legend()
        plt.tight_layout()
        return fig

    raise ValueError("La méthode doit être 'plotly' ou 'matplotlib'")


def plot_temps_de_carriere_pilotes(data: pd.DataFrame, methode: str = "plotly"):
    """
    Affiche un graphique représentant la durée de carrière des pilotes.

    Parameters
    ----------
    data : pd.DataFrame
        Doit contenir les colonnes ["nom_pilote", "duree"].
    methode : str
        "plotly" ou "matplotlib".

    Returns
    -------
    fig : Figure Plotly ou Matplotlib
    """
    data_sorted = data.sort_values("duree", ascending=False)

    if methode == "plotly":
        fig = px.bar(
            data_sorted,
            x="nom_pilote",
            y="duree",
            title="Temps de carrière par pilote",
            labels={"nom_pilote": "Pilote", "duree": "Durée (années)"},
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig

    elif methode == "matplotlib":
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(data_sorted["nom_pilote"], data_sorted["duree"], color="#2ca02c")
        ax.set_title("Temps de carrière par pilote")
        ax.set_ylabel("Durée (années)")
        ax.set_xticks(range(len(data_sorted)))
        ax.set_xticklabels(data_sorted["nom_pilote"], rotation=45, ha="right")
        plt.tight_layout()
        return fig

    raise ValueError("La méthode doit être 'plotly' ou 'matplotlib'")


def plot_carriere_pilote(df: pd.DataFrame, methode: str = "plotly"):
    """
    Affiche les statistiques détaillées (barres + camembert) pour un pilote unique.

    Parameters
    ----------
    df : pd.DataFrame
        Une seule ligne avec colonnes : nom_pilote, nb_podiums_1/2/3, nb_courses
    methode : str
        "plotly" ou "matplotlib"

    Returns
    -------
    fig : Plotly (2) ou Matplotlib (1)
    """
    pilot = df.iloc[0]["nom_pilote"]
    stats = {
        "🥇 Or (1er)": df.iloc[0]["nb_podiums_1"],
        "🥈 Argent (2e)": df.iloc[0]["nb_podiums_2"],
        "🥉 Bronze (3e)": df.iloc[0]["nb_podiums_3"],
        "🏁 Courses participées": df.iloc[0]["nb_courses"],
    }
    total = stats["🏁 Courses participées"]
    podiums = stats["🥇 Or (1er)"] + stats["🥈 Argent (2e)"] + stats["🥉 Bronze (3e)"]
    autres = total - podiums

    if methode == "plotly":
        df_barres = pd.DataFrame(stats.items(), columns=["Stat", "Valeur"])
        fig1 = px.bar(
            df_barres,
            x="Valeur",
            y="Stat",
            orientation="h",
            title=f"Statistiques de carrière de {pilot}",
            color="Stat",
            color_discrete_map={
                "🥇 Or (1er)": "#FFD700",
                "🥈 Argent (2e)": "#C0C0C0",
                "🥉 Bronze (3e)": "#CD7F32",
                "🏁 Courses participées": "#7f7f7f",
            },
        )
        fig1.update_layout(title_x=0.5, showlegend=False)

        df_pie = pd.DataFrame(
            {"Catégorie": ["Podiums", "Autres"], "Valeur": [podiums, autres]}
        )
        fig2 = px.pie(
            df_pie,
            values="Valeur",
            names="Catégorie",
            title=f"Ratio podiums / autres pour {pilot}",
            color="Catégorie",
            color_discrete_map={"Podiums": "#FFD700", "Autres": "#d3d3d3"},
        )
        fig2.update_layout(title_x=0.2)
        return fig1, fig2

    elif methode == "matplotlib":
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Barres horizontales
        labels = list(stats.keys())
        values = list(stats.values())
        colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#7f7f7f"]
        bars = axes[0].barh(labels, values, color=colors)
        axes[0].set_title(f"Statistiques de carrière de {pilot}")
        for bar in bars:
            w = bar.get_width()
            axes[0].text(
                w + 0.5, bar.get_y() + bar.get_height() / 2, str(int(w)), va="center"
            )

        # Camembert
        axes[1].pie(
            [podiums, autres],
            labels=["Podiums", "Autres"],
            autopct="%1.1f%%",
            colors=["#FFD700", "#d3d3d3"],
            startangle=140,
        )
        axes[1].set_title("Ratio podiums / autres")

        plt.tight_layout()
        return fig

    raise ValueError("La méthode doit être 'plotly' ou 'matplotlib'")
