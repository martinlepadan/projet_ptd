# 🏁 Projet F1 — Analyse et Modélisation de Données de Formule 1

Bienvenue dans ce projet de visualisation, d'analyse statistique et de modélisation autour des données de Formule 1. Cette application interactive est développée en **Python** avec **Streamlit**, et permet d'explorer différentes facettes de la F1 à travers des requêtes, une régression logistique, un réseau de neurones et un clustering.

---

## 🚀 Fonctionnalités principales

### 📊 Requêtes interactives
- Nombre de victoires par pilote ou par écurie
- Classements de saisons
- Statistiques de carrière
- Temps de pit-stops

### 🤖 Modèle supervisé : Régression logistique
- Prédiction d’un podium à partir de données de course
- Comparaison avec/sans `class_weight="balanced"`
- Visualisations interactives (matrice de confusion, importance des variables)

### 🧠 Modèle non supervisé : Clustering
- Classification des pilotes selon leur style de carrière
- ACP (Analyse en Composantes Principales) pour la réduction de dimension
- Visualisation des groupes formés avec Plotly

---

## 🛠️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/martinlepadan/projet_ptd.git
cd projet_ptd_
```

## ▶️ Lancer l'application

```bash
python src/__main__.py
```
> [!NOTE]
> Le script vérifie automatiquement que tous les packages nécessaires sont bien installés

---

## 📁 Structure du projet

```

```

---

## 📦 Librairies utilisées

- `pandas` — manipulation de données
- `scikit-learn` — apprentissage supervisé et non supervisé
- `plotly` — graphiques interactifs
- `streamlit` — application web interactive
- `matplotlib`  — visualisation statique
- `numpy`

---
