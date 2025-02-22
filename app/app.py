from shiny import App, ui, render


app_ui = ui.page_navbar(
    ui.nav_panel(
        "Accueil",
        ui.page_sidebar(
            ui.sidebar(
                ui.input_slider(
                    "slider_accueil",
                    "Taille Beuteu Justin (en m)",
                    min=0,
                    max=100,
                    value=50,
                ),
                open="closed",
            ),
            ui.h2("Bienvenue sur la page d'accueil"),
            ui.output_text("texte_accueil"),
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
    @output
    @render.text
    def texte_accueil():
        return f"Valeur selectionnée : {input.slider_accueil()}"

    @output
    @render.text
    def texte_stat():
        return f"Quel est le meilleure Théorème : {input.choix_stat()}"

    @output
    @render.text
    def texte_param():
        return f"Sucer Justin : {'Oui' if input.activation() else 'Non'}"


app = App(app_ui, server)
