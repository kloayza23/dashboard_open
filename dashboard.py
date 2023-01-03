import pandas as pd
from pymongo import MongoClient
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

mongClient = MongoClient('127.0.0.1', 27017)
db = mongClient.db_iris

setosa_df = pd.DataFrame(list(db.setosa.find()))
versicolor_df = pd.DataFrame(list(db.versicolor.find()))
virginica_df = pd.DataFrame(list(db.virginica.find()))
cant_variedad_df = pd.DataFrame(list(db.cant_variedad.find()))


# ************************** BARRA DE NAVEGACION Y LOGO **************************
logo = '	https://i.pinimg.com/originals/a3/66/f0/a366f0985b6d2750b0242b66fbdef604.png'
navbar = dbc.NavbarSimple(
    brand='Iris Dashboard',
    brand_style={'fontSize': 40, 'color': 'white'},
    children=
    [
        html.A(html.Img(src=logo, width='100',height='40'),
               href='https://archive.ics.uci.edu/ml/datasets/iris',
               target='_blank',
               style={'color': 'black'}
               )
    ],
    color='primary',
    fluid=True,
    sticky='top'
)

pie_variedad_totales = go.Figure(
                    data=[go.Pie(labels=cant_variedad_df.T.index[1:4].tolist(), values=cant_variedad_df.T[0].values[1:4].tolist())],
                    layout= {
                                    "title": "Variedad Iris",
                                    "height": 390,  # px
                                    "width": 390,
                    },
)
drop_vary=dcc.Dropdown(id='drop_vary',options=cant_variedad_df.T.index[1:4].tolist())
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    navbar,
    drop_vary,
    html.Br(),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
            id='vary-tot',
            figure=pie_variedad_totales
            )
        ),
        dbc.Col(
            dash_table.DataTable(id='data-iris'),
        ),
        dbc.Col(dcc.Graph(id='graph-iris'))
    ])
])
@app.callback(
    Output('graph-iris', 'figure'),
    Input('drop_vary', 'value'),
)
def update_chart(drop_vary):
    if drop_vary=='setosa':
        fig_len= px.scatter(setosa_df, x="sepal.length", y="petal.length")
    elif drop_vary=='Versicolor':
        fig_len= px.scatter(versicolor_df, x="sepal.length", y="petal.length")
    elif drop_vary=='Virginica':
        fig_len= px.scatter(virginica_df, x="sepal.length", y="petal.length")
    else:
        fig_len= px.scatter(setosa_df, x="sepal.length", y="petal.length")
    return fig_len

@app.callback(
    Output('data-iris', 'data'),
    Input('drop_vary', 'value'),
)
def update_table(drop_vary):
    if drop_vary=='setosa':
        ta_re=setosa_df.filter(items=['sepal.length','petal.length']).head(5).to_dict('records')
    elif drop_vary=='Versicolor':
        ta_re=versicolor_df.filter(items=['sepal.length','petal.length']).head(5).to_dict('records')
    elif drop_vary=='Virginica':
        ta_re=virginica_df.filter(items=['sepal.length','petal.length']).head(5).to_dict('records')
    else:
        ta_re=setosa_df.filter(items=['sepal.length','petal.length']).head(5).to_dict('records')
    return ta_re
if __name__ == '__main__':
    app.run_server(debug=True)
