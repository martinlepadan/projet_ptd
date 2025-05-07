"""
Fichier permettant d'appliquer ACP et Kmeans sur un dataset
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def clustering_pilotes(n_clusters=3):
    """
    Effectue une ACP puis clustering des pilotes de F1
    en fonction de leurs performances.

    Parameters
    -----------
    n_clusters : int = 3
        Le nombre de clusters à former avec l'algorithme K-Means.
    Returns
    --------
    pd.DataFrame
        Un DataFrame contenant les informations agrégées des pilotes, leurs clusters
        et les deux premières composantes principales (PC1 et PC2).
    list
        Une liste des noms des caractéristiques utilisées pour le clustering.
    """
    drivers = pd.read_csv("data/drivers.csv")
    standings = pd.read_csv("data/driver_standings.csv")
    races = pd.read_csv("data/races.csv")

    df = standings.merge(drivers, on="driverId").merge(
        races[["raceId", "year"]], on="raceId"
    )
    df["nom_pilote"] = df["forename"] + " " + df["surname"]

    df_agg = df.groupby("nom_pilote").agg(
        {"points": "sum", "wins": "sum", "raceId": "count", "year": ["min", "max"]}
    )
    df_agg.columns = ["points", "wins", "courses", "debut", "fin"]
    df_agg["duree"] = df_agg["fin"] - df_agg["debut"] + 1
    df_agg["pts_par_course"] = df_agg["points"] / df_agg["courses"]
    df_agg = df_agg[
        df_agg["courses"] >= 10
    ]  # Sinon on a des pilotes qui n'ont pas fait assez de courses

    features = ["points", "wins", "courses", "duree", "pts_par_course"]
    X = df_agg[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    clusters = kmeans.fit_predict(X_scaled)

    df_agg["cluster"] = clusters
    df_agg["PC1"] = X_pca[:, 0]
    df_agg["PC2"] = X_pca[:, 1]

    return df_agg.reset_index(), features
