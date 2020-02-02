import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame
import plotly.graph_objs as go
import dash
import dash_core_components as dcc                  # 交互式组件
import dash_html_components as html                 # 代码转html
from dash.dependencies import Input, Output
import utils.excel2redis as rds

def get_show_scatter(_df):
    x = _df.values[:,0]
    y1 = _df.values[:, 1]
    y2 = _df.values[:, 2]
    y3 = _df.values[:, 3]
    y4 = _df.values[:, 4]
    y5 = _df.values[:, 5]
    y6 = _df.values[:, 6]
    y7 = _df.values[:, 7]
    y8 = _df.values[:, 8]
    y9 = _df.values[:, 9]
    y10 = _df.values[:, 10]
    y11 = _df.values[:, 11]
    y12 = _df.values[:, 12]
    y13 = _df.values[:, 13]
    y14 = _df.values[:, 14]
    y15 = _df.values[:, 15]
    y16 = _df.values[:, 16]
    trace = go.Scatter(
        x=x,
        y=y1,
        name='出口水分'
    )
    trace1 = go.Scatter(
        x=x,
        y=y2,
        name='瞬时流量'
    )
    trace2 = go.Scatter(
        x=x,
        y=y3,
        name='流量设定值'
    )
    trace3 = go.Scatter(
        x=x,
        y=y4,
        name='出口温度'
    )
    trace4 = go.Scatter(
        x=x,
        y=y5,
        name='热风温度设定值'
    )
    trace5 = go.Scatter(
        x=x,
        y=y6,
        name='热风温度实际值'
    )
    trace6 = go.Scatter(
        x=x,
        y=y7,
        name='回风温度设定值'
    )
    trace7 = go.Scatter(
        x=x,
        y=y8,
        name='回风温度实际值'
    )
    trace8 = go.Scatter(
        x=x,
        y=y9,
        name='加水量设定值'
    )
    trace9 = go.Scatter(
        x=x,
        y=y10,
        name='加水量实际值'
    )
    trace10 = go.Scatter(
        x=x,
        y=y11,
        name='蒸汽流量'
    )
    trace11 = go.Scatter(
        x=x,
        y=y12,
        name='空气压力'
    )
    trace12 = go.Scatter(
        x=x,
        y=y13,
        name='水压力检测'
    )
    trace13 = go.Scatter(
        x=x,
        y=y14,
        name='蒸汽压力'
    )
    trace14 = go.Scatter(
        x=x,
        y=y15,
        name='散热器工作压力'
    )
    trace15 = go.Scatter(
        x=x,
        y=y6,
        name='水雾化蒸汽压力'
    )

    return go.Figure(
        data = [trace,trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11,trace12,trace13,trace14,trace15]
    )

def load_data(_key):
    df = rds.getBatchData(_key, 2)
    # df1 = DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
    df1 = DataFrame(df.values[:, [0, 3, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]])
    ret = get_show_scatter(df1)
    return ret

df = rds.getBatchData('2400-2019-11-03*', 2)
# df1 = DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
df1 = DataFrame(df.values[:, [0,3,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16]])
# df2 = DataFrame(df1, dtype=np.float)
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
        html.H1('松散回潮预测分析',style={'text-align':'center'}),
        html.Label('生产日期选择：'),
        dcc.Dropdown(id='input-dropdown',
            options=[{'label': '11月3日', 'value': '2400-2019-11-03*'},
                     {'label': '11月4日', 'value': '2400-2019-11-04*'},
                     {'label': '11月5日', 'value': '2400-2019-11-05*'}],
                        value='2400-2019-11-03*'),
        html.Label(id='output-text'),
        dcc.Graph(
            id='example-graph',
            figure = get_show_scatter(df1)
            )
])
@app.callback(
    Output('example-graph', 'figure'),
    [Input('input-dropdown', 'value')]
)
def update_output_div(input_value):
    return load_data(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
