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
            dbc.Col([
              html.H3("Dashboard de Consumo de Energia"),
              html.H5("Dados atuais e sendo exibidos em Tempo Real, referente ao plano de energia, consumo e custo.", style={"margin-top":"15px","margin-bottom":"30px"})
            ], width=12, style={"text-align":"center"}),
            dbc.Col([
                    dbc.CardGroup([
                            dbc.Card([
                                    html.Legend("Plano de Energia"),
                                    html.H5("Atual: " + plano, id="p-saldo-dashboards", style={}),
                            ], style={"padding-left": "20px", "padding-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa-bolt", style=card_icon), 
                                color="warning",
                                style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                            )])
                    ], width=4),

            dbc.Col([
                    dbc.CardGroup([
                            dbc.Card([
                                    html.Legend("Média de Consumo Agência"),
                                    html.H5("Gastando: " + str(media) + "W/s", id="p-receita-dashboards"),
                            ], style={"padding-left": "20px", "padding-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa-line-chart ", style=card_icon), 
                                color="success",
                                style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                            )])
                    ], width=4),

            # Custo
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
                            ],
                style={"height": "100%", "padding": "20px","gap":"15px"}),
                 

            ], width=12)
    ]),
    dbc.Col(dbc.Card(dcc.Graph(id="graph1"), 
    style={"height": "100%", "padding": "10px"}), width=12),
         dcc.Interval(
            id='interval-component',
            interval=30000,
            n_intervals=0
        )
        ], style={"margin": "10px","align-self":"center"})



# =========  Callbacks  =========== #
    
# Gráfico 1

@app.callback(
    Output('graph1', 'figure'),
    [Input('date-picker-config', 'start_date'),
    Input('date-picker-config', 'end_date'),
    Input('interval-component', 'n_intervals'), 
    Input(ThemeChangerAIO.ids.radio("theme"), "value")])
def update_output( start_date, end_date,n_clicks,theme):
    sql = "select * from dadoEnergia where fkCaixa = 1 and consumo <> 0;"
    sqlframe = pd.read_sql(sql,conn)
    sqlframe["momento"] = pd.to_datetime(sqlframe["momento"])
    df_sqlframe = pd.DataFrame(sqlframe).sort_values(by='momento', ascending=True)
    
    mask = (df_sqlframe['momento'] > start_date) & (df_sqlframe['momento'] <= end_date) 
    df_sqlframe = df_sqlframe.loc[mask]
  

    df_sqlframe = df_sqlframe.set_index('momento')[['consumo']]
    fig = go.Figure()
    
    # fig.add_trace(go.Scatter(name='Despesas', x=df_ds['Data'], y=df_ds['Acumulo'], fill='tonexty', mode='lines'))
    fig.add_trace(go.Scatter(name='Receitas', x=df_sqlframe.index, y=df_sqlframe['consumo'], mode='lines'))
    # fig.add_trace(go.Scatter(name='Saldo Mensal', x=df_saldo_mes['Mes'], y=df_saldo_mes['Acumulado'], mode='lines'))

    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig
