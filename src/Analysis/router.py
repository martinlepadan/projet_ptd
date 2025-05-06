"""Fichier permettant d'envoyer les questions et graphes vers l'application Dash"""

from src.Analysis.Queries import queries_pilotes, queries_ecuries, queries_pit_stops
from src.Analysis.Graphs import graphs_pilotes, graphs_ecuries, graphs_pit_stops


def get_question(question_id):
    functions = {
        "q1": queries_pilotes.nombre_victoires_pilotes,
        "q2": queries_pilotes.classement_saison,
        "q3": queries_pilotes.temps_de_carriere_pilotes,
        "q4": queries_ecuries.ecuriesPoints,
        "q5": queries_pit_stops.pit_stop,
        "q7": queries_pilotes.statistiques_pilote,
        "q8": queries_ecuries.ecuriesPoints,
        "q9": queries_ecuries.victoiresEcuries,
    }
    return functions.get(question_id)


def get_graph(question_id):
    functions = {
        "q1": graphs_pilotes.plot_nombre_victoires_pilotes,
        "q2": graphs_pilotes.plot_classement_saison,
        "q3": graphs_pilotes.plot_temps_de_carriere_pilotes,
        # "q5": graphs_pit_stops.plot_temps_pit_stop,
        "q7": graphs_pilotes.plot_statistiques_pilote,
        "q8": graphs_ecuries.plot_classement_saison_ecuries,
    }
    return functions.get(question_id, False)
