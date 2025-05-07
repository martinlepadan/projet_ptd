"""
Routeur entre les identifiants de questions et les fonctions associées
(pour les requêtes et pour les graphes).
"""

from typing import Callable
from src.Analysis.Queries import queries_pilotes, queries_ecuries, queries_pit_stops
from src.Analysis.Graphs import graphs_pilotes, graphs_ecuries, graphs_pit_stops


def get_question(question_id: str) -> Callable | None:
    """
    Associe un identifiant de question à sa fonction de requête.

    Parameters
    ----------
    question_id : str
        Identifiant de la question

    Returns
    -------
    Callable | None
        La fonction de requête correspondante ou None si non trouvée.
    """
    functions = {
        "q1": queries_pilotes.nombre_victoires_pilotes,
        "q2": queries_pilotes.classement_saison,
        "q3": queries_pilotes.temps_de_carriere_pilotes,
        "q4": queries_ecuries.victoires_ecuries_saison,
        "q5": queries_pit_stops.pit_stop,
        "q6": queries_pit_stops.min_pit_stop,
        "q7": queries_pilotes.statistiques_pilote,
        "q8": queries_ecuries.ecuries_points,
        "q9": queries_ecuries.victoires_ecurie_relatif,
    }
    return functions.get(question_id)


def get_graph(question_id: str) -> Callable | None:
    """
    Associe un identifiant de question à sa fonction de visualisation.

    Parameters
    ----------
    question_id : str
        Identifiant de la question

    Returns
    -------
    Callable | None
        La fonction de graphe correspondante ou None si non trouvée.
    """
    functions = {
        "q1": graphs_pilotes.plot_nombre_victoires_pilotes,
        "q2": graphs_pilotes.plot_classement_saison,
        "q3": graphs_pilotes.plot_temps_de_carriere_pilotes,
        "q4": graphs_ecuries.plot_victoires_ecuries_saison,
        "q5": graphs_pit_stops.plot_temps_pit_stop,
        "q6": graphs_pit_stops.plot_min_pit_stop,
        "q7": graphs_pilotes.plot_carriere_pilote,
        "q8": graphs_ecuries.plot_classement_saison_ecuries,
    }
    return functions.get(question_id)
