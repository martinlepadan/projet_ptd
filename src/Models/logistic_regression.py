"""Fichier pour réaliser une régression logistique"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
)
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Chargement des données nécessaires
drivers = pd.read_csv("data/drivers.csv")
results = pd.read_csv("data/results.csv")
races = pd.read_csv("data/races.csv")
constructors = pd.read_csv("data/constructors.csv")

# Fusion des données
df = results.merge(drivers, on="driverId")
df = df.merge(races[["raceId", "year", "circuitId"]], on="raceId")
df = df.merge(constructors[["constructorId", "name"]], on="constructorId")

# Création de la variable cible : 1 si le pilote finit dans les 3 premiers, 0 sinon
df["podium"] = (df["positionOrder"] <= 3).astype(int)

# Sélection des variables explicatives
features = ["grid", "year", "circuitId", "constructorId"]
X = df[features]
y = df["podium"]

# Préparation des colonnes catégorielles et numériques
numeric_features = ["grid", "year"]
categorical_features = ["circuitId", "constructorId"]

# Pipeline de prétraitement
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

# Pipeline complet avec modèle
clf = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000)),
    ]
)

# Séparation train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Entraînement
clf.fit(X_train, y_train)

# Prédictions
y_pred = clf.predict(X_test)

# Évaluation
evaluation_results = {
    "accuracy": accuracy_score(y_test, y_pred),
    "confusion_matrix": confusion_matrix(y_test, y_pred),
    "classification_report": classification_report(y_test, y_pred),
}

print(evaluation_results)
