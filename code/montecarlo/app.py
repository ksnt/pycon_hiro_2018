# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import random
import json
import math
import numpy as np

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Monte Carlo Simulation'),

    html.Div(children=''' by ksnt
    '''),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='my-slider',
        min=1,
        max=10000,
        step=10,
        value=10,
    ),
    html.Div(id='slider-output-container'),
    html.Div(id='slider-output-container2'),
    html.Div(id='slider-output-container3'),

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})
])

"""
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
"""

@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('intermediate-value', 'children')])
def update_figure(value):
    v = json.loads(value)
    print(v[1].__class__)
    ps_in = v[1]
    ps_out = v[2]
    ps_in_and_out = []
    ps_in_and_out.append(
    go.Scatter(
            x=[p[0] for p in ps_in],
            y=[p[1] for p in ps_in],
            mode='markers',
            name = "Inside Circle",
            opacity=0.7
    ))
    ps_in_and_out.append(
    go.Scatter(
            x=[p[0] for p in ps_out],
            y=[p[1] for p in ps_out],
            mode='markers',
            name = "Outside Circle",
            opacity=0.7
        )
    )
    return {
    'data':ps_in_and_out,
    'layout': go.Layout(
            xaxis={'title': '', 'range': [0,1]},
            yaxis={'title': '', 'range': [0,1]},
            legend={'x': 0, 'y': 1},
            hovermode='closest')
    }

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    return 'The sampling size is: "{}"'.format(value)


@app.callback(
    dash.dependencies.Output('slider-output-container2', 'children'),
    [dash.dependencies.Input('intermediate-value', 'children')])
def update_output(value):
    v = json.loads(value)
    #print(v)
    return 'The value of estimated PI is: "{}"'.format(v[0])


@app.callback(
    dash.dependencies.Output('slider-output-container3', 'children'),
    [dash.dependencies.Input('intermediate-value', 'children')])
def update_output(value):
    v = json.loads(value)
    #print(v)
    return 'The Error is: "{}" %'.format( (abs(v[0] - np.pi)/np.pi)*100 )

@app.callback(
    dash.dependencies.Output('intermediate-value', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_pi(value):
    random.seed(100) # Set the seed
    ps = [[random.random(), random.random()] for i in range(value)]
    count = [ps[i][0] ** 2 + ps[i][1]**2 < 1 for i in range(len(ps))].count(True)
    pi = 4* count / value
    #print(pi)
    ps_in = [p for p in ps if p[0]**2 + p[1]** 2 < 1]
    ps_out = [p for p in ps if p[0]**2 + p[1]** 2 >= 1]
    return json.dumps((pi,ps_in,ps_out))

if __name__ == '__main__':
    app.run_server(debug=True)

