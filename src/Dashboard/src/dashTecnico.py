import pandas as pd
from dash import html, dcc
import dash
import dash_bootstrap_components as dbc


estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.COSMO]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
# FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"


app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])


app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True
server = app.server

app.layout = dbc.Container(children=[
    dbc.Col(children=[html.Div("Track Vision - Green Power", className="titulo")],md = 12),
    dbc.Col(children=[
        html.H6("Seu Perfil:", className="abaperfil")
    ],md = 2)
],className="page-content")

if __name__ == '__main__':
    app.run_server(debug=True)



