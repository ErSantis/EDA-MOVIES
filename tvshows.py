#-------Imports----------#

import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import plotly.express as px
import pycountry
from iso639 import Lang


#---------Connect to Database--------

try:
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-FMPUJNUK\SQLEXPRESS;DATABASE=Movies;UID=sa;PWD=123456')
    print('Conexion exitosa')
except Exception as ex:
    print(ex)


#-------Graph 1: Graph of the distribution--------#

#Make the Query to the DB
def values_count(value):
    """
    The function `values_count` retrieves the count of movies from a database table where the networks
    column contains a specific value.
    
    :param value: The `value` parameter is a string that represents a value to search for in the
    `networks` column of a table called `movies`
    :return: the count of rows in the "movies" table where the "networks" column contains the specified
    value.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(("SELECT Count(*) FROM movies as D WHERE D.networks like" + f'\'%{value}%\''))
        rows= cursor.fetchall()
        return rows[0][0]
    except Exception as ex:
        print(ex)


#Plot the graph 2
def donut():
    """
    The `donut` function creates a donut chart using the `plotly` library to visualize the sizes of
    different streaming services.
    :return: a pie chart figure object.
    """
    labels = ['Netflix', 'Prime video', 'HBO', 'Disney+','BBC One', 'YouTube','NBC','FOX','Discovery','MTV']
    colors = ["#ff6b6b", "#EDE603", "#6C15B9", "#72efdd","#003880", "#D8047E","#DC3A0E","#0E1EDC","#0EDC30","#0E94DC"]
    sizes = []
    for net in labels:
        sizes.append(values_count(net))
    fig =  px.pie(
        values=sizes,
        names=labels,
        hole=0.5,
        color_discrete_sequence=colors,
        labels={'names': 'Streaming Service'}
    )
    fig.update_layout(
        paper_bgcolor='#ffffff',
        height=896
        #height=740  # Cambia el fondo a azul
    )
    fig.update_traces(textinfo='percent+label')
    return fig


#-------- Graph 1: Graph of votes ---------#

#Make the Query to the DB
def vote_count(value): 
    """
    The function `vote_count` retrieves the name, genres, and vote count of movies from a database table
    called "movies" that match a given network value and have a non-zero vote count, ordered by vote
    count in descending order.
    
    :param value: The `value` parameter is a string that represents the network name. The function
    retrieves the name, genres, and vote count of movies from a database table called "movies" where the
    network name matches the provided value. The movies are sorted in descending order based on their
    vote count
    :return: the rows from the database that match the given value and have a non-zero vote count,
    sorted in descending order by vote count.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT D.name ,D.genres, D.vote_count FROM movies as D WHERE D.networks like" + f'\'%{value}%\' and D.vote_count !=0 order by D.vote_count DESC')
        rows= cursor.fetchall()
        return rows
    except Exception as ex:
        print(ex)
    

#Plot the graph 1
def sunburst(val1, net):
    """
    The `sunburst` function takes in a value and a network, and returns a sunburst plot based on the
    data in the network.
    
    :param val1: The parameter `val1` is the number of rows you want to include in the sunburst chart.
    It determines how many data points will be displayed in the chart
    :param net: The `net` parameter is a list of tuples containing information about different streaming
    platforms. Each tuple contains the name of the platform, its genre, and the number of votes it has
    received
    :return: a Plotly sunburst chart object.
    """
    c = net
    df = pd.DataFrame()
    net = vote_count(net)
    x = {'Netflix': 'amp', 'Prime Video': 'blugrn', 'HBO': 'haline', 'Disney+': 'dense', 'BBC One': 'amp', 'YouTube': 'teal'}
    df['name'] = [item[0] for item in net]
    df['genres'] = [item[1] for item in net]
    df['Votes'] = [item[2] for item in net]
    min_vote_count = df['Votes'].min()
    max_vote_count = df['Votes'].max()
    df['votes_average'] = 10 * (df['Votes'] - min_vote_count) / (max_vote_count - min_vote_count)
    fig =px.sunburst(
    df[0:val1],
    path=['name','genres'],
    values='votes_average',
    color='votes_average',
    color_continuous_scale=x[c],
    )
    fig.update_layout(
        paper_bgcolor='#ffffff',
        height=862,
        title_font=dict(family='Arial', size=18),
        font_family='Times New Roman',
        font_size = 18
    )
     # Configura el rango inicial de zoom
    fig.update_xaxes(range=[0, 1])  # Ajusta el rango del eje X
    fig.update_yaxes(range=[0, 1])  # Ajusta el rango del eje Y

    return fig

