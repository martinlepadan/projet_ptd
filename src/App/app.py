"""Application Streamlit"""

import streamlit as st
import pandas as pd
from src.Analysis.router import get_question, get_graph
import io


st.set_page_config(page_title="Analyse de données F1", layout="wide")
st.markdown(
    """
    <style>
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    st.image("Red-Bull-Logo.png", width=400)

st.markdown(
    """
    <h1 style='text-align: center; font-family: Futura, Trebuchet MS, sans-serif;'>
        Red Bull Project
    </h1>
    """,
    unsafe_allow_html=True
)



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
            "q4": "Nombre de victoires par écurie par saison",
            "q8": "Classement écuries par saison",
            "q10": "Dashboard écuries",
        },
        "Pit-Stops": {
            "q5": "Temps moyen de pit-stop par écurie par saison (2020-2023)",
        },
    }

    emojis = {"Pilotes": "🏁", "Écuries": "🏎️", "Pit-Stops": "🛠️"}

    question_emojis = {
        "q1": "🏆",
        "q2": "📊",
        "q3": "⏱️",
        "q5": "🔧",
        "q7": "🧑‍💼",
        "q8": "🏆",
        "q10": "📊",
    }

    descriptions = {
        "q1": "Affiche les pilotes ayant gagné un certain nombre de courses.",
        "q2": "Affiche le classement final des pilotes pour une saison donnée.",
        "q3": "Montre la durée de carrière de chaque pilote.",
        "q4": "Montre le nombre de victoires par écurie par saison.",
        "q5": "Compare le temps moyen des pit-stops par écurie.",
        "q7": "Fournit un résumé statistique de la carrière d'un pilote.",
        "q8": "Affiche le classement final des écuries pour une saison donnée.",
        "q10": "Renvoie un dashboard avec 3 statistiques générales d'écuries.",
    }

    for theme, questions in THEMES.items():
        emoji = emojis.get(theme)
        with st.expander(f"{emoji} {theme}", expanded=False):
            question_label = st.selectbox(
                "🧩 Questions",
                options=list(questions.keys()),
                format_func=lambda k: f"{question_emojis.get(k, '')} {questions[k]}",
                key=f"{theme}-question",
                index=None,
                placeholder="Choisissez une question ...",
            )

            st.success(descriptions.get(question_label, "Sélectionnez une question."))

            if question_label is not None:
                query_func = get_question(question_label)
                plot_func = get_graph(question_label)

                method = None
                if question_label in ["q1", "q10"]:
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
                elif question_label == "q3":
                    params["duree_min"] = st.number_input(
                        "⏱️ Durée de carrière minimum (en années)",
                        min_value=0,
                        value=15,
                        max_value=24,
                    )
                elif question_label == "q4":
                    ecurie = pd.read_csv("data/constructors.csv")
                    ecurie_dispo = ecurie["name"].unique().tolist()
                    params["ecuries"] = st.multiselect(
                        "🏎️ Sélectionnez les écuries",
                        options=sorted(ecurie_dispo),
                        default=["Red Bull", "BMW", "Mercedes", "McLaren"],
                        key="select-ecuries",
                    )
                    if len(params["ecuries"]) == 0:
                        st.warning("Veuillez sélectionner au moins une écurie.")
                        st.stop()

                    params["saisons"] = st.slider(
                        "📅 Saison",
                        min_value=1950,
                        max_value=2023,
                        value=(1985, 2020),
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
                        index=521,
                    )
                elif question_label == "q8":
                    params["saison"] = st.slider(
                        "📅 Saison",
                        min_value=1950,
                        max_value=2023,
                        value=2023,
                        key="slider-q8",
                    )
                elif question_label == "q10":
                    ecurie = pd.read_csv("data/constructors.csv")
                    ecurie_dispo = ecurie["name"].unique().tolist()

                    params["ecurie"] = st.selectbox(
                        "🏎️ Choisissez une écurie",
                        options=sorted(ecurie_dispo),
                        key="select-ecurie",
                        index=167,
                    )
                if question_label == "q10":
                    st.subheader("📊 Dashboard - Statistiques de l'écurie")

                    # Extraire les trois valeurs attendues du DataFrame
                    total_victoires, nb_participations, moyenne_victoires = query_func(
                        method, **params
                    )

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            label="🏆 Total des victoires",
                            value=int(total_victoires),
                            help=(
                                "Nombre total de victoires enregistrées par l'écurie "
                                "sur toutes ses saisons."
                            ),
                        )
                    with col2:
                        st.metric(
                            label="📅 Saisons disputées",
                            value=int(nb_participations),
                            help=(
                                "Nombre de saisons où l'écurie a participé à "
                                "au moins une course."
                            ),
                        )
                    with col3:
                        st.metric(
                            label="📈 Moyenne de victoires/saison",
                            value=moyenne_victoires,
                            help=(
                                "Nombre moyen de victoires par saison "
                                "pour cette écurie."
                            ),
                        )
                else:
                    if method:
                        df = query_func(method=method, **params)
                    else:
                        df = query_func(**params)
                    st.session_state[f"df_{question_label}"] = df

                    # Récupérer les données stockées
                    df = st.session_state.get(f"df_{question_label}")

                    if df is not None:
                        st.subheader("📄 Données")
                        st.dataframe(df)

                        st.subheader("💾 Exporter les données")
                        filename_csv = st.text_input(
                            "Nom du fichier CSV",
                            "resultats.csv",
                            key=f"csv-filename-{question_label}",
                        )
                        st.download_button(
                            label="Télécharger les données (.csv)",
                            data=df.to_csv(index=False).encode("utf-8"),
                            file_name=filename_csv,
                            mime="text/csv",
                            key=f"csv-{question_label}",
                            icon=":material/download:",
                        )

                        if plot_func is not False:
                            st.subheader("📊 Visualisation")

                            methode_graph = st.radio(
                                "Méthode d'affichage du graphe :",
                                options=["plotly", "matplotlib"],
                                key=f"graph-type-{question_label}",
                            )

                            if question_label == "q7":
                                figs = plot_func(df, methode=methode_graph)

                                if methode_graph == "plotly":
                                    fig1, fig2 = figs
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.plotly_chart(fig1, use_container_width=True)
                                    with col2:
                                        st.plotly_chart(fig2, use_container_width=True)

                                elif methode_graph == "matplotlib":
                                    fig = figs
                                    st.pyplot(fig)

                                    st.subheader("🖼️ Exporter le graphe")
                                    filename_png = st.text_input(
                                        "Nom du fichier PNG",
                                        "carriere_pilote.png",
                                        key=f"png-filename-{question_label}",
                                    )

                                    buffer = io.BytesIO()
                                    fig.savefig(
                                        buffer, format="png", bbox_inches="tight"
                                    )
                                    buffer.seek(0)

                                    st.download_button(
                                        label="Télécharger le graphique (.png)",
                                        data=buffer,
                                        file_name=filename_png,
                                        mime="image/png",
                                        key=f"png-{question_label}",
                                        icon=":material/download:",
                                    )

                            else:
                                fig = plot_func(df, methode=methode_graph)

                                if methode_graph == "plotly":
                                    st.plotly_chart(fig, use_container_width=True)

                                elif methode_graph == "matplotlib":
                                    st.pyplot(fig)

                                    st.subheader("🖼️ Exporter le graphe")
                                    filename_png = st.text_input(
                                        "Nom du fichier PNG",
                                        "graphique.png",
                                        key=f"png-filename-{question_label}",
                                    )

                                    buffer = io.BytesIO()
                                    fig.savefig(
                                        buffer, format="png", bbox_inches="tight"
                                    )
                                    buffer.seek(0)

                                    st.download_button(
                                        label="Télécharger le graphique (.png)",
                                        data=buffer,
                                        file_name=filename_png,
                                        mime="image/png",
                                        key=f"png-{question_label}",
                                        icon=":material/download:",
                                    )


# ========== ONGLET 2 : RÉGRESSION ========== #
with tabs[1]:
    st.header("📊 Modèle de Régression")

# ========== ONGLET 3 : RÉSEAU DE NEURONES ========== #
with tabs[2]:
    st.header("🧠 Prédictions par réseau de neurones")
