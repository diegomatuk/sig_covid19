import dash
import dash_core_components as dcc
import dash_html_components as html
import time
from collections import deque
import plotly.graph_objs as go
import random
from dash.dependencies import Input, Output , State

from objects.rutas import Rutas


external_css = ["https://codepen.io/amyoshino/pen/jzXypZ.css"]

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']


app = dash.Dash('proyecto-sig', external_scripts = external_js, external_stylesheets = external_css)


app.layout = html.Div([

    #TITLE ROW (FIRST BLOCK)
    html.Div(
        [
        html.H2(
            'COVID19 - SIG',
            style = {'font-family': 'Times',
                       "margin-left": "20",
                       "margin-bottom": "0"},
                className='eight columns',
                )
        ], className = 'row'

        ),

    #INPUTS BLOCK
    html.Div([
        dcc.Input(id = 'cliente-afectado',type = 'text',placeholder = '',value = ''),
        dcc.Input(id = 'numero_rutas', type = 'number',placeholder = '', value = ''),
        html.Button('Calcular',id = 'submit-val',n_clicks = 0)

        ]),
    #SEGUNDO BLOQUE
    html.Div([

    html.Iframe(id = 'mapa1', srcDoc = open('mapa1.html','r').read(),width = '32%', height = '600',style = {'margin':'4px'}),
    html.Iframe(id = 'mapa2', srcDoc = open('mapa2.html','r').read(),width = '32%', height = '600',style = {'margin':'4px'}),
    html.Iframe(id = 'mapa3', srcDoc = open('mapa_interseccion.html','r').read(),width = '32%', height = '600',style = {'margin':'4px'})],

    style = {
            'margin-top': 20, 'border':
            '1px solid #C6CCD5', 'padding': 15,
            'border-radius': '5px'

            })

    ])



@app.callback(
    [Output('mapa1' ,'srcDoc'),
    Output('mapa2' ,'srcDoc'),
    Output('mapa3' ,'srcDoc')],
    [Input('submit-val','n_clicks')],
    [State('numero_rutas','value'),
    State('cliente-afectado','value')]

)
def calculo(numero_rutas,cliente_afectado,n_clicks):
    ruta = Rutas()
    ruta.main(num_puntos = 5,nombre_ruta = 'ruta1',n_clicks = n_clicks)
    return open('mapa1.html','r').read(), open('mapa2.html').read(),  open('mapa_interseccion.html').read()


if __name__ == '__main__':
    app.run_server(debug = True)


# @app.callback(
#     dash.dependencies.Output('graphs','children'),
#     [dash.dependencies.Input('vehicle-data-name', 'value')],
#     )
#
# def update_graph(data_names):
#     graphs = []
#     update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos)
#
#     if len(data_names)>2:
#         class_choice = 'col s12 m6 l4'
#     elif len(data_names) == 2:
#         class_choice = 'col s12 m6 l6'
#     else:
#         class_choice = 'col s12'
#
#
#     for data_name in data_names:
#
#         data = go.Scatter(
#             x=list(times),
#             y=list(data_dict[data_name]),
#             name='Scatter',
#             fill="tozeroy",
#             fillcolor="#6897bb"
#             )
#
#         graphs.append(html.Div(dcc.Graph(
#             id=data_name,
#             animate=True,
#             figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
#                                                         yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
#                                                         margin={'l':50,'r':10,'t':45,'b':10},
#                                                         title='{}'.format(data_name))}
#             ), className=class_choice))
#     return graphs










#
# dcc.Dropdown(id='vehicle-data-name',
#              options=[{'label': s, 'value': s}
#                       for s in data_dict.keys()],
#              value=['Coolant Temperature','Oil Temperature','Intake Temperature'],
#              multi=True
#              ),
# html.Div(children=html.Div(id='graphs'), className='row'),
# dcc.Interval(
#     id='graph-update',
#     interval=100),
