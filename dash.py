

# Dash
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
# Plot (graph)
import plotly_express as px
import plotly.graph_objects as go


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])  # DARKLY BOOTSTRAP CYBORG VAPOR SKETCHY
server=app.server

app.layout=html.Div(className="graph",children =[
    html.H1(children="DashBoard - Covid 19", style={'textAlign': 'center'}),
    html.Hr(),
    html.Br(),
])

#https://dash.plotly.com/basic-callbacks meilleur site




