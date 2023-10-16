import dash
from dash import dash_table,dcc,html
from dash.dependencies import Input, Output
from tvshows import donut, sunburst, bar, plot_map, get_df, histo

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap"
]
df = get_df()
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

    #Titulo
    html.Div([
        html.H1("Exploratory Data Analysis on TV Shows", className='custom-font-lilita', style={'textAlign': 'center', 'color': 'white'}),
    ], style={'backgroundColor': '#39B6A9', 'padding': '20px', 'text-align': 'center'}),


    html.Div([
    
        html.Div([
        
            html.H2("Genre of the top TV Shows", className='custom-font-lilita', style={'color': 'white', 'text-align': 'center'}),

            # Div para el campo "Top" y dropdown
            html.Div([
                html.Label("Top", className='custom-font-lilita', style={'color': 'white', 'padding': '10px', 'text-align': 'right'}),
                dcc.Input(
                    id='top-n-dropdown',
                    type='number',
                    min=1,
                    max=10,
                    value=10,
                    style={'width': '30px','font-family': 'Nunito'}
                )
            ], style={'position':'absolute','z-index':'2','top':'0','right':'5px'}),
        ], style={ 'justify-content': 'space-between', 'text-align': 'center', 'align-items': 'center','position':'relative'}),
        

        dcc.Dropdown(
            id='dropdown',
            options=[{'label': platform, 'value': platform} for platform in ['Netflix', 'Prime Video', 'HBO', 'Disney+', 'BBC One', 'YouTube']],
            value='Netflix',
            style={'width': '100%','font-family': 'Nunito','font-size':'18'}
        ),

        # Gráfico
        dcc.Graph(
            id='sunburst-graph',
            style={'width': '100%', 'height': '100%'}
        )
        ], style={**div_style, 'border-radius': '5px', 'backgroundColor': '#007266', 'text-align': 'center'}),
    
    # Div para la gráfica de distribución de TV Shows en plataformas
    html.Div([
        html.H2("Distribution of TV Shows on Platforms", className='custom-font-lilita', style={'color': 'white'}),
        dcc.Graph(
            id='donut-graph',
            figure=donut(),
            style={'width': '100%','height': '100%'}
        )
    ], style={**div_style, 'backgroundColor': '#007266', 'border-radius': '5px', 'text-align': 'center'}),

    # Div para la gráfica de idioma de TV Shows
    html.Div([
        html.H2("Language of TV Shows", className='custom-font-lilita', style={'color': 'white'}),
        dcc.Dropdown(
            id='dropdown2',
            options=[{'label': platform, 'value': platform} for platform in ['Netflix', 'Prime Video', 'HBO', 'Disney+', 'BBC One', 'YouTube']],
            value='Netflix',
            style={'width': '100%','font-family': 'Nunito','font-size':'18'}
        ),
        dcc.Graph(
            id='bar-graph',
            figure = bar('Netflix'),
            style={'width': '100%'}
        )
    ], style={**div_style, 'backgroundColor': '#007266', 'border-radius': '5px', 'text-align': 'center'}),

    # Div para la gráfica de rating por país
    html.Div([
        html.H2("Rating Map by Country", className='custom-font-lilita', style={'color': 'white'}),
        dcc.Dropdown(
            id='dropdown3',
            options=[{'label': platform, 'value': platform} for platform in ['Netflix', 'Prime Video', 'HBO', 'Disney+', 'BBC One', 'YouTube']],
            value='Netflix',
            style={'width': '100%','font-family': 'Nunito','font-size':'18'}
        ),
        dcc.Graph(
            id='map-graph',
            figure = plot_map('Netflix'),
            style={'width': '100%'}
        )
    ], style={**div_style, 'backgroundColor': '#007266', 'border-radius': '5px', 'text-align': 'center'}),

  #Tabla
    html.Div([
        html.H2("Series Status", className='custom-font-lilita', style={'color': 'white'}),
        
    ], style={'backgroundColor': '#007266', 'border-radius': '5px', 'text-align': 'center', 'width': '100%'}),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=get_df().to_dict('records'), page_size=11, style_table={'overflowX': 'auto'},
                                style_cell={'font-family': 'Nunito', 'font-size': '24px','text-align':'center'})
        ]),
        html.Div([
            dcc.RadioItems(
            options=[
                {'label': 'Planned', 'value': 'Planned'},
                {'label': 'In Production', 'value': 'In Production'},
                {'label': 'Returning Series', 'value': 'Returning Series'},
                {'label': 'Canceled', 'value': 'Canceled'},
                {'label': 'Ended', 'value': 'Ended'},
                {'label': 'Pilot', 'value': 'Pilot'}
            ],
            value='Ended',
            inline=True,
            id='radio-buttons',
            style={'color': 'white' },
            labelStyle={'font-size': '20px'},
            className='custom-font-lilita'
            )
        ], style={'backgroundColor': '#007266', 'border-radius': '5px', 'text-align': 'center', 'width': '100%', 'padding-bottom': '5px'}),
        html.Div(className='six columns', children=[
            dcc.Graph(figure=histo(df,'Ended'), id='histo')
        ])
    ]),
    
    
    html.Hr(),

    # Footer
    html.Footer([
        # Columna izquierda
        html.Div([
            html.Img(src='/assets/dash-logo-new.png', alt='Imagen 1', style={'width': 'auto', 'height': '40px', 'margin-bottom': '10px', 'margin-right' : '20px'}),
            html.Img(src='https://static-00.iconduck.com/assets.00/kaggle-icon-2048x796-qhhbb3dh.png', alt='Imagen 2', style={'width': 'auto', 'height': '40px'})
        ], style={'display': 'flex', 'align-items': 'center', 'float': 'left'}),

        # Columna central
        html.Div([
            html.P("© 2023 Linero, Santis y Vergara. Todos los derechos reservados.", className='custom-input-quicksand', style={'border-color': '#39B6A9'}),  # Copyright
            html.P("Base de datos recuperada de Kaggle: ", className='custom-input-quicksand', style={'display': 'inline', 'border-color': '#39B6A9'}),
            dcc.Link("Clic Aquí", className='custom-input-quicksand', href='https://www.kaggle.com/datasets/asaniczka/full-tmdb-tv-shows-dataset-2023-150k-shows',
                    style={'text-decoration': 'underline', 'color': 'blue', 'border-color': '#39B6A9'})
        ], style={'flex': 1, 'text-align': 'center', 'margin-left': '15%'}),

        # Columna derecha
        html.Div([
            html.P("Enlace al repositorio", className='custom-input-quicksand', style={'border-color': '#39B6A9'}),
            html.A(
                html.Img(src='/assets/GitHub-Emblem.png', alt='Enlace al repositorio de GitHub', style={'width': 'auto', 'height': '50px', 'margin-right': '10px'}),
                href='https://github.com/ErSantis/EDA-MOVIES' #Para acceder al repositorio
            )
        ], style={'flex': 1, 'display': 'flex', 'justify-content': 'flex-end', 'align-items': 'center', 'float': 'right', 'margin-left': '20px'})
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'backgroundColor': '#39B6A9', 'padding': '20px'})
], style={'backgroundColor': '#39B6A9'})


@app.callback(
    Output('sunburst-graph', 'figure'),
    Input('top-n-dropdown', 'value'),
    Input('dropdown', 'value')
)
def actualizar_grafico(valor_n_dropdown, valor_dropdown):
    return sunburst(valor_n_dropdown, valor_dropdown)

initial = 'Netflix'
@app.callback(
    Output('bar-graph', 'figure'),
    Input('dropdown2', 'value')
)
def actualizar_grafico2(valor_dropdown):
    return bar(valor_dropdown)

@app.callback(
    Output('map-graph', 'figure'),
    Input('dropdown3', 'value')
)
def actualizar_grafico3(value):
    return plot_map(value)

@app.callback(
    Output('histo', 'figure'),
    Input('radio-buttons', 'value')
)

def update_graph(col_chosen):
    return histo(df,col_chosen)

if __name__ == '__main__':
    app.run_server(debug=True)
