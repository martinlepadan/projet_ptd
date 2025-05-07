"""Application Streamlit"""

import os
import streamlit as st
import pandas as pd
import io
import time
import keyboard
import psutil
import numpy as np

from src.Analysis.router import get_question, get_graph
from src.Models.LogisticRegression.logistic_regression import compare_logistic
from src.Models.LogisticRegression.graph import plot_confusion_matrix
from src.Models.Classification.classification import clustering_pilotes
from src.Models.Classification.graph import graph_classification


bonus_mode = os.getenv("BONUS_MODE", "Non") == "Oui"

st.set_page_config(page_title="Analyse de données F1", layout="wide")
st.markdown(
    """
    <style>
    header, .stElementToolbar {
    visibility: hidden;
    }

    div[data-testid="stMainBlockContainer"] {
        padding-top: 3em;
    }
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    st.image("./src/App/assets/Red-Bull-Logo.png", width=400)

st.markdown(
    """
    <h1 style='text-align: center; font-family: Futura, Trebuchet MS, sans-serif;'>
        Red Bull Project
    </h1>
    """,
    unsafe_allow_html=True,
)

if bonus_mode:
    tabs = st.tabs(["Requêtes", "Régression", "Classification", "Réseau de Neurones"])
else:
    tabs = st.tabs(["Requêtes", "Régression", "Classification"])


# ONGLET 1 : REQUÊTES
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
            "q4": "Nombre de victoires par écurie et par saison",
            "q8": "Classement écuries par saison",
            "q9": "Dashboard écuries",
        },
        "Pit-Stops": {
            "q5": "Temps moyen de pit-stop par écurie par saison (2020-2023)",
            "q6": "Temps de pit-stop minimal par saison",
        },
    }

    emojis = {"Pilotes": "🏁", "Écuries": "🏎️", "Pit-Stops": "🛠️"}

    question_emojis = {
        "q1": "🏆",
        "q2": "📊",
        "q3": "⏱️",
        "q4": "🏎️",
        "q5": "🔧",
        "q6": "⏱️",
        "q7": "🧑‍💼",
        "q8": "🏆",
        "q9": "📊",
    }

    descriptions = {
        "q1": "Affiche les pilotes ayant gagné un certain nombre de courses.",
        "q2": "Affiche le classement final des pilotes pour une saison donnée.",
        "q3": "Montre la durée de carrière de chaque pilote.",
        "q4": "Montre le nombre de victoires par écurie par saison.",
        "q5": "Compare le temps moyen des pit-stops par écurie.",
        "q6": "Donne le meilleur pit-stop de chaque saison.",
        "q7": "Fournit un résumé statistique de la carrière d'un pilote.",
        "q8": "Affiche le classement final des écuries pour une saison donnée.",
        "q9": "Renvoie un dashboard avec 3 statistiques générales d'écuries.",
    }

    for theme, questions in THEMES.items():
        emoji = emojis.get(theme)
        with st.expander(f"{emoji} {theme}", expanded=False):
            st.markdown("""---""")
            question_label = st.selectbox(
                "🧩 Questions",
                options=list(questions.keys()),
                format_func=lambda k: f"{question_emojis.get(k, '')} {questions[k]}",
                key=f"{theme}-question",
                index=None,
                placeholder="Choisissez une question ...",
            )

            st.success(descriptions.get(question_label, "Sélectionnez une question."))
            st.markdown("""---""")
            if question_label is not None:
                st.markdown("""### 🔨 Variables""")
                query_func = get_question(question_label)
                plot_func = get_graph(question_label)

                method = None
                if question_label in ["q1", "q6", "q9"]:
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
                elif question_label == "q9":
                    ecurie = pd.read_csv("data/constructors.csv")
                    ecurie_dispo = ecurie["name"].unique().tolist()

                    params["ecurie"] = st.selectbox(
                        "🏎️ Choisissez une écurie",
                        options=sorted(ecurie_dispo),
                        key="select-ecurie",
                        index=167,
                    )
                if question_label == "q9":
                    st.subheader("📊 Dashboard - Statistiques de l'écurie")

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

                    df = st.session_state.get(f"df_{question_label}")

                    if df is not None:
                        st.markdown("""---""")
                        st.markdown("### 📄 Données")
                        st.dataframe(df)

                        st.markdown("##### 💾 Exporter les données")
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
                        st.markdown("""---""")
                        if plot_func is not None:
                            st.markdown("### 📊 Visualisation")

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

                                    st.markdown("##### 🖼️ Exporter le graphe")
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

                                    st.markdown("##### 🖼️ Exporter le graphe")
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


# ONGLET 2 : RÉGRESSION
with tabs[1]:
    st.header("📊 Régression Logistique — Prédiction de podium")

    st.markdown(
        """
        Ce modèle de régression logistique a pour objectif de **prédire si un pilote va
        terminer sur le podium (top 3)**
        en se basant sur certaines caractéristiques comme sa position de départ,
        l'écurie ou l'année.

        ⚠️ Le jeu de données est fortement **déséquilibré** : la majorité des pilotes ne
        finissent pas sur le podium.
        C'est pourquoi nous comparons deux versions du modèle :

        - Une version **non pondérée** (standard)
        - Une version **pondérée avec l'option `class_weight="balanced"`**, qui corrige
        le déséquilibre des classes

        Cette comparaison permet de mieux comprendre l'impact de la pondération sur la
        **précision globale** et sur la **capacité à bien détecter les podiums**.

        ---
        """
    )

    if "results" not in st.session_state:
        if st.button("📈 Lancer et comparer les deux modèles"):
            with st.spinner("En cours de traitement..."):
                results = compare_logistic()
                st.session_state["results"] = results

    if "results" in st.session_state:
        results = st.session_state["results"]

        col1, col2 = st.columns(2)
        for name, col, emoji in zip(
            ["Non pondérée", "Pondérée"], [col1, col2], ["⚙️", "⚖️"]
        ):
            with col:
                st.subheader(f"{emoji} {name}")
                res = results[name]

                st.metric(label="🎯 Accuracy", value=f"{res['accuracy']:.2%}")

                report_df = pd.DataFrame(res["report"]).transpose().round(3)
                report_df.rename(index={"0": "Pas podium", "1": "Podium"}, inplace=True)
                st.dataframe(report_df.style.format("{:.3f}"), height=240)

        st.markdown("---")
        st.subheader("📊 Matrices de confusion (% par classe réelle)")
        col1, col2 = st.columns(2)
        for name, col in zip(["Non pondérée", "Pondérée"], [col1, col2]):
            with col:
                fig_cm = plot_confusion_matrix(
                    results[name]["confusion_matrix"], ["Pas podium", "Podium"]
                )
                st.plotly_chart(fig_cm, use_container_width=True)

        st.markdown(
            """
            ---

            **💡 Interprétation** :
            - Le modèle **non pondéré** a une meilleure accuracy globale car il prédit
            principalement "Pas podium", ce qui fonctionne bien dans un jeu déséquilibré.
            - Le modèle **avec `class_weight="balanced"`** se trompe moins sur les
            podiums (rappel plus élevé), ce qui est souvent plus utile dans un contexte
            où les podiums sont rares.
            - La matrice de confusion montre que le modèle pondéré fait moins d'erreurs
            sur les podiums, mais a plus de faux positifs (prédit podium alors que
            ce n'est pas le cas).
            """
        )

# ONGLET 3 : ACP + K-MEANS
with tabs[2]:
    st.header("🧠 Clustering des pilotes selon leur style de carrière")

    st.markdown(
        """
        Cette analyse utilise un algorithme de **k-means** pour regrouper les pilotes en
        fonction de leur carrière :
        - Total de points
        - Nombre de victoires
        - Nombre de courses disputées
        - Durée de carrière
        - Moyenne de points par course

        On utilise également une **ACP** (Analyse en Composantes Principales) pour
        réduire la dimension à 2 axes et visualiser les groupes formés.

        ---
        """
    )
    n_clusters = st.slider(
        "Nombre de groupes (clusters)", min_value=2, max_value=10, value=3
    )

    if st.button("Lancer le clustering"):
        with st.spinner("Clustering en cours..."):
            df_clustered, used_vars = clustering_pilotes(n_clusters=n_clusters)

        st.success(f"{len(df_clustered)} pilotes analysés.")

        st.dataframe(df_clustered[["nom_pilote", "cluster"] + used_vars])

        fig = graph_classification(df_clustered)
        st.plotly_chart(fig, use_container_width=True)

# ONGLET 4 : RÉSEAU DE NEURONES
if bonus_mode:
    from src.Models.NeuralNetwork.train import train_model

    with tabs[3]:
        st.header("🤖 Prédictions par réseau de neurones")
        st.markdown(
            """
                    - Ce modèle repose sur un **réseau de neurones PyTorch**.
                    - Il permet de prédire une variable cible (continue ou binaire)
                    à partir de données de course.
                    - L'utilisateur peut personnaliser l'architecture : couches,
                    dropout, learning rate, etc.
                    - Des graphiques interactifs affichent l'évolution de la perte et
                    de l'accuracy.
                    - Le but n'est absolument pas de faire de bonnes prédictions, mais
                    juste d'explorer de façon amusante le jeu de données.
                    """
        )

        st.markdown("Sélectionnez les paramètres de votre modèle :")

        results = pd.read_csv("data/results.csv")
        drivers = pd.read_csv("data/drivers.csv")
        races = pd.read_csv("data/races.csv")
        constructors = pd.read_csv("data/constructors.csv")
        driver_standings = pd.read_csv("data/driver_standings.csv")
        constructor_standings = pd.read_csv("data/constructor_standings.csv")

        races_filtered = races[races["year"] >= 2010]
        results_filtered = results[results["raceId"].isin(races_filtered["raceId"])]

        top_drivers = results_filtered["driverId"].value_counts().nlargest(100).index
        results_filtered = results_filtered[
            results_filtered["driverId"].isin(top_drivers)
        ]

        df = (
            results_filtered.merge(drivers, on="driverId", how="left")
            .merge(
                races_filtered[["raceId", "year", "circuitId"]], on="raceId", how="left"
            )
            .merge(constructors, on="constructorId", how="left")
            .merge(
                driver_standings,
                on=["driverId", "raceId"],
                how="left",
                suffixes=("", "_ds"),
            )
            .merge(
                constructor_standings,
                on=["constructorId", "raceId"],
                how="left",
                suffixes=("", "_cs"),
            )
        )

        df = df.dropna(axis=1, thresh=len(df) * 0.9)
        df = df.select_dtypes(include=["number", "object"]).copy()

        selected_columns = [
            "grid",
            "positionOrder",
            "points",
            "laps",
            "milliseconds",
            "fastestLap",
            "rank",
            "fastestLapSpeed",
            "year",
            "points_ds",
            "position_ds",
            "wins",
            "points_cs",
            "position_cs",
            "wins_cs",
            "circuitId",
            "constructorRef",
            "driverRef",
        ]

        df = df[selected_columns].rename(
            columns={
                "grid": "Position de départ",
                "positionOrder": "Position finale",
                "points": "Points",
                "laps": "Tours",
                "milliseconds": "Temps",
                "fastestLap": "Tour le plus rapide",
                "rank": "Rang",
                "fastestLapSpeed": "Vitesse du tour le plus rapide",
                "year": "Année",
                "points_ds": "Points pilote saison",
                "position_ds": "Position pilote saison",
                "wins": "Victoires du pilote",
                "points_cs": "Points écurie saison",
                "position_cs": "Position écurie saison",
                "wins_cs": "Victoires de l'écurie",
                "circuitId": "Circuit",
                "constructorRef": "Écurie",
                "driverRef": "Pilote",
            }
        )

        colonnes = df.columns.tolist()

        with st.expander("### 🧮 Paramètres du modèle"):

            target = st.selectbox(
                "🎯 Variable à prédire",
                placeholder="Choisissez une variable à prédire ...",
                options=colonnes,
                index=None,
            )

            features = st.pills(
                "🎯 Variables explicatives",
                options=[col for col in colonnes if col != target],
                selection_mode="multi",
            )

            n_epochs = st.slider(
                "🔁 Nombre d'epochs",
                min_value=10,
                max_value=500,
                value=100,
                step=10,
                help="Nombre d'itérations pour entraîner le modèle.",
            )

            dropout_rate = st.slider(
                "💧 Dropout",
                min_value=0.0,
                max_value=0.9,
                step=0.05,
                value=0.2,
                help="Taux de neurones à ignorer pour éviter le surapprentissage.",
            )

            lr = st.number_input(
                "⚙️ Learning rate",
                value=0.001,
                format="%.5f",
                help="Taux d'apprentissage pour le modèle.",
                step=0.0005,
            )

            st.markdown("🧱 Architecture des couches cachées")
            if "hidden_layers" not in st.session_state:
                st.session_state.hidden_layers = [64]

            add = st.button(
                "➕ Ajouter une couche",
                disabled=len(st.session_state.hidden_layers) >= 4,
            )
            remove = st.button(
                "➖ Supprimer la dernière couche",
                disabled=len(st.session_state.hidden_layers) <= 1,
            )

            if add:
                st.session_state.hidden_layers.append(64)
            if remove:
                st.session_state.hidden_layers.pop()

            hidden_sizes = []
            for i, size in enumerate(st.session_state.hidden_layers):
                neurons = st.number_input(
                    f"🧠 Couche cachée {i + 1}",
                    min_value=1,
                    max_value=512,
                    value=size,
                    step=1,
                    key=f"layer_{i}",
                )
                hidden_sizes.append(neurons)

        st.markdown("#### 🔧 Paramètres de configuration du réseau de neurones")
        architecture = [{", ".join(str(n) for n in hidden_sizes)}]
        st.code(
            f"""
                📌 Cible : {target}
                🎯 Variables explicatives : {', '.join(features)}
                🧱 Architecture : {len(hidden_sizes)} couches — {architecture}
                💧 Dropout : {dropout_rate}
                ⚙️ Learning Rate : {lr}
                🔁 Epochs : {n_epochs}
                """,
            language="yaml",
        )

        if st.button("🚀 Entraîner le réseau de neurones"):
            with st.spinner("🔁 Entraînement du modèle..."):
                try:
                    from src.Models.NeuralNetwork.graphs import (
                        plot_loss_curves,
                        plot_accuracy_curves,
                    )

                    df_clean = df.dropna(subset=features + [target])

                    model, train_losses, train_accuracies, test_metrics = train_model(
                        df=df_clean,
                        features=features,
                        target=target,
                        hidden_sizes=hidden_sizes,
                        dropout=dropout_rate,
                        lr=lr,
                        epochs=n_epochs,
                    )

                    st.success("🎉 Entraînement terminé avec succès !")

                    st.subheader("📋 Récapitulatif des dernières métriques")
                    if len(train_losses) > 0:
                        st.metric(
                            "📉 Dernière perte (train)", f"{train_losses[-1]:.4f}"
                        )

                    has_accuracy = not all(np.isnan(train_accuracies))

                    if has_accuracy:
                        st.metric(
                            "✅ Dernière accuracy (train)",
                            f"{train_accuracies[-1]*100:.2f}%",
                        )

                    if test_metrics:
                        last_epoch = max(test_metrics.keys())
                        st.metric(
                            "🧪 Perte test (dernier point)",
                            f"{test_metrics[last_epoch]['loss']:.4f}",
                        )
                        if has_accuracy and "accuracy" in test_metrics[last_epoch]:
                            acc = test_metrics[last_epoch]["accuracy"]
                            if not np.isnan(acc):
                                st.metric(
                                    "🧪 Accuracy test (dernier point)",
                                    f"{acc*100:.2f}%",
                                )

                    st.subheader("📊 Évolution des métriques (tous les 10 epochs)")
                    table_data = []
                    for epoch in range(0, len(train_losses), 10):
                        ep = epoch + 1
                        t_loss = train_losses[epoch]
                        t_acc = (
                            train_accuracies[epoch]
                            if epoch < len(train_accuracies)
                            else np.nan
                        )
                        test = test_metrics.get(ep, {})
                        row = {
                            "Époch": ep,
                            "Loss (train)": round(t_loss, 4),
                            "Loss (test)": round(test.get("loss", np.nan), 4),
                        }

                        if has_accuracy:
                            row["Accuracy (train)"] = (
                                round(t_acc * 100, 2) if not np.isnan(t_acc) else "—"
                            )
                            row["Accuracy (test)"] = (
                                round(test["accuracy"] * 100, 2)
                                if "accuracy" in test and not np.isnan(test["accuracy"])
                                else "—"
                            )

                        table_data.append(row)

                    st.dataframe(table_data, use_container_width=True)

                    st.subheader("📈 Courbes de perte (Train & Test)")
                    fig_loss = plot_loss_curves(train_losses, test_metrics)
                    st.pyplot(fig_loss)

                    if has_accuracy:
                        st.subheader("📈 Courbes d'accuracy (Train & Test)")
                        fig_acc = plot_accuracy_curves(train_accuracies, test_metrics)
                        st.pyplot(fig_acc)
                    else:
                        st.info(
                            "ℹ️ Pas de courbe d'accuracy — tâche de régression détectée."
                        )
                except Exception as e:
                    st.error(f"❌ Une erreur est survenue : {e}")


exit_app = st.button("Quitter l'app")
if exit_app:
    time.sleep(0.5)
    keyboard.press_and_release("ctrl+w")
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()
