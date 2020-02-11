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
    len1 = len(brp1.realYlist[:])
    # len2 = len(rList)
    fig = plotly.subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    # fig['layout']['margin'] = {
    #     'l': 30, 'r': 10, 'b': 30, 't': 10
    # }
    # fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig.append_trace({
        'x': [i for i in range(len1)],
        'y': rList,
        'name': '实际值',
        'mode': 'lines',#'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': [i for i in range(len1)],
        'y': pList,
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