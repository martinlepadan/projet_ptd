import streamlit as st
from src.Analysis.router import get_question, get_graph

st.set_page_config(page_title="F1 Analysis App", layout="wide")

st.title("🏎️ REDBULL PROJECT - Analyse des données F1")

# Tabs principaux
tabs = st.tabs(["Requêtes", "Régression", "Réseau de Neurones"])

# ========== ONGLET 1 : REQUÊTES ==========
with tabs[0]:
    st.header("Analyse par thématique")

    THEMES = {
        "Pilotes": {
            "q1": "Nombre de victoires par pilote",
            "q2": "Classement des pilotes pour une saison",
            "q3": "Temps de carrière des pilotes",
        },
        "Écuries": {"q4": "Classement des écuries par année"},
        "Pit-Stops": {"q5": "Temps moyen de pit-stop par écurie"},
        "Circuits": {"q6": "Performances par type de circuit"},
    }

    emojis = {
        "Pilotes": "🏁",
        "Écuries": "🏎️",
        "Pit-Stops": "🛠️",
        "Circuits": "🛤️",
    }

    for theme, questions in THEMES.items():
        emoji = emojis.get(theme, "📂")
        with st.expander(f"{emoji} {theme}", expanded=False):
            question_label = st.selectbox(
                f"Question ({theme})",
                options=list(questions.keys()),
                format_func=lambda k: questions[k],
                key=f"{theme}-question",
            )
            query_func = get_question(question_label)
            plot_func = get_graph(question_label)

            # Sélecteurs selon la question
            method = None
            if question_label in ["q1", "q4", "q5", "q6"]:
                method = st.selectbox(
                    "Méthode",
                    options=["pandas", "homemade"],
                    key=f"{question_label}-method",
                )

            params = {}
            if question_label == "q1":
                params["nb_victoires"] = st.number_input(
                    "Seuil minimum de victoires", min_value=0, value=30
                )
            elif question_label == "q2":
                params["saison"] = st.slider(
                    "Saison2", min_value=1950, max_value=2023, value=2023
                )
            elif question_label == "q4":
                params["saison"] = st.slider(
                    "Saison4", min_value=1950, max_value=2023, value=2023
                )
            elif question_label == "q5":
                params["saison"] = st.slider(
                    "Saison5", min_value=1950, max_value=2023, value=2023
                )

            if st.button("Exécuter", key=f"btn-{question_label}"):
                # Appel de la fonction
                if method:
                    df = query_func(method=method, **params)
                else:
                    df = query_func(**params)

                st.subheader("🧾 Données")
                st.dataframe(df)

                if plot_func:
                    st.subheader("📈 Visualisation")
                    fig = plot_func(df)
                    st.plotly_chart(fig, use_container_width=True)

# ========== ONGLET 2 : RÉGRESSION ==========
with tabs[1]:
    st.header("📊 Modèle de Régression")
    st.info("À compléter : affichage des résultats de la régression linéaire.")

# ========== ONGLET 3 : RÉSEAU DE NEURONES ==========
with tabs[2]:
    st.header("🧠 Prédictions par réseau de neurones")
    st.info("À compléter : chargement modèle, prédictions, visualisation.")
