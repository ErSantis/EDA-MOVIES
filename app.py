import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from tvshows import donut, sunburst, bar, plot_map

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Estilos de CSS con una paleta de colores oscuros diferentes
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Aplicar los estilos CSS
app.css.append_css({"external_url": external_stylesheets})

# Estilo global de la página
app.layout = html.Div([
    # Encabezado
    html.Div([
        html.H1("EDA TV SHOWS AND SERIES", style={'textAlign': 'center', 'color': 'white'}),
    ], style={'backgroundColor': '#1C2833', 'padding': '20px'}),

    # Fila 1: Gráfico de género de los 10 mejores programas de televisión
    html.Div([
        html.H2("Genre of the top 10 TV Shows", style={'color': 'white'}),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': platform, 'value': platform} for platform in ['Netflix', 'Prime Video', 'HBO', 'Disney+', 'BBC One', 'YouTube']],
            value='Netflix',
            style={'width': '100%'}
        ),
        dcc.Graph(
            id='bar-graph',
            style={'width': '100%'}
        )
    ], style={'backgroundColor': '#39424E', 'padding': '20px', 'border-radius': '5px'}),

    # Fila 2: Gráfico de distribución de programas en plataformas
    html.Div([
        html.H2("Distribution of TV Shows on Platforms", style={'color': 'white'}),
        dcc.Graph(
            id='donut-graph',
            figure=donut(),
            style={'width': '100%'}
        )
    ], style={'backgroundColor': '#1F4068', 'padding': '20px', 'border-radius': '5px'}),

    # Fila 3: Gráfico de idioma de programas de televisión
    html.Div([
        html.H2("Language of TV Shows", style={'color': 'white'}),
        dcc.Dropdown(
            id='dropdown2',
            options=[{'label': platform, 'value': platform} for platform in ['Netflix', 'Prime Video', 'HBO', 'Disney+', 'BBC One', 'YouTube']],
            value='Netflix',
            style={'width': '100%'}
        ),
        dcc.Graph(
            id='graph2',
            style={'width': '100%'}
        )
    ], style={'backgroundColor': '#485460', 'padding': '20px', 'border-radius': '5px'}),

    # Fila 4: Mapa de calificación por país
    html.Div([
        html.H2("Rating Map by Country", style={'color': 'white'}),
        dcc.Dropdown(
            id='dropdown3',
            options=[{'label': platform, 'value': platform} for platform in ['Netflix', 'Prime Video', 'HBO', 'Disney+', 'BBC One', 'YouTube']],
            value='Netflix',
            style={'width': '100%'}
        ),
        dcc.Graph(
            id='map-graph',
            style={'width': '100%'}
        )
    ], style={'backgroundColor': '#293241', 'padding': '20px', 'border-radius': '5px'}),
])

# Definir funciones de devolución de llamada
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

@app.callback(
    Output('map-graph', 'figure'),
    Input('dropdown3', 'value')
)
def actualizar_grafico3(value):
    return plot_map(value)

if __name__ == '__main__':
    app.run_server(debug=True)
