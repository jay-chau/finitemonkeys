import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

def pSuccess(characters, timestep, monkeys, speed):
    keys = 29 #26 letters plus space, . and ,
  
    return 1-((1-(1/keys)**characters)**((timestep-characters+1)*speed))**monkeys

def maxaxis(c, m, s,p):
    k=29
    return (-s*np.log(1 - (1/k)**c) + c*s*np.log(1 - (1/k)**c) + np.log((1 - p)**(1/m)))/(s*np.log(1 - (1/k)**c))


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children = [
    html.Div(children="Characters"),
    dcc.Slider(id="Literature", min=1, max=10, step=1, value=2, marks={i: '{}'.format(i) for i in range(0,11,1)}),
    html.Div(children="Monkeys"),
    dcc.Slider(id="Monkeys", min=1, max=100, step=1, value=2, marks={i: '{}'.format(i) for i in range(0,105,5)}),
    html.Div(children="Speed (Characters/Second)"),
    dcc.Slider(id="Speed", min=1, max=20, step=1, value=2, marks={i: '{}'.format(i) for i in range(0,25,5)}),
    html.Div(
        dcc.Graph(id='ProbabilityTime')
        )
    ])

@app.callback(
    Output("ProbabilityTime", "figure"),
    [
        Input("Literature", "value"),
        Input("Monkeys", "value"),
        Input("Speed", "value")
        ]
    )
def calculatemonkeys(characters, monkeys, speed):
    monkeylife = 25 #years
    xaxis = maxaxis(characters,monkeys, speed,0.99)
    timeaxis = np.linspace(characters, xaxis, 101)
    t = pSuccess(characters, timeaxis, monkeys, speed)
    r = {
        'data':[
            {'x': timeaxis,
            'y': t*100,
            'name': "Probability"}
            ],
        'layout': {
            'title': "title",
            'yaxis': {
                "title": "Success (%)",
                "range": [0,100]},
            'xaxis': {
                "range": [0,xaxis],
                "title": "Seconds"}
            }
        }
    return r

if __name__ == '__main__':
    app.run_server(debug=True)