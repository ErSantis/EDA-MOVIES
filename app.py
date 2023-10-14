import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from tvshows import donut, sunburst, bar, plot_map

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap"
]

app = dash.Dash(__name__)

# Aplicar los estilos CSS
app.css.append_css({
    'external_url': 'url("assets/styles.css")'
})

app.title = 'EDA: TV SHOWS AND SERIES'

# Estilos CSS para los divs
div_style = {
    'display': 'inline-block',
    'vertical-align': 'top',
    'width': 'calc(50% - 10px)',  # 50% de ancho con 10px de espacio entre los divs
    'margin-right': '10px',
    'margin-bottom': '10px',
    'box-sizing': 'border-box'
}

app.layout = html.Div([
    html.Div([
        html.H1("EDA TV SHOWS AND SERIES", className='custom-font', style={'textAlign': 'center', 'color': 'white'}),
    ], style={'backgroundColor': '#1f8983', 'padding': '20px'}),

    # Div para la gráfica de género de TV Shows
    html.Div([
        html.H2("Genre of the top TV Shows", style={'color': 'white'}),
        html.Div([
            html.Label("Seleccione el top que desea ver", style={'color': 'white', 'padding': '5px'}),
            dcc.Input(
                id='top-n-dropdown',
                type='number',
                min=1,
                max=10,
                value=1,
                style={'width': '69px', 'margin-left': '10px'}
            )
        ], style={'display': 'flex', 'align-items': 'center'}),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': platform, 'value': platform} for platform in ['Netflix', 'Prime Video', 'HBO', 'Disney+', 'BBC One', 'YouTube']],
            value='Netflix',
            style={'width': '110px'}
        ),
        dcc.Graph(
            id='bar-graph',
            style={'width': '150%'}
        )
    ], style={**div_style, 'backgroundColor': '#56bbb4', 'border-radius': '5px'}),

    # Div para la gráfica de distribución de TV Shows en plataformas
    html.Div([
        html.H2("Distribution of TV Shows on Platforms", style={'color': 'white'}),
        dcc.Graph(
            id='donut-graph',
            figure=donut(),
            style={'width': '100%'}
        )
    ], style={**div_style, 'backgroundColor': '#56bbb4', 'border-radius': '5px'}),

    # Div para la gráfica de idioma de TV Shows
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
    ], style={**div_style, 'backgroundColor': '#72d3cc', 'border-radius': '5px'}),

    # Div para la gráfica de rating por país
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
    ], style={**div_style, 'backgroundColor': '#8dece4', 'border-radius': '5px'}),

    html.Hr(),

    # Footer
    html.Footer([
        html.Div([
            html.Img(src='/assets/dash-logo-new.png', alt='Imagen 1', style={'width': '130px', 'height': 'auto'}),
            html.Img(src='/assets/plotly_logo.png', alt='Imagen 2', style={'width': '130px', 'height': 'auto'})
        ], style={'float': 'left', 'width': '150px'}),

        html.Div([
            html.P("© 2023 Linero, Santis y Vergara. Todos los derechos reservados."),
            html.P("Base de datos recuperada de Kaggle: ", style={'display': 'inline'}),
            dcc.Link("Clic Aquí", href='https://www.kaggle.com/datasets/asaniczka/full-tmdb-tv-shows-dataset-2023-150k-shows', style={'text-decoration': 'underline', 'color': 'blue'})
        ], style={'text-align': 'center'}),

        html.Div([
            html.P("Enlace al repositorio:", style={'text-align': 'center'}),
            html.A(
                html.Img(src='/assets/GitHub-Emblem.png', alt='Enlace al repositorio de GitHub', style={'width': '130px', 'height': 'auto'}),
                href='https://github.com/ErSantis/EDA-MOVIES'
            )
        ], style={'float': 'right'})
    ])
])

@app.callback(
    Output('bar-graph', 'figure'),
    Input('top-n-dropdown', 'value'),
    Input('dropdown', 'value')
)
def actualizar_grafico(valor_n_dropdown, valor_dropdown):
    return sunburst(valor_n_dropdown, valor_dropdown)

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
