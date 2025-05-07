# 🏁 Projet Red Bull - Analyse de données F1

Bienvenue dans ce projet de visualisation, d'analyse statistique et de modélisation autour des données de Formule 1. Cette application interactive est développée en **Python** avec **Streamlit**. Elle permet d'explorer ce jeu de données de différentes manières à l'aide d'outils d'apprentissages supervisés et non supervisé, ainsi que de représentations graphiques.

---

## 🚀 Fonctionnalités principales

### 📊 Requêtes interactives
- Nombre de victoires par pilote ou par écurie
- Classements de saisons
- Statistiques de carrière
- Temps de pit-stops
- Sauvegade des graphes et données possible

### 📊 Modèle supervisé : Régression logistique
- Prédiction d’un podium à partir de données de course
- Comparaison avec/sans `class_weight="balanced"`
- Visualisations interactives (matrice de confusion, importance des variables)

### 🧠 Modèle non supervisé : Clustering
- Classification des pilotes selon leur style de carrière
- ACP (Analyse en Composantes Principales) pour la réduction de dimension
- Visualisation des groupes formés avec Plotly

### 🤖 Modèle supervisé : Réseaux de neurones
- Création de son propre réseau de neurones
- Visualisation des résultats par époch
- Totalement optionnel
---

## 🛠️ Installation et lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/martinlepadan/projet_ptd.git
cd projet_ptd
```

### 2. Lancer l'application

```bash
python __main__.py
```
> [!NOTE]
> Le script vérifie automatiquement que tous les packages nécessaires sont bien installés

---

## 📁 Structure du projet

```bash
projet_traitement/
├── .flake8
├── .gitignore
├── __main__.py
├── AUTHORS.md
├── LICENSE
├── README.md
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── data/
│   └── *.csv
├── src/
│   ├── __init__.py
│   ├── Analysis/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── utils.py
│   │   ├── Graphs/
│   │   │   ├── __init__.py
│   │   │   ├── graphs_ecuries.py
│   │   │   ├── graphs_pilotes.py
│   │   │   └── graphs_pit_stops.py
│   │   └── Queries/
│   │       ├── __init__.py
│   │       ├── queries_ecuries.py
│   │       ├── queries_pilotes.py
│   │       └── queries_pit_stops.py
│   ├── App/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── assets/
│   │       └── Red-Bull-Logo.png
│   └── Models/
│       ├── __init__.py
│       ├── Classification/
│       │   ├── __init__.py
│       │   ├── classification.py
│       │   └── graph.py
│       ├── LogisticRegression/
│       │   ├── __init__.py
│       │   ├── graph.py
│       │   └── logistic_regression.py
│       └── NeuralNetwork/
│           ├── __init__.py
│           ├── graphs.py
│           ├── neural_network.py
│           └── train.py
└── test/
    ├── test_ecuries.py
    └── test_pilotes.py

```

## 📢 Remarques
- Les graphes/dataframes des requêtes pit-stops peuvent mettre un peu de temps à s'afficher et à s'actualiser.
- Si vous voulez télécharger le graphe associé à une requête, choisissez l'option `matplotlib`. Si vous préférez l'interactvité et l'intégration, choisissez l'option `plotly`.
- Si vous réalisez des réseaux de neurones, ne mettez pas d'hyperparamètres trop lourds (nombre de couche, neurones). Il s'entraîne sur votre machine et n'est pas du tout optimisé, le but étant surtout de le rendre personnalisable.
---

## 📦 Librairies utilisées

- `pandas` — manipulation de données
- `scikit-learn` — apprentissage supervisé et non supervisé
- `plotly` — graphiques interactifs
- `streamlit` — application web interactive
- `matplotlib`  — visualisation statique
- `pytorch` — réseaux de neurones
---
