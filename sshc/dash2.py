import dash
from dash.dependencies import Output,Input
import dash_core_components as dcc
import dash_html_components as html
import plotly

import sshc.modelPredict as  mp
import sshc.simulationRun.dataSource as ds

# allDF = DataFrame()
# for i in range(0, 14, 1):
#     df = ds.sshc_datasource(no=i).sshc_df
#     batch2 = bp.batch(df)
#     wtDFList = batch2.retrive_wt_data(_flowCol=1, _moistureCol=3, _triggerFlow=0, _triggerMoisture=16,
#                                       _delay=60)  # [df]
#     for wtDF in wtDFList:
#         allDF = pd.concat([allDF, wtDF], axis=0)
# allDF = allDF.iloc[:, [3, 9, 6, 16, 15, 8]]
# df_x = allDF.values[:, 1:]
# df_y = allDF.values[:, 0]
# rf_model, ss_x, ss_y = mp.randomForest_model(df_x, df_y)
rf_model = mp.model_load('c://allX.m')
ss_x = mp.model_load('c://allX-ss_x.m')
ss_y = mp.model_load('c://allX-ss_y.m')

df1 = ds.sshc_datasource(no=0).sshc_df
# batch1 = bp.batch(df1)
# wtDFList = batch1.retrive_wt_data(_flowCol=1, _moistureCol=3, _triggerFlow=0, _triggerMoisture=16,
#                                   _delay=60)  # (2,1,0,16,60)





app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('Example'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=2*1000,
            n_intervals=0
        )
    ])
)

@app.callback(Output('live-update-graph', 'figure'),[Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    nLoc = n*50
    if nLoc > df1.shape[0]:
        nLoc = df1.shape[0]
    testDF = df1.iloc[:n*100, :]  # pd.concat([headDF1,wtDFList[0].iloc[:i,:]],axis=0)
    testDF = testDF.iloc[:, [3, 9, 6, 16, 15, 8]]
    df_x1 = testDF.values[:, 1:]
    df_y1 = testDF.values[:, 0]
    scores, df_p = mp.randomForest_predict_score(rf_model, ss_x, ss_y, df_x1, df_y1, _isPlot=False)
    fig = plotly.subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    # fig['layout']['margin'] = {
    #     'l': 30, 'r': 10, 'b': 30, 't': 10
    # }
    # fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    sLoc = 0
    if nLoc>100 :
        sLoc = nLoc - 100
    data_y = df_p.values[sLoc:,0]
    data_y1 = df_p.values[sLoc:, 1]
    lens = len(data_y)
    fig.append_trace({
        'x': [i for i in range(lens)],
        'y': data_y,
        'name': '实际值',
        'mode': 'lines',#'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': [i for i in range(lens)],
        'y': data_y1,
        'name': '预测值',
        'mode': 'lines',
        'type': 'scatter'
    }, 1, 1)
    # fig.append_trace({
    #     'x': [i for i in range(lens)],
    #     'y': df_p.values[:,2],
    #     'name': 'Bar',
    #     'type': 'bar'
    # }, 1, 1)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)