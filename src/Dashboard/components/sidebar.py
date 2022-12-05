import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from datetime import datetime, date
from dash_bootstrap_templates import ThemeChangerAIO
from globals import *

# ========= Layout ========= #
layout = dbc.Card([
                html.Img(src="assets/track-vision.png"),
                html.Hr(),
                dbc.Card(id='botao_avatar',
                    children=[html.Img(src="/assets/tecnico.png", id="avatar_change", alt="Avatar", className='perfil_avatar'),
                ], style={'background-color': 'transparent', 'border-color': 'transparent','margin-left':'10px'}),

            dbc.Row([
                dbc.Col([
                    html.H5("Logado como:")
                ], width=12, style={"text-align":"center"}),
            ]),
                        dbc.Row([
                dbc.Col([
                    html.H5("TÉCNICO")
                ], width=12, style={"text-align":"center","color":"green"}),
            ]),
        
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Dashboard", href="/dashboards", active="exact"),
                ], vertical=True, pills=True, id='nav_buttons', style={"margin-bottom": "50px"}),
            ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.BOOTSTRAP})

        ], id='sidebar_completa'
    )