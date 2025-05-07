"""Tests unitaires pour les requêtes."""

from src.Analysis.Queries.queries_pilotes import (
    nombre_victoires_pilotes,
    classement_saison,
    temps_de_carriere_pilotes,
)
from src.Analysis.Queries.queries_ecuries import ecuriesPoints


def test_hamilton_victoires():
    """
    Lewis Hamilton a remporté 103 courses (jusqu'en 2024)
    """
    df = nombre_victoires_pilotes("pandas", nb_victoires=30)
    row = df[df["nom_pilote"] == "Lewis Hamilton"]
    assert not row.empty
    assert abs(row["wins"].values[0] - 103) <= 5


def test_verstappen_victoires():
    """
    Max Verstappen a remporté environ 54 courses à la fin de 2023.
    """
    df = nombre_victoires_pilotes("pandas", nb_victoires=30)
    row = df[df["nom_pilote"] == "Max Verstappen"]
    assert row["wins"].values[0] >= 54


def test_red_bull_points_2023():
    """
    Red Bull a remporté environ 800 points en 2023.
    """
    df = ecuriesPoints("pandas", saison=2023)
    top = df.sort_values("points", ascending=False).iloc[0]
    assert "red_bull" in top["constructorRef"].lower()
    assert abs(top["points"] - 800) <= 30


def test_classement_verstappen_2023():
    """
    Max Verstappen est le champion du monde 2023.
    """
    df = classement_saison(saison=2023)
    assert df.iloc[0]["nom_pilote"] == "Max Verstappen"


def test_carriere_schumacher():
    """
    Michael Schumacher a eu une carrière de 21 ans
    """
    df = temps_de_carriere_pilotes(0)
    row = df[df["nom_pilote"] == "Michael Schumacher"]
    assert abs(row["duree"].values[0] - 21) <= 2
