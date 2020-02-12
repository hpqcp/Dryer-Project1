import dash
from dash.dependencies import Output,Input
import dash_core_components as dcc
import dash_html_components as html
import plotly

# import sshc.modelPredict as  mp
import sshc.simulationRun.dataSource as ds
import sshc.simulationRun.running_datasoure as rd

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

bsr1 = rd.batch_sim_run(_no=0)
df = bsr1.batch_df_list[1]
# n = 0
step = 10
brp1 = rd.batch_running_process()
# while(True):
#     df1 = bsr1.retrive_data_step(0,n,step)
#     if df1.empty :
#         break
#     brp1.import_running_data(df1)
#     # loc1 = brp1.get_all(df1.values[:,9],0,'>')
#     a = DataFrame([brp1.realYlist, brp1.predictYList]).T
#
#     n = n + step

# batch1 = bp.batch(df1)
# wtDFList = batch1.retrive_wt_data(_flowCol=1, _moistureCol=3, _triggerFlow=0, _triggerMoisture=16,
#                                   _delay=60)  # (2,1,0,16,60)





app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('Example'),
        dcc.Graph(id='live-update-graph'),
        dcc.Graph(id='step-graph'),
        dcc.Interval(
            id='interval-component',
            interval=2*1000,
            n_intervals=0
        )
    ])
)

@app.callback(Output('live-update-graph', 'figure'),[Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    print(str(n))
    nLoc = n*step
    df1 = bsr1.retrive_data_step(0, nLoc, step)
    brp1.import_running_data(df1)
    rList = brp1.realYlist[-50:]
    pList = brp1.predictYList[-50:]
    cList =  list(map(lambda x: x[0]-x[1], zip(rList, pList)))
    len1 = len(brp1.realYlist[:])
    len2 = len(brp1.realYlist)
    fig = plotly.subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.05,subplot_titles=['五分钟水分对比','预测值-实际值差','全批次水分对比'])
    fig['layout']['margin'] = {
        'l': 10, 'r': 10, 'b': 10, 't': 10
    }
    fig['layout']['legend'] = {'x': 1, 'y': 0, 'xanchor': 'right', 'orientation':'h'}
    fig.append_trace({
        'x': [i for i in range(len1)],
        'y': rList,
        'name': '5分钟实际值',
        'mode': 'lines',#'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': [i for i in range(len1)],
        'y': pList,
        'name': '5分钟预测值',
        'mode': 'lines',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': [i for i in range(len2)],
        'y': brp1.realYlist,
        'name': '总览实际值',
        'mode': 'lines',
        'type': 'scatter'
    }, 3, 1)
    fig.append_trace({
        'x': [i for i in range(len2)],
        'y': brp1.predictYList,
        'name': '总览预测值',
        'mode': 'lines',
        'type': 'scatter'
    }, 3, 1)
    fig.append_trace({
        'x': [i for i in range(len1)],
        'y': cList,
        'name': '五分钟预测-实际差',
        'type': 'bar'
    }, 2, 1)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)