#----------- Graph 3: Language of the tv shows ------#

#Split the column
def splitting(dataframe,col):
    """
    The function "splitting" takes a dataframe and a column name as input, and returns a new dataframe
    where the values in the specified column are split into separate columns using comma as the
    delimiter.
    
    :param dataframe: The dataframe parameter is the pandas DataFrame that you want to split
    :param col: The "col" parameter is the name of the column in the dataframe that you want to split
    :return: a dataframe that contains the dummy variables created from splitting the values in the
    specified column of the input dataframe.
    """
    result = dataframe[col].str.get_dummies(',')
    print('Done!')
    return result


#Rename a dataframe
def rename(df):
    """
    The function `rename` takes a DataFrame as input and renames its columns using a language library,
    returning the modified DataFrame.
    
    :param df: The parameter `df` is a pandas DataFrame object
    :return: a DataFrame with the columns renamed according to their corresponding language names.
    """
    nuevos_nombres = {}

    for i in df.columns:
        try:
            nuevo_nombre = Lang(i.strip()).name
            nuevos_nombres[i] = nuevo_nombre
        except Exception as e:
            nuevos_nombres[i] = i  

    return df.rename(columns=nuevos_nombres)


#Make the Query
def lan_count(value):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT D.name ,D.languages FROM movies as D WHERE D.networks like" + f'\'%{value}%\' and D.languages is not null')
        rows= cursor.fetchall()
        return rows
    except Exception as ex:
        print(ex)


#Create the dataframe
def create_df(value):
    """
    The function `create_df` creates a DataFrame from a given value, counts the occurrences of each LAN
    in the DataFrame, splits the 'lan' column into multiple columns, merges the new columns with the
    original DataFrame, and renames the columns.
    
    :param value: The `value` parameter is the input value that is passed to the `lan_count` function.
    It is used to calculate the number of languages in a network
    :return: The function `create_df` returns a pandas DataFrame `df_l_merged`.
    """
    df = pd.DataFrame()
    net = lan_count(value)
    df['name'] = [item[0] for item in net]
    df['lan'] = [item[1] for item in net]
    m_lang  = splitting(df,'lan')
    df_l_merged = pd.concat([df, m_lang], axis = 1, sort = False)
    df_l_merged = rename(df_l_merged)
    return df_l_merged


#Plot the graph 3
def bar(value):
    """
    The function `bar` creates a bar chart showing the number of TV shows for the top 20 languages,
    based on a given value.
    
    :param value: The parameter `value` is the language for which you want to create the bar chart. It
    is used to filter the data and calculate the number of TV shows for each language. The bar chart
    will display the top 20 languages by the number of TV shows
    :return: a bar chart (plotly.graph_objects.Figure object) that shows the number of TV shows for the
    top 20 languages. The chart is customized with a specific color for each language based on the input
    value.
    """
    dataframe = create_df(value)
    val_counts = dataframe.iloc[:,15:].sum(axis=0).sort_values(ascending=False)
    val_counts2 = pd.DataFrame(val_counts,columns=['Number of TV Shows'])

    # Crear un DataFrame con los 20 primeros valores
    top_20 = val_counts2[:20]
    
    fig = px.bar(
        top_20,
        x=top_20.index,
        y='Number of TV Shows',
        color=top_20.index,
        title='Languages by Number of TV Shows',
        labels={'Number of TV Shows': 'Number of TV Shows', 'index': 'language'}
    )

    fig.update_layout(
        xaxis_title='Language',
        yaxis_title='Number of TV shows',
        showlegend=False,
        plot_bgcolor='white',
        height=650
    )
    c = {'Netflix':'#ff6b6b',
         'Prime Video':'#00A8E1',
        'HBO':'#800080',
        'Disney+':'#72efdd',
        'BBC One':'#003880',    
        'YouTube':'#D8047E'}
    fig.update_traces(marker_color=c[value])
    return fig


#----------- Graph 4: map of the countries of the tv shows most voted

#Make the Query
def map(value):
    """
    The function `map` retrieves data from a database table called "movies" based on a given value and
    returns the rows that match the criteria.
    
    :param value: The `value` parameter is a string that represents the network name. It is used to
    filter the movies based on the network they are aired on
    :return: the rows fetched from the database query.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT D.id , D.origin_country, D.vote_count FROM movies as D WHERE D.networks like" + f'\'%{value}%\' and D.origin_country is not null')
        rows= cursor.fetchall()
        return rows
    except Exception as ex:
        print(ex)


#Create the dataframe
def create_df_map(value):
    """
    The function `create_df_map` takes a value, creates a DataFrame, maps the value to the DataFrame,
    expands the DataFrame by splitting the 'country' column, groups the DataFrame by country and
    calculates the mean of the 'votes' column, and returns the resulting DataFrame.
    
    :param value: The `value` parameter is expected to be a list of tuples. Each tuple should contain
    three elements: the name of a network, the country where the network is located, and the number of
    votes the network has received
    :return: a DataFrame called `df_country_rating` which contains the average votes for each country in
    the input DataFrame `df`.
    """
    df = pd.DataFrame()
    net = map(value)
    df['name'] = [item[0] for item in net]
    df['country'] = [item[1] for item in net]
    df['votes'] = [item[2] for item in net]
    df_expand = df.assign(country=df['country'].str.split(',')).explode('country')
    df_country_rating = df_expand.groupby('country')['votes'].mean().reset_index()
    return df_country_rating


#Get the name of the country from iso
def get_country_name(alpha_2):
    """
    The function `get_country_name` takes an alpha-2 country code as input and returns the corresponding
    country name using the pycountry library.
    
    :param alpha_2: The parameter "alpha_2" is a two-letter country code
    :return: the name of a country based on its alpha-2 code. If the alpha-2 code is valid and
    corresponds to a country, the function will return the name of that country. If the alpha-2 code is
    invalid or does not correspond to a country, the function will return None.
    """
    try:
        country = pycountry.countries.get(alpha_2=alpha_2.strip())
        if country:
            return country.name
        else:
            return None
    except Exception as e:
        return None


#Plot the graph 4
def plot_map(value):
    """
    The function `plot_map` creates a scatter plot on a world map, showing the average rating by country
    for a given value.
    
    :param value: The `value` parameter is the type of shows for which you want to plot the map. It
    could be any category or genre of shows, such as "comedy", "drama", "action", etc
    """
    df_country_rating = create_df_map(value)
    df_country_rating['country'] = df_country_rating['country'].apply(get_country_name)
    fig = px.scatter_geo(df_country_rating, locations='country', locationmode='country names', color='votes',
                        title=f'Average Rating by Country for {value} Shows', scope='world',size='votes', height=650)

    return fig    



#----------- Graph 5: Graph of the distribution of the status of the tv shows


#Create dataframe with all information about the show (status, votes, runtime...)
def get(value):
    """
    The function retrieves the status and count of movies from a database based on a given value.
    
    :param value: The `value` parameter is a string that represents the network name. It is used to
    filter the movies table based on the networks column. The SQL query retrieves the status and count
    of movies that have the specified network in their networks column. The result is returned as a list
    of tuples, where each
    :return: the result of the SQL query executed on the database. The result is a list of tuples, where
    each tuple contains the status and the count of movies that have the specified value in their
    networks column.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT m.status, COUNT(*) Cant FROM movies as m WHERE m.networks like" + f'\'%{value}%\'  group by m.status')
        rows= cursor.fetchall()
        return rows
    except Exception as ex:
        print(ex)


# Make the dataframe
def get_df():
    """
    The function `get_df` creates a DataFrame with a column for different streaming platforms and
    populates additional columns with data obtained from a function `get`.
    :return: a pandas DataFrame object.
    """
    plat = {'Platform':['Netflix', 'Prime video', 'HBO', 'Disney+','BBC One', 'YouTube','NBC','FOX','Discovery','MTV']}
    df = pd.DataFrame(plat)
    for index, row in df.iterrows():
        x = get(row['Platform'])
        for i in x:
            df.loc[index, f'{i[0]}'] = i[1]
    return df


#plot the histogram
def histo(df,col_chosen):
    """
    The `histo` function creates a histogram plot using the specified column from a given dataframe.
    
    :param df: The parameter "df" is a pandas DataFrame that contains the data you want to plot. It
    should have a column named 'Platform' that represents the x-axis values and a column named
    'col_chosen' that represents the y-axis values
    :param col_chosen: The parameter "col_chosen" is a string that represents the column name in the
    dataframe "df" that you want to plot on the y-axis of the histogram
    :return: The function `histo` returns a histogram plot (figure) created using the `px.histogram`
    function from the Plotly Express library. The histogram is plotted based on the data in the
    DataFrame `df` and the column specified by `col_chosen`.
    """
    fig = px.histogram(df, x='Platform', y=col_chosen)
    return fig