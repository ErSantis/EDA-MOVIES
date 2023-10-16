#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import plotly.express as px
import pycountry


# ### Connect to Database

# In[5]:


try:
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-FMPUJNUK\SQLEXPRESS;DATABASE=Movies;UID=sa;PWD=123456')
    print('Conexion exitosa')
except Exception as ex:
    print(ex)


# ### Graph of the distribution

# In[6]:


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


# In[7]:


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


# ### Graph of votes

# In[8]:


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
    


# In[9]:


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


# In[10]:


# ### Graph of language

# In[27]:


from iso639 import Lang
Lang('es').name


# In[28]:


def splitting(dataframe,col):
    result = dataframe[col].str.get_dummies(',')
    print('Done!')
    return result


# In[29]:


def rename(df):
    nuevos_nombres = {}

    for i in df.columns:
        try:
            nuevo_nombre = Lang(i.strip()).name
            nuevos_nombres[i] = nuevo_nombre
        except Exception as e:
            nuevos_nombres[i] = i  

    return df.rename(columns=nuevos_nombres)


# In[30]:


def lan_count(value):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT D.name ,D.languages FROM movies as D WHERE D.networks like" + f'\'%{value}%\' and D.languages is not null')
        rows= cursor.fetchall()
        return rows
    except Exception as ex:
        print(ex)


# In[31]:


def create_df(value):
    df = pd.DataFrame()
    net = lan_count(value)
    df['name'] = [item[0] for item in net]
    df['lan'] = [item[1] for item in net]
    m_lang  = splitting(df,'lan')
    df_l_merged = pd.concat([df, m_lang], axis = 1, sort = False)
    df_l_merged = rename(df_l_merged)
    return df_l_merged


# In[54]:


def bar(value):
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

def map(value):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT D.id , D.origin_country, D.vote_count FROM movies as D WHERE D.networks like" + f'\'%{value}%\' and D.origin_country is not null')
        rows= cursor.fetchall()
        return rows
    except Exception as ex:
        print(ex)


def create_df_map(value):
    df = pd.DataFrame()
    net = map(value)
    df['name'] = [item[0] for item in net]
    df['country'] = [item[1] for item in net]
    df['votes'] = [item[2] for item in net]
    df_expand = df.assign(country=df['country'].str.split(',')).explode('country')
    df_country_rating = df_expand.groupby('country')['votes'].mean().reset_index()
    return df_country_rating

def get_country_name(alpha_2):
    try:
        country = pycountry.countries.get(alpha_2=alpha_2.strip())
        if country:
            return country.name
        else:
            return None
    except Exception as e:
        return None

def plot_map(value):
    df_country_rating = create_df_map(value)
    df_country_rating['country'] = df_country_rating['country'].apply(get_country_name)
    fig = px.scatter_geo(df_country_rating, locations='country', locationmode='country names', color='votes',
                        title=f'Average Rating by Country for {value} Shows', scope='world',size='votes', height=650)

    return fig    

def get(value):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT m.status, COUNT(*) Cant FROM movies as m WHERE m.networks like" + f'\'%{value}%\'  group by m.status')
        rows= cursor.fetchall()
        return rows
    except Exception as ex:
        print(ex)

def get_df():
    plat = {'Platform':['Netflix', 'Prime video', 'HBO', 'Disney+','BBC One', 'YouTube','NBC','FOX','Discovery','MTV']}
    df = pd.DataFrame(plat)
    for index, row in df.iterrows():
        x = get(row['Platform'])
        for i in x:
            df.loc[index, f'{i[0]}'] = i[1]
    return df
def histo(df,col_chosen):
    fig = px.histogram(df, x='Platform', y=col_chosen)
    return fig