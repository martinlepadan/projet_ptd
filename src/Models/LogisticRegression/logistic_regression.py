"""Fichier contenant la fonction pour faire la régression logistique"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score


def compare_logistic() -> dict:
    """
    Cette fonction compare deux modèles de régression logistique :
    un modèle non pondéré et un modèle pondéré.

    Returns
    -------
    dict
        Un dictionnaire contenant les résultats des deux modèles.
        Chaque clé est le nom du modèle et la valeur est un dictionnaire
        contenant l'accuracy, la matrice de confusion et le rapport de classification.

    """
    df_results = pd.read_csv("data/results.csv")
    df_races = pd.read_csv("data/races.csv")
    df_constructors = pd.read_csv("data/constructors.csv")

    df = df_results.merge(df_races[["raceId", "year", "circuitId"]], on="raceId")
    df = df.merge(df_constructors[["constructorId", "name"]], on="constructorId")

    df["podium"] = (df["positionOrder"] <= 3).astype(int)

    features = ["grid", "year", "circuitId", "constructorId"]
    X = df[features]
    y = df["podium"]

    num_cols = ["grid", "year"]
    cat_cols = ["circuitId", "constructorId"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ]
    )

    def make_model(class_weight=None):
        return Pipeline(
            [
                ("preprocessor", preprocessor),
                (
                    "classifier",
                    LogisticRegression(max_iter=1000, class_weight=class_weight),
                ),
            ]
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=0.2, random_state=42
    )

    models = {
        "Non pondérée": make_model(class_weight=None),
        "Pondérée": make_model(class_weight="balanced"),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results[name] = {
            "accuracy": accuracy_score(y_test, y_pred),
            "confusion_matrix": confusion_matrix(y_test, y_pred),
            "report": classification_report(y_test, y_pred, output_dict=True),
        }

    return results
