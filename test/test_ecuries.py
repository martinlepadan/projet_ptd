"""
Tests unitaires pour les requêtes sur les écuries.
"""

from src.Analysis.Queries.queries_ecuries import ecuries_points


def test_red_bull_points_2023():
    """
    Red Bull a remporté environ 800 points en 2023.
    """
    df = ecuries_points("pandas", saison=2023)
    top = df.sort_values("points", ascending=False).iloc[0]
    assert "red_bull" in top["constructorRef"].lower()
    assert abs(top["points"] - 800) <= 30
