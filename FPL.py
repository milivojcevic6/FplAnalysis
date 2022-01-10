import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import random
import requests
import numpy as np
import matplotlib.pyplot as plt

url= "https://fantasy.premierleague.com/api/bootstrap-static/"
r= requests.get(url)
json= r.json()

p= pd.DataFrame(json['elements'])          # uploading players

#------------------------------------------ creating a list for player dropdown

p11=p[p['team_code']==3]
p11=p11.loc[:,['web_name','code']]
p11=p11.rename({'web_name': 'label', 'code': 'value'}, axis=1)
ddic_p1= p11.to_dict(orient='records')

#------------------------------------------ creating default players for the table

p1=p[p['code']==80201]
p2=p[p['code']==54694]
p1=p1.loc[:,['web_name','total_points','goals_scored','assists','clean_sheets','minutes','penalties_missed','penalties_saved','saves','yellow_cards','red_cards', 'dreamteam_count','bonus','now_cost']]
p2=p2.loc[:,['web_name','total_points','goals_scored','assists','clean_sheets','minutes','penalties_missed','penalties_saved','saves','yellow_cards','red_cards', 'dreamteam_count','bonus','now_cost']]
indd =['Player','Total points','Goals scored','Assists','Clean sheets','Minutes played','Penalities missed','Penalities saved','Saves','Yellow cards','Red cards','Team of the week','Bonus points','Current value (times 10)']

p1=p1.append(p2)
p1=p1.transpose()
p1['Categories'] = indd
p1.columns=['Player 1', 'Player 2', 'Categories']
df=p1


teams = pd.DataFrame(json['teams'])          # uploading teams

#------------------------------------------ creating a list for teams dropdown
teams= teams.loc[:,['name','code']]
teams = teams.rename({'name': 'label', 'code': 'value'}, axis=1)
dic_teams= teams.to_dict(orient='records')

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#00308f",
    'color':'#f8f9fa'
}

CONTENT_STYLE = {
    "min-height": "100%",
    "margin-left": "16rem",
    #"margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


sidebar = html.Div(
    [
        html.H2("FPL Analysis", className="display-4"),
        html.Hr(),
        html.P(
            "Number of students per education level", className="lead"
        ),
        html.Br(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Top players", href="/top", active="exact"),
                dbc.NavLink("Player comparison", href="/players", active="exact"),
                dbc.NavLink("Player prediction", href="/prediction", active="exact"),
            ], style={'color':"light"},
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Welcome to the FPL Analysis',
                        style={'textAlign':'center'}),
                html.H4("Select the section you would like to visit",
                       style={'margin-top': '15%', 'textAlign':'center'}), 
                html.Div(
                    [
                        dbc.Button("Top players", href="/top", className='mt-4', style={'width':'30%'}, outline=True, color="secondary", size="lg"),
                        html.Br(),
                        dbc.Button("Player comparison", href="/players", className='my-2', style={'width':'30%'}, outline=True, color="secondary", size="lg"),
                        html.Br(),
                        dbc.Button("Player prediction", href="/prediction", style={'width':'30%'}, outline=True, color="secondary", size="lg"),
                    ],
                    className="d-grid gap-2 d-md-block", 
                    style={'textAlign':'center'},
                ),
                html.Div(
                    html.H4('Currently, FPL is played by '+str(json['total_players'])+' players', className='fixed-bottom'),
                        style={'margin-left':'35%', 'background-color':'red', 'width':'30%' },
                    className='d-flex')
                ]
    elif pathname == "/top":
        return [
                html.H1('Top 5 players',
                        style={'textAlign':'center'}),
                html.H4("Select the category",
                       style={'margin-top': '5%', 'textAlign':'center'}),
                
                dcc.Dropdown(id="cat",
                    options=[
                        {"label": "Total points", "value": "total_points"},
                        {"label": "Total goals", "value": "goals_scored"},
                        {"label": "Total assists", "value": "assists"},
                        {"label": "Total clean sheets", "value": "clean_sheets"}],
                    multi=False,
                    clearable=False,
                    value="total_points",
                    style={'width': "40%"}
                    ),
                    html.Br(),
                    dcc.Graph(id='top_map', figure={})
                ]

    elif pathname == "/players":
        return [
                html.H1('Compare players',
                        style={'textAlign':'center'}),
                html.Hr(),
                
                html.Div([
                    html.Div([
                        html.H4("Select first player",
                           style={'margin-top': '5%', 'textAlign':'center'}),

                        dcc.Dropdown(
                            id='team1',
                            options=dic_teams,
                            multi=False,
                            value=0
                        ),
                        html.Div([
                            dcc.Dropdown(
                                id='player1',
                                options=ddic_p1,
                                value=0,
                                multi=False,
                            )
                        ])], className='mx-auto', style={'width':'40%'}),

                    html.Div([
                        html.H4("Select second player",
                               style={'margin-top': '5%', 'textAlign':'center'}),
                        dcc.Dropdown(
                            id='team2',
                            options=dic_teams,
                            multi=False,
                            value=0
                        ),
                        html.Div(
                            dcc.Dropdown(
                                id='player2',
                                options=ddic_p1,
                                value=0,
                                multi=False,
                            )
                        )], className='mx-auto', style={'width':'40%'})],
                         className='d-flex'),
                html.Br(),
                html.Div(
                    html.Div(
                            dash_table.DataTable(
                                    id='table',
                                    columns=[{"name": i, "id": i} for i in df.columns],
                                    data=df.to_dict('records'),
                                    style_cell=dict(textAlign='center'),
                                    style_header=dict(backgroundColor="paleturquoise"),
                                    style_data=dict(backgroundColor="lavender"),
                                    style_data_conditional=[
                                        {
                                            'if': {
                                                'filter_query': '{Player 1} > {Player 2}',
                                                'column_id': 'Player 1'
                                            },
                                            'color': 'red'},
                                        {
                                            'if': {
                                                'filter_query': '{Player 2} > {Player 1}',
                                                'column_id': 'Player 2'
                                            },
                                                'color': 'red'},
                                        {
                                            'if': {
                                                'row_index': 0
                                            },
                                            'color': 'black'}]
                                ),
                        style={'width':'50%'},
                        className='mx-auto'),
                    className='d-flex')
    ]
    elif pathname == "/prediction":
        return [
                html.H1('Player prediction',
                        style={'textAlign':'center'}),


                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback(
    Output(component_id='top_map', component_property='figure'),
    [Input(component_id='cat', component_property='value')]
)
def update_graph(option_slctd):

    df=pd.DataFrame(json['elements'])
    dff = df.sort_values( option_slctd, ascending=False)
    dff = dff.loc[:,['web_name', option_slctd]]
    names = dff.iloc[0:5, 0]
    values = dff.iloc[0:5, 1]
    barchart=px.bar(dff, names, values, text_auto=True)

    return barchart

@app.callback(
    [Output('player1', 'value'),
     Output('player1', 'options')],
    Input('team1', 'value')
)
def update_output(value1):

    pp= pd.DataFrame(json['elements'])
    p11=pp[pp['team_code']==value1]
    p11=p11.loc[:,['web_name','code']]
    p11=p11.rename({'web_name': 'label', 'code': 'value'}, axis=1)
    dic_p1= p11.to_dict(orient='records')

    if p11.shape==(0,2):
        x=0
    else: x=p11.iloc[0,1]

    return x, dic_p1

@app.callback(
    [Output('player2', 'value'),
     Output('player2', 'options')],
    Input('team2', 'value')
)
def update_output(value1):

    p11=p[p['team_code']==value1]
    p11=p11.loc[:,['web_name','code']]
    p11=p11.rename({'web_name': 'label', 'code': 'value'}, axis=1)
    dic_p1= p11.to_dict(orient='records')

    if p11.shape==(0,2):
        x=0
    else: x=p11.iloc[0,1]

    return x, dic_p1

@app.callback(
    [Output('table','data'),
     Output('table','columns')],
    [Input('player1', 'value'),
    Input('player2', 'value')]
)
def update_output(vp1,vp2):
    if vp1==0 or vp2==0:
        vp1=80201
        vp2=54694

    p1=p[p['code']==vp1]
    p2=p[p['code']==vp2]
    p1=p1.loc[:,['web_name','total_points','goals_scored','assists','clean_sheets','minutes','penalties_missed','penalties_saved','saves','yellow_cards','red_cards', 'dreamteam_count','bonus','now_cost']]
    p2=p2.loc[:,['web_name','total_points','goals_scored','assists','clean_sheets','minutes','penalties_missed','penalties_saved','saves','yellow_cards','red_cards', 'dreamteam_count','bonus','now_cost']]
    indd =['Name','Total points','Goals scored','Assists','Clean sheets','Minutes played','Penalities missed','Penalities saved','Saves','Yellow cards','Red cards','Team of the week','Bonus points','Current value (times 10)']

    p1=p1.append(p2)
    p1=p1.transpose()
    p1['Categories'] = indd
    p1.columns=['Player 1', 'Player 2', 'Categories']
    p1=p1[['Player 1', 'Categories', 'Player 2']]
    columns=[{"name": i, "id": i} for i in p1.columns]

    return p1.to_dict('records'), columns 


if __name__ == '__main__':
    app.run_server(debug=True)