"""Fichier permettant d'envoyer les questions et graphes vers l'application Dash"""

import src.Analysis.queries as queries
import src.Analysis.graphs as graphs


def get_question(question_id):
    functions = {
        "q1": queries.nombre_victoires_pilotes,
        "q2": queries.classement_saison,
        "q3": queries.temps_de_carriere_pilotes,
    }
    return functions.get(question_id)


def get_graph(question_id):
    functions = {
        "q1": graphs.plot_nombre_victoires_pilotes,
        "q2": graphs.plot_classement_saison,
        "q3": graphs.plot_temps_de_carriere_pilotes,
    }
    return functions.get(question_id)
