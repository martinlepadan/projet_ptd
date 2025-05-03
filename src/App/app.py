"""Application Dash"""

import sys
import os
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "REDBULL PROJECT"

app.layout = dbc.Container(
    [
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Analyse des données",
                    children=[
                        html.Div(
                            className="control-panel",
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4("Paramètres de la requête"),
                                                dcc.Dropdown(
                                                    id="question-selector",
                                                    options=[
                                                        {
                                                            "label": "Points par écurie/"
                                                            "saison",
                                                            "value": "q1",
                                                        },
                                                        {
                                                            "label": "Performances par "
                                                            "pilote",
                                                            "value": "q2",
                                                        },
                                                        {
                                                            "label": "Évolution des "
                                                            "performances",
                                                            "value": "q3",
                                                        },
                                                    ],
                                                    value="q1",
                                                ),
                                                html.Br(),
                                                dcc.Dropdown(
                                                    id="method-selector",
                                                    options=[
                                                        {
                                                            "label": "Pandas",
                                                            "value": "homemade",
                                                        },
                                                        {
                                                            "label": "Python Pur",
                                                            "value": "homemade",
                                                        },
                                                    ],
                                                    value="pandas",
                                                ),
                                                html.Br(),
                                                html.Div(id="dynamic-parameters"),
                                                html.Br(),
                                                dbc.Button(
                                                    "Exécuter la requête",
                                                    id="run-query",
                                                    color="primary",
                                                ),
                                            ],
                                            md=3,
                                        ),
                                        dbc.Col(
                                            [
                                                html.H4("Résultats"),
                                                dcc.Loading(
                                                    id="loading-results",
                                                    type="default",
                                                    children=[
                                                        html.Div(id="results-table"),
                                                        dcc.Graph(id="results-plot"),
                                                    ],
                                                ),
                                            ],
                                            md=9,
                                        ),
                                    ]
                                )
                            ],
                        )
                    ],
                ),
                # REGRESSION
                dcc.Tab(
                    label="Modèle de Régression",
                    children=[
                        html.Div(
                            [
                                html.H3("Analyse par régression linéaire"),
                            ]
                        )
                    ],
                ),
                # NN
                dcc.Tab(
                    label="Réseau de Neurones",
                    children=[
                        html.Div(
                            [
                                html.H3("Prédictions par réseau de neurones"),
                            ]
                        )
                    ],
                ),
            ]
        )
    ],
    fluid=True,
)


@app.callback(
    Output("dynamic-parameters", "children"), Input("question-selector", "value")
)
def update_parameters(selected_question):
    """Adapte les paramètres dynamiques selon la question sélectionnée"""
    if selected_question == "q1":
        return [
            dcc.Slider(
                id="season-slider",
                min=1950,
                max=2023,
                value=2023,
                marks={str(year): str(year) for year in range(1950, 2025, 5)},
            )
        ]
    elif selected_question == "q2":
        return [
            dcc.Dropdown(
                id="driver-selector",
                options=[],
                multi=True,
            )
        ]


@app.callback(
    [Output("results-table", "children"), Output("results-plot", "figure")],
    [Input("run-query", "n_clicks")],
    [
        State("question-selector", "value"),
        State("method-selector", "value"),
        State("season-slider", "value"),
    ],
)
def run_query(n_clicks, question, method, season):
    """Exécute la requête et retourne les résultats"""
    if n_clicks is None:
        return dash.no_update, dash.no_update
    query_func = get_question(question)

    results_df, plot_fig = query_func(
        method=method,
        season=season,
    )

    table = dash_table.DataTable(
        data=results_df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in results_df.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
    )

    return table, plot_fig


if __name__ == "__main__":
    app.run(debug=True)
