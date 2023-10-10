#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler


# ### Connect to Database

# In[5]:


try:
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-FMPUJNUK\SQLEXPRESS;DATABASE=Prueba;UID=sa;PWD=123456')
    print('Conexion exitosa')
except Exception as ex:
    print(ex)


# ### Graph of the distribution

# In[6]:


def values_count(value):
    try:
        cursor = connection.cursor()
        cursor.execute(("SELECT Count(*) FROM data2 as D WHERE D.networks like" + f'\'%{value}%\''))
        rows= cursor.fetchall()
        return rows[0][0]
    except Exception as ex:
        print(ex)


# In[7]:


def donut():
    labels = ['Netflix', 'Prime video', 'HBO', 'Disney+']
    colors = ["#ff6b6b", "#95d5b2", "#a2d2ff", "#72efdd"]
    sizes = []
    for net in labels:
        sizes.append(values_count(net))
    fig =  px.pie(
        values=sizes,
        names=labels,
        title='TV SHOWS',
        hole=0.5,
        color_discrete_sequence=colors,
        labels={'names': 'Streaming Service'}
    )

    fig.update_traces(textinfo='percent+label')
    return fig


# ### Graph of votes

# In[8]:


def vote_count(value):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT D.name ,D.genres, D.vote_count FROM data2 as D WHERE D.networks like" + f'\'%{value}%\' and D.vote_count !=0 order by D.vote_count DESC')
        rows= cursor.fetchall()
        return rows
    except Exception as ex:
        print(ex)
    


# In[9]:


def sunburst(net):
    
    c = net
    df = pd.DataFrame()
    net = vote_count(net)
    x = {'Netflix':'amp','Prime Video':'blugrn','HBO':'haline','Disney+':'dense'}
    df['name'] = [item[0] for item in net]
    df['genres'] = [item[1] for item in net]
    df['Votes'] = [item[2] for item in net]
    fig =px.sunburst(
    df[0:10],
    path=['name','genres'],
    values='Votes',
    color='Votes',
    color_continuous_scale=x[c],
    width=800,
    height=800)
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
        cursor.execute("SELECT D.name ,D.languages FROM data2 as D WHERE D.networks like" + f'\'%{value}%\' and D.languages is not null')
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
        plot_bgcolor='white'
    )
    c = {'Netflix':'#ff6b6b',
         'Prime Video':'#00A8E1',
        'HBO':'#800080',
        'Disney+':'#72efdd'}
    fig.update_traces(marker_color=c[value])

    return fig


# In[55]:


