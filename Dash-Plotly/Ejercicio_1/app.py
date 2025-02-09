import pandas as pd
import plotly.express as px  
from dash import Dash, dcc, html, Input, Output 
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv("intro_bees.csv")

app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(dbc.Card(html.P("A"),style={'height':'50vh'}),width=6,className='g-0'),
            dbc.Col([
                dbc.Row(dbc.Card(html.P("B")),style={'height':'25vh'}),
                dbc.Row(dbc.Card(html.P("C")),style={'height':'25vh'})
            ],width=6,style={'height':'50vh'})
        ],style={'height':'50vh'}),

        dbc.Row(dbc.Card(html.P("D")),style={'height':'50vh'})
    ],style={'height':'100vh','width':'100vw'},className='h-100',fluid=True
)


# @app.callback([
#     Output(component_id='output_container',component_property='children'),
#     Output(component_id='my_bee_hist',component_property='figure')
#     ],
#     Input(component_id='slct_yeaar',component_property='value'))
# def update_graph(option):
#     print(option)
#     print(type(option))
#     container="Selected Year: "+str(option)
#     dff = df.copy()
#     dff = dff[dff["Year"] == option]  # Descomentar si necesitas filtrar por año
#     dff = dff.groupby("Affected by", as_index=False)['Pct of Colonies Impacted'].mean()

#     # Usar un gráfico de barras en lugar de histograma
#     fig = px.bar(data_frame=dff, x='Affected by', y='Pct of Colonies Impacted', 
#                 title="Impacto por tipo de afectación", labels={'Affected by': 'Causa', 'Pct of Colonies Impacted': 'Porcentaje promedio afectado'})

#     return container, fig

#------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
