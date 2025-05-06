import pandas as pd
import plotly.express as px
from Graphs.graphs_ecuries import plot_classement_saison_ecuries
from Queries.queries_ecuries import ecuriesPoints

df = ecuriesPoints(method='pandas' , saison= 2023)

fig=plot_classement_saison_ecuries(df)
fig.show()