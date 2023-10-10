import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from tvshows import  donut, sunburst,bar

app = dash.Dash(__name__)

app.layout = html.Div([
    
    html.Div(
        html.H1("EDA TV SHOWS"),
        style={'text-align': 'center'}
    ),    
    
    html.Hr(),
    # Primer cuadrante (arriba a la izquierda)
    html.Div([
        html.H2("Distribution of tv shows on the plattforms"),
        dcc.Graph(
            id='donut-graph',
            figure=donut(),
            style={'width': '100%', 'height': '50vh'}
        )
    ], style={'grid-row': '1 / 2', 'grid-column': '1 / 2'}),
    
    # Segundo cuadrante (arriba a la derecha)
    html.Div([
        html.H2("Genre of the top 10 stv shows "),
        dcc.Dropdown(
            id='dropdown',
            options=['Netflix','Prime Video', 'HBO','Disney+'],
            value='Netflix',
            style={'width': '100%'}
        ),
        dcc.Graph(
            id='bar-graph',
            style={'width': '100%', 'height': '50vh'}
        )
    ], style={'grid-row': '1 / 2', 'grid-column': '2 / 3'}),
    
    # Tercer cuadrante (abajo a la izquierda)
    html.Div([
        html.H2("Language of tv shows"),
        dcc.Dropdown(
            id='dropdown2',
            options=['Netflix','Prime Video', 'HBO','Disney+'],
            value='Netflix',
            style={'width': '100%'}
        ),
        dcc.Graph(
            id='graph2',
            style={'width': '100%', 'height': '50vh'}
        )
    ], style={'grid-row': '2 / 3', 'grid-column': '1 / 2'}),
    
    # Cuarto cuadrante (abajo a la derecha)
    html.Div(id='resultado', style={'grid-row': '2 / 3', 'grid-column': '2 / 3'})
], style={'display': 'grid', 'grid-template-rows': '1fr 1fr', 'grid-template-columns': '1fr 1fr', 'gap': '10px'})
@app.callback(
    Output('bar-graph', 'figure'),
    Input('dropdown', 'value')
)
def actualizar_grafico(value):
    return sunburst(value)

@app.callback(
    Output('graph2', 'figure'),
    Input('dropdown2', 'value')
)
def actualizar_grafico2(value):
    return bar(value)

if __name__ == '__main__':
    app.run_server(debug=True)
