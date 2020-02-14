import dash
from dash.dependencies import Output,Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
from pandas import DataFrame

# import sshc.modelPredict as  mp
import sshc.simulationRun.dataSource as ds
import sshc.simulationRun.running_datasoure as rd



# # 定义表格组件
# def create_table(df,max_rows=12):
#
#     """基于dataframe，设置表格格式"""
#     table = html.Table(
#         # Header
#         [
#             html.Tr(
#                 [
#                     html.Th(col) for col in DataFrame(columns={'实际值','预测值'}).columns#df.columns
#                 ]
#             )
#         ]
#         # # Body
#         # +[
#         #     html.Tr(
#         #         [
#         #             html.Td(
#         #                 df.iloc[i][col]
#         #             ) for col in df.columns
#         #         ]
#         #     ) for i in range(min(len(df), max_rows))
#         # ]
#     )
#     return table
#
# def batch_splite(_no):
#     import sshc.simulationRun.dataSource as ds
#     import sshc.simulationRun.batchProcess as bp
#     sshc_ds = ds.sshc_datasource(no=_no)
#     batch1 = bp.batch(sshc_ds.sshc_df)
#     batch1.batch_splite_byTime(interval=12)
#     rtList = batch1.spliteLocList
#     # dd = [{'label': '11月3日', 'value': 0},
#     #                  {'label': '11月4日', 'value': 1}]
#     listBatch=[]
#     for i in range(len(rtList)):
#         dictBatch = {}
#         dic1 = dateList[int(_no)]
#         # key_list = list(filter(lambda k: dic1.get(k) == _no, dic1.keys()))
#         label1 = dic1['label']
#         value1 = dic1['value']
#         dictBatch['label'] = label1+' - 第 '+str(i+1)+' 批'
#         dictBatch['value'] = str(_no)+'-'+str(i)#+'-'+str(rtList[i][0])+'-'+str(rtList[i][1])
#         listBatch.append(dictBatch)
#     # listBatch.append({'label':'All','value':str(_no)+'-0-0'})
#     return listBatch

class dash_run():
    dateList = [ {'label': '11月3日', 'value': 0},
                 {'label': '11月4日', 'value': 1},
                 {'label': '11月5日', 'value': 2},
                 {'label': '11月6日', 'value': 3},
                 {'label': '11月7日', 'value': 4},
                 {'label': '11月8日', 'value': 5},
                 {'label': '11月9日', 'value': 6},
                 {'label': '11月10日', 'value': 7},
                 {'label': '11月11日', 'value': 8},
                 {'label': '11月12日', 'value': 9},
                 {'label': '11月13日', 'value': 10},
                 {'label': '11月14日', 'value': 11},
                 {'label': '11月15日', 'value': 12},
                 {'label': '11月16日', 'value': 13}]
    # dataDF = None
    # batchDateNo = 0
    # batchNo = 0
    # step = 10
    # batchRunProcess = None

    def __init__(self,_batchDateNo,_batchNo,_step = 10):
        self.batchDateNo = _batchDateNo
        self.batchNo = _batchNo
        self.step = _step
        self.dataDF = rd.batch_sim_run(_dateNo=_batchDateNo)
        self.batchRunProcess = rd.batch_running_process()

# aa = dash_run(0,0,10)
dash_run.batchNo1 = 10
print




app = dash.Dash(__name__)
# app.layout = html.Div([
#     html.Div([
#         html.H2('松散回潮水份预测'),
#         html.H1(' '),
#         html.Div([
#             html.Div([html.Label('生产日期选择:')],style={"float":"left","width":"150px"}),
#             html.Div([dcc.Dropdown(id='input-dropdown', options=dateList)],style={"float":"left","width":"200px"}),
#             html.Div([html.Label('批次选择:')],style={"float":"left","width":"150px"}),
#             html.Div([dcc.Dropdown(id='batch-dropdown')],style={"float":"left","width":"300px"}),
#             html.Div([html.Button('开  始',id='confirm-button')],style={"float":"left","width":"100px"}),
#             html.Div([],style={"clear":"left"})
#             ],style={'display':'inline',"height":"30px"}),
#         dcc.Graph(id='live-update-graph'),
#         dcc.Interval(
#             id='interval-component',
#             interval=3*1000,
#             n_intervals=0,disabled=True
#         )],style={'text-align':'center'})#,
#     # html.Div([html.H4('美国农业出口数据表(2011年)'),create_table(df)])
# ])
#
# @app.callback(Output('batch-dropdown', 'options'),
#     [Input('input-dropdown', 'value')])
# def update_output_div(input_value):
#     return batch_splite(input_value)
#
# @app.callback(Output('interval-component', 'disabled'),
#     [Input('batch-dropdown', 'value')])
# def update_interval(input_value):
#     if input_value == None:
#         return True
#     res = input_value.split('-')
#     global batchNo,batchDate,brp1
#     selectDate = int(res[0])
#     selectBatch = int(res[1])
#     batchNo = selectBatch
#     batchDate = selectDate
#     brp1.realYlist=[]
#     brp1.predictYList=[]
#     brp1=None
#     brp1 = rd.batch_running_process()
#     a = brp1
#
#
#     return False
#
# @app.callback(Output('interval-component', 'n_intervals'),
#     [Input('batch-dropdown', 'value')])
# def update_interval(input_value):
#     return 0
#
# @app.callback(Output('live-update-graph', 'figure'),[Input('interval-component', 'n_intervals')])
# def update_graph_live(n):
#     print(str(n))
#     global brp1
#     nLoc = n*step
#     df1 = bsr1.retrive_data_step(_batchNo= batchNo ,_startLoc = nLoc,_step = step)
#     a= len(brp1.realYlist)
#     brp1.import_running_data(df1)
#     rList = brp1.realYlist[-50:]
#     pList = brp1.predictYList[-50:]
#     cList =  list(map(lambda x: x[0]-x[1], zip(rList, pList)))
#     len1 = len(brp1.realYlist[:])
#     len2 = len(brp1.realYlist)
#     fig = plotly.subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.2,subplot_titles=['最近五分钟水分对比','预测值-实际值差','全批次水分对比'])
#     fig['layout']['margin'] = {
#         'l': 10, 'r': 10, 'b': 10, 't': 50
#     }
#     fig['layout']['legend'] = {'x': 1, 'y': 0, 'xanchor': 'right', 'orientation':'h'}
#     fig.append_trace({
#         'x': [i for i in range(len1)],
#         'y': rList,
#         'name': '5分钟实际值',
#         'mode': 'lines',#'lines+markers',
#         'type': 'scatter'
#     }, 1, 1)
#     fig.append_trace({
#         'x': [i for i in range(len1)],
#         'y': pList,
#         'name': '5分钟预测值',
#         'mode': 'lines',
#         'type': 'scatter'
#     }, 1, 1)
#     fig.append_trace({
#         'x': [i for i in range(len2)],
#         'y': brp1.realYlist,
#         'name': '总览实际值',
#         'mode': 'lines',
#         'type': 'scatter'
#     }, 3, 1)
#     fig.append_trace({
#         'x': [i for i in range(len2)],
#         'y': brp1.predictYList,
#         'name': '总览预测值',
#         'mode': 'lines',
#         'type': 'scatter'
#     }, 3, 1)
#     fig.append_trace({
#         'x': [i for i in range(len1)],
#         'y': cList,
#         'name': '五分钟预测-实际差',
#         'type': 'bar'
#     }, 2, 1)
#     return fig

if __name__ == '__main__':
    app.run_server(debug=True)