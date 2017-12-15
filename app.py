
# coding: utf-8

# In[1]:

import pandas as pd
df = pd.read_csv('nama_10_gdp_1_Data_aaa.csv')
df.head()


# In[2]:

df.columns


# In[3]:

available_indicators = df['NA_ITEM'].unique()
available_indicators


# In[ ]:

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


available_indicators = df['NA_ITEM'].unique()

available_countries = df['GEO'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices' 
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure' 
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='TIME--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    
    html.Div([

        html.Div([
            dcc.Dropdown(  
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Spain' 
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown( 
                id='indicator',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure' 
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='line-chart')   
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('TIME--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('indicator', 'value')
    ])
def update_graph(country_name, indicator_name):
    
    
    
    return {
        'data': [go.Scatter(
            x = df['TIME'].unique(), 
            y = df[(df['NA_ITEM'] == indicator_name) & (df['GEO'] == country_name)]['Value'], # get the value for y coordinate
            text = country_name, 
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'TIME'
            
            },
            yaxis={
                'title': indicator_name
                
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


# In[20]:

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()


available_indicators = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()


app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(   
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Spain' 
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown( 
                id='indicator',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure' 
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='line-chart')
])

@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('indicator', 'value')
    ])
def update_graph(country_name, indicator_name):
    
   
    
    return {
        'data': [go.Scatter(
            x = df['TIME'].unique(), 
            y = df[(df['NA_ITEM'] == indicator_name) & (df['GEO'] == country_name)]['Value'], # get the value for y coordinate
            text = country_name, 
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'TIME'
            
            },
            yaxis={
                'title': indicator_name
                
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


# In[ ]:



