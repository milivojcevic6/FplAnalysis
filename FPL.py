#%%

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
p= pd.DataFrame(json['elements'])
p11=p[p['team_code']==3]
p11=p11.loc[:,['web_name','code']]
p11=p11.rename({'web_name': 'label', 'code': 'value'}, axis=1)
dic_p1= p11.to_dict(orient='records')

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
df=p1.to_dict('records')


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
        html.H2("FPL Analysis", className="display-4", style={'color':'#f8f9fa'}),
        html.Hr(),
        html.P(
            "Number of students per education level", className="lead"
        ),
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
        #html.Footer(
        #        html.Div([
        #                    html.A( html.I(className="fa fa-github"),
        #                    href="https://github.com/milivojcevic6", target="_blank",),
        #                    html.I(className="bi bi-person-bounding-box"),
        #                    html.I(className="bi bi-person-bounding-box"),
        #            ], className='col-sm-5 social d-inline')
        #    )


        #<div class="col-sm-5 social">
        #            <ul>
        #                <li>
        #                    <a href="https://github.com/milivojcevic6" target="_blank"><i class="fa fa-github" aria-hidden="true"></i></a>
        #               </li>
        #                <li>
        #                    <a href="https://www.linkedin.com/in/milivojcevic6" target="_blank"><i class="fa fa-linkedin" aria-hidden="true"></i></a>
       #                 </li>
       #                 <li>
       #                     <a href="https://www.instagram.com/milivojcevic6/" target="_blank"><i class="fa fa-instagram" aria-hidden="true"></i></a>
        #                </li>
        #            </ul>
       #        </div>

        #html.Div(
        #    [
        #        html.I(className="bi bi-person-bounding-box"),
        #        html.I(className="bi bi-github"),
        #        html.I(className="bi bi-linkedin"),
        #    ], style={width="32"; height="32"}),
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
                )

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
                
                html.H4("Select first player",
                       style={'margin-top': '5%', 'textAlign':'center'}),

                dcc.Dropdown(
                    id='team1',
                    options=dic_teams,
                    multi=False,
                    value='3'
                ),
                html.Div([
                    dcc.Dropdown(
                        id='player1',
                        options=dic_p1,
                        value=p11.iloc[0,1],
                        multi=False,
                    )
                ]),

                html.H4("Select second player",
                       style={'margin-top': '2%', 'textAlign':'center'}),

                dcc.Dropdown(
                    id='team2',
                    options=dic_teams,
                    multi=False,
                    value='3'
                ),
                html.Div([
                    dcc.Dropdown(
                        id='player2',
                        options=dic_p1,
                        value=p11.iloc[0,1],
                        multi=False,
                    )
                ]),
                html.Div([
                            dash_table.DataTable(
                                    id='table',
                                    columns=['Categories', 'Player 1', 'Player 2'],
                                    data=df,
                                    style_cell=dict(textAlign='left'),
                                    style_header=dict(backgroundColor="paleturquoise"),
                                    style_data=dict(backgroundColor="lavender")
                                )
                        ])
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


# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='top_map', component_property='figure'),
    [Input(component_id='cat', component_property='value')]
)
def update_graph(option_slctd):

    #container = "Displayed category: {}".format(option_slctd)
    print(option_slctd)

    df=pd.DataFrame(json['elements'])
    dff = df.sort_values( option_slctd, ascending=False)
    dff = dff.loc[:,['web_name', option_slctd]]
    names = dff.iloc[0:5, 0]
    values = dff.iloc[0:5, 1]

    barchart=px.bar(dff, names, values, text_auto=True)

    return barchart

@app.callback(
    Output('player1', 'children'),
    Input('team1', 'value')
)
def update_output(value1):

    p1=p[p['team_code']==value1]
    p11=p1.loc[:,['web_name','code']]
    p11=p11.rename({'web_name': 'label', 'code': 'value'}, axis=1)
    dic_p1= p11.to_dict(orient='records')
    print(p11)

    x=html.Div([
        dcc.Dropdown(
            id='player1',
            value= p11.iloc[1,1],
            options=dic_p1,
            multi=False,
        )
    ])

    return x

@app.callback(
    Output('player2', 'children'),
    Input('team2', 'value')
)
def update_output(value1):

    p11=p[p['team_code']==value1]
    p11=p11.loc[:,['web_name','code']]
    p11=p11.rename({'web_name': 'label', 'code': 'value'}, axis=1)
    dic_p1= p11.to_dict(orient='records')

    x=html.Div([
        dcc.Dropdown(
            id='player2',
            value= p11.iloc[1,1],
            options=dic_p1,
            multi=False,
        )
    ])

    return x

@app.callback(
    Output('table','figure'),
    [Input('player1', 'value'),
    Input('player2', 'value')]
)
def update_output(vp1,vp2):

    p1=p[p['code']==vp1]
    p2=p[p['code']==vp2]
    p1=p1.loc[:,['web_name','total_points','goals_scored','assists','clean_sheets','minutes','penalties_missed','penalties_saved','saves','yellow_cards','red_cards', 'dreamteam_count','bonus','now_cost']]
    p2=p2.loc[:,['web_name','total_points','goals_scored','assists','clean_sheets','minutes','penalties_missed','penalties_saved','saves','yellow_cards','red_cards', 'dreamteam_count','bonus','now_cost']]
    indd =['Player','Total points','Goals scored','Assists','Clean sheets','Minutes played','Penalities missed','Penalities saved','Saves','Yellow cards','Red cards','Team of the week','Bonus points','Current value (times 10)']

    p1=p1.append(p2)
    p1=p1.transpose()
    p1['Categories'] = indd
    print('p1')
    print(p1.head())
    p1.columns=['Player 1', 'Player 2', 'Categories']
    df=p1.to_dict('records')

    x=html.Div([
            dash_table.DataTable(
                id='table',
                columns=['Categories', 'Player 1', 'Player 2'],
                data=df,
                style_cell=dict(textAlign='left'),
                style_header=dict(backgroundColor="paleturquoise"),
                style_data=dict(backgroundColor="lavender")
            )
    ])


    return x


if __name__ == '__main__':
    app.run_server(debug=True)