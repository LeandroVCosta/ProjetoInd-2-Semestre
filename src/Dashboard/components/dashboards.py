from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app

import pdb
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

graph_margin=dict(l=25, r=25, t=25, b=0)


# =========  Layout  =========== #
layout = dbc.Col([
        dbc.Row([
            # Saldo
            dbc.Col([
                    dbc.CardGroup([
                            dbc.Card([
                                    html.Legend("Plano de Energia"),
                                    html.H5("Atual:", id="p-saldo-dashboards", style={}),
                            ], style={"padding-left": "20px", "padding-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa-bolt", style=card_icon), 
                                color="warning",
                                style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                            )])
                    ], width=4),

            # Receita
            dbc.Col([
                    dbc.CardGroup([
                            dbc.Card([
                                    html.Legend("Média de Consumo"),
                                    html.H5("Gastando: " + str(media) + "W/s", id="p-receita-dashboards"),
                            ], style={"padding-left": "20px", "padding-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa-line-chart ", style=card_icon), 
                                color="success",
                                style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                            )])
                    ], width=4),

            # Despesa
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend("Estimativa de Custo:"),
                        html.H5("R$: -" + str(estimativa), id="p-despesa-dashboards"),
                    ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(className="fa fa-usd", style=card_icon), 
                        color="danger",
                        style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                    )])
                ], width=4),
        ], style={"margin": "10px"}),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                        # html.Legend("Filtrar Análise", className="card-title"),
                        # html.Label("Categorias das receitas"),
                        # html.Div(
                        #     dcc.Dropdown(
                        #     id="dropdown-receita",
                        #     clearable=False,
                        #     style={"width": "100%"},
                        #     persistence=True,
                        #     persistence_type="session",
                        #     multi=True)                       
                        # ),
                        html.Legend("Período de Análise", style={"margin-top": "10px","text-align":"center"}),
                        dcc.DatePickerRange(
                            month_format='Do MMM, YY',
                            end_date_placeholder_text='Data...',
                            start_date=datetime.today() - timedelta(days=31),
                            end_date=datetime.today() + timedelta(days=31),
                            with_portal=True,
                            updatemode='singledate',
                            id='date-picker-config',
                            style={'z-index': '100',"align-self":"center"}),
                            
                        html.Button("Atualizar",
                            id="button-atualizar",
                            style={"width":"40%","align-self":"center",}
                        ), 
                            ],
                style={"height": "100%", "padding": "20px","gap":"15px"}),
                 

            ], width=12)
    ]),
    dbc.Col(dbc.Card(dcc.Graph(id="graph1"), style={"height": "100%", "padding": "10px"}), width=12),
        ], style={"margin": "10px","align-self":"center"})



# =========  Callbacks  =========== #
# Dropdown Receita
@app.callback([Output("dropdown-receita", "options"),
    Output("dropdown-receita", "value"),
    Output("p-receita-dashboards", "children")],
    Input("store-receitas", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    return [([{"label": x, "value": x} for x in df.Categoria.unique()]), val, f"R$ {valor}"]

# Dropdown Despesa
@app.callback([Output("dropdown-despesa", "options"),
    Output("button-atualizar", "value"),
    Output("p-despesa-dashboards", "children")],
    Input("store-despesas", "[data]"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    return [([{"label": x, "value": x} for x in df.Categoria.unique()]), val, f"R$ {valor}"]


    
# Gráfico 1

@app.callback(
    Output('graph1', 'figure'),
    [Input('date-picker-config', 'start_date'),
    Input('date-picker-config', 'end_date'), 
    Input(ThemeChangerAIO.ids.radio("theme"), "value")])
def update_output( start_date, end_date,theme):
    df_sqlframe = pd.DataFrame(sqlframe).sort_values(by='momento', ascending=True)
    print(start_date,end_date)
    mask = (df_sqlframe['momento'] > start_date) & (df_sqlframe['momento'] <= end_date) 
    print(mask)
    df_sqlframe = df_sqlframe.loc[mask]
    print(df_sqlframe)
  

    df_sqlframe = df_sqlframe.set_index('momento')[['consumo']]
    fig = go.Figure()
    
    # fig.add_trace(go.Scatter(name='Despesas', x=df_ds['Data'], y=df_ds['Acumulo'], fill='tonexty', mode='lines'))
    fig.add_trace(go.Scatter(name='Receitas', x=df_sqlframe.index, y=df_sqlframe['consumo'], mode='lines'))
    # fig.add_trace(go.Scatter(name='Saldo Mensal', x=df_saldo_mes['Mes'], y=df_saldo_mes['Acumulado'], mode='lines'))

    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig
