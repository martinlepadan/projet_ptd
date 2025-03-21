from shiny import App, ui, reactive, render
from functions import get_query_as_df, QUERY_PATH

with open(QUERY_PATH) as txtfile:
    file = txtfile.read()
queries = [r.strip() for r in file.split(';') if r.strip()]

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Accueil",
        ui.page_sidebar(
            ui.sidebar(
                ui.input_slider(
                    "slider_accueil",
                    "Nombre de victoire minimales",
                    min=0,
                    max=100,
                    value=0,
                ),
                open="closed",
            ),
            ui.output_table("victoires_par_pilote"),
        ),
    ),
    ui.nav_panel(
        "Statistiques",
        ui.page_sidebar(
            ui.sidebar(
                ui.input_select(
                    "choix_stat",
                    "Choisir une statistique",
                    {"Benyamé-Tchebichev": "Benyamé-Tchebichev", "Fubini-Tonneli": "Fubini-Tonneli"},
                ),
                open="closed",
            ),
            ui.h2("Page des Statistiques"),
            ui.output_text("texte_stat"),
        ),
    ),
    ui.nav_panel(
        "Paramètres",
        ui.page_sidebar(
            ui.sidebar(
                ui.input_checkbox("activation", "Option Secrète", False),
                open="closed",
            ),
            ui.h2("Page des Paramètres"),
            ui.output_text("texte_param"),
        ),
    ),
    title="Projet Traitement de Données - Formule 1",
)


def server(input, output, session):

    @reactive.Calc
    def dataframe():
        return get_query_as_df(queries[0], int(input.slider_accueil()))

    @output()
    @render.table
    def victoires_par_pilote():
        return dataframe()

    @output
    @render.text
    def texte_stat():
        return f"Quel est le meilleure Théorème : {input.choix_stat()}"

    @output
    @render.text
    def texte_param():
        return f"Sucer Justin : {'Oui' if input.activation() else 'Non'}"


app = App(app_ui, server)
