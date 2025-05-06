"""Application Streamlit"""

import streamlit as st
import pandas as pd
from src.Analysis.router import get_question, get_graph


st.set_page_config(page_title="F1 Analysis App", layout="wide")

st.title("🏎️ REDBULL PROJECT - Analyse des données F1")

tabs = st.tabs(["Requêtes", "Régression", "Réseau de Neurones"])

# ========== ONGLET 1 : REQUÊTES ========== #
with tabs[0]:
    st.header("🔍 Analyse par thématique")

    THEMES = {
        "Pilotes": {
            "q1": "Nombre de victoires par pilote",
            "q2": "Classement des pilotes pour une saison",
            "q3": "Temps de carrière des pilotes",
            "q7": "Statistiques de carrière d'un pilote",
        },
        "Écuries": {
            "q4": "Classement des écuries par année",
        },
        "Pit-Stops": {
            "q5": "Temps moyen de pit-stop par écurie",
        },
    }

    emojis = {"Pilotes": "🏁", "Écuries": "🏎️", "Pit-Stops": "🛠️"}

    question_emojis = {
        "q1": "🏆",
        "q2": "📊",
        "q3": "⏱️",
        "q4": "📈",
        "q5": "🔧",
        "q7": "🧑‍💼",
    }

    descriptions = {
        "q1": "Affiche les pilotes ayant gagné un certain nombre de courses.",
        "q2": "Affiche le classement final des pilotes pour une saison donnée.",
        "q3": "Montre la durée de carrière de chaque pilote.",
        "q4": "Montre le classement des écuries pour une saison donnée.",
        "q5": "Compare le temps moyen des pit-stops par écurie.",
        "q7": "Fournit un résumé statistique de la carrière d'un pilote.",
    }

    for theme, questions in THEMES.items():
        emoji = emojis.get(theme)
        with st.expander(f"{emoji} {theme}", expanded=False):
            question_label = st.selectbox(
                "🧩 Questions",
                options=list(questions.keys()),
                format_func=lambda k: f"{question_emojis.get(k, '')} {questions[k]}",
                key=f"{theme}-question",
            )

            st.success(descriptions.get(question_label, "Sélectionnez une question."))

            query_func = get_question(question_label)
            plot_func = get_graph(question_label)

            method = None
            if question_label in ["q1", "q4", "q5", "q6"]:
                method = st.selectbox(
                    "⚙️ Méthode",
                    options=["pandas", "homemade"],
                    key=f"{question_label}-method",
                )

            params = {}

            if question_label == "q1":
                params["nb_victoires"] = st.number_input(
                    "🏁 Seuil minimum de victoires", min_value=0, value=30
                )
            elif question_label == "q2":
                params["saison"] = st.slider(
                    "📅 Saison",
                    min_value=1950,
                    max_value=2023,
                    value=2023,
                    key="slider-q2",
                )
            elif question_label == "q4":
                params["saison"] = st.slider(
                    "📅 Saison",
                    min_value=1950,
                    max_value=2023,
                    value=2023,
                    key="slider-q4",
                )
            elif question_label == "q5":
                params["saison"] = st.slider(
                    "📅 Saison",
                    min_value=1950,
                    max_value=2023,
                    value=2023,
                    key="slider-q5",
                )
            elif question_label == "q7":
                drivers = pd.read_csv("data/drivers.csv")
                pilote_dispo = (
                    drivers.apply(
                        lambda row: row["forename"] + " " + row["surname"], axis=1
                    )
                    .unique()
                    .tolist()
                )

                params["nom_pilote"] = st.selectbox(
                    "👤 Choisissez un pilote",
                    options=sorted(pilote_dispo),
                    key="select-pilote",
                )

            if st.button("🚀 Exécuter", key=f"btn-{question_label}"):
                if method:
                    df = query_func(method=method, **params)
                else:
                    df = query_func(**params)

                st.subheader("📄 Données")
                st.dataframe(df)

                st.subheader("💾 Exporter les données")
                filename_csv = st.text_input("Nom du fichier CSV", "resultats.csv")
                st.download_button(
                    label="Télécharger les données (.csv)",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name=filename_csv,
                    mime="text/csv",
                    key=f"csv-{question_label}",
                    icon=":material/download:",
                )

                st.subheader("📊 Visualisation")
                fig = plot_func(df)
                st.plotly_chart(fig, use_container_width=True)


# ========== ONGLET 2 : RÉGRESSION ========== #
with tabs[1]:
    st.header("📊 Modèle de Régression")

# ========== ONGLET 3 : RÉSEAU DE NEURONES ========== #
with tabs[2]:
    st.header("🧠 Prédictions par réseau de neurones")
