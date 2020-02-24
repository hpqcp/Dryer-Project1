import sys
sys.path.append('../')
import dash
from dash.dependencies import Output,Input,State
import dash_core_components as dcc
import dash_html_components as html
# import dash_auth
import plotly
from pandas import DataFrame
import pandas as pd
from datetime import datetime

# import sshc.modelPredict as  mp
import sshc.simulationRun.dataSource as ds
import sshc.simulationRun.running_datasoure as rd





VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'sshc2020'
}

app = dash.Dash(__name__)
server = app.server
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

def create_html():
    # if run1 == None or run1.dfAll.empty:
    #     return None
    # r2=run1.r2
    # mse = run1.mse
    # mae = run1.mae
    # df = DataFrame([r2,mse,mae]).round(5)
    # df1 = DataFrame(['R2','MSE','MAE'])
    # df = pd.concat([df1,df],axis=1)
    # df.columns = ['指标名','指标值']
    # html1 = html.Table([
    #         html.Tr(
    #             [
    #                 html.Th(col) for col in df.columns
    #             ]
    #         )]
    #         + [
    #             html.Tr(
    #                 [
    #                     html.Td(
    #                         df.iloc[i][col], style={'border': 'solid 1px black', 'width': '100px'}
    #                     ) for col in df.columns
    #                 ],
    #             ) for i in range(len(df))
    #     ]
    # )
    # return html1
    return None

# 定义表格组件
def create_table(max_rows=12):
    # if run1 == None or run1.dfAll.empty:
    #     return None
    #
    # rList = run1.batchRunProcess.realYList[-run1.step:]
    # pList = run1.batchRunProcess.predictYList[-run1.step:]
    # cList = list(map(lambda x: x[0] - x[1], zip(rList, pList)))
    # tList = run1.dfAll.values[-run1.step:,0]
    # df = DataFrame([rList,pList,cList]).T
    # # df.loc['平均值'] = df.apply(lambda x: x.mad())
    # df = df.round(2)
    # df = pd.concat([DataFrame(tList),df],axis = 1)
    # df.columns = ['时间','实际值','预测值','差值']
    # df['时间'] = pd.to_datetime(df['时间'])
    # df['时间'] = df['时间'].map(lambda x: x.strftime('%H:%M:%S'))
    #
    # """基于dataframe，设置表格格式"""
    # table = html.Table(
    #     # Header
    #     [
    #         html.Tr(
    #             [
    #                 html.Th(col) for col in df.columns
    #             ]
    #         )
    #     ]
    #     # Body
    #     +[
    #         html.Tr(
    #             [
    #                 html.Td(
    #                     df.iloc[i][col],style={'border':'solid 1px black','width':'100px'}
    #                 ) for col in df.columns
    #             ],
    #         ) for i in range(min(len(df), max_rows))
    #     ]
    # )
    # return table
    return None

def batch_splite(_no):
    # import sshc.simulationRun.dataSource as ds
    # import sshc.simulationRun.batchProcess as bp
    # sshc_ds = ds.sshc_datasource(no=_no)
    # batch1 = bp.batch(sshc_ds.sshc_df)
    # batch1.batch_splite_byTime(interval=12)
    # rtList = batch1.spliteLocList
    # # dd = [{'label': '11月3日', 'value': 0},
    # #                  {'label': '11月4日', 'value': 1}]
    batch1 = dash_run.batchList
    listBatch=[]
    for i in range(len(batch1)):
        dictBatch = {}
        dic1 = dash_run.batchList[i]
        # key_list = list(filter(lambda k: dic1.get(k) == _no, dic1.keys()))
        label1 = dic1['label']
        value1 = dic1['value']
        dateValue1 = dic1['date']
        if dateValue1 == _no:
            dictBatch['label'] = label1
            dictBatch['value'] = str(_no)+'-'+str(value1)#+'-'+str(rtList[i][0])+'-'+str(rtList[i][1])
            listBatch.append(dictBatch)
    # listBatch.append({'label':'All','value':str(_no)+'-0-0'})
    return listBatch

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
                 {'label': '11月14日', 'value': 10},
                 {'label': '11月15日', 'value': 11},
                 {'label': '11月16日', 'value': 12},
                 {'label': '11月17日', 'value': 13}]
    batchList = [{'label': '11月3日 第 1 批', 'value': 0,'date':0},
                 {'label': '11月3日 第 2 批', 'value': 1, 'date': 0},
                 {'label': '11月4日 第 1 批', 'value': 0, 'date': 1},
                 {'label': '11月4日 第 2 批', 'value': 1, 'date': 1},
                 {'label': '11月5日 第 1 批', 'value': 0, 'date': 2},
                 {'label': '11月5日 第 2 批', 'value': 1, 'date': 2},
                 {'label': '11月6日 第 1 批', 'value': 0, 'date': 3},
                 {'label': '11月6日 第 2 批', 'value': 1, 'date': 3},
                 {'label': '11月7日 第 1 批', 'value': 0, 'date': 4},
                 {'label': '11月7日 第 2 批', 'value': 1, 'date': 4},
                 {'label': '11月8日 第 1 批', 'value': 0, 'date': 5},
                 {'label': '11月8日 第 2 批', 'value': 1, 'date': 5},
                 {'label': '11月9日 第 1 批', 'value': 0, 'date': 6},
                 {'label': '11月10日 第 1 批', 'value': 0, 'date': 7},
                 {'label': '11月10日 第 2 批', 'value': 1, 'date': 7},
                 {'label': '11月11日 第 1 批', 'value': 0, 'date': 8},
                 {'label': '11月11日 第 2 批', 'value': 1, 'date': 8},
                 {'label': '11月12日 第 1 批', 'value': 0, 'date': 9},
                 {'label': '11月12日 第 2 批', 'value': 1, 'date': 9},
                 {'label': '11月14日 第 1 批', 'value': 0, 'date': 10},
                 {'label': '11月15日 第 1 批', 'value': 0, 'date': 11},
                 {'label': '11月16日 第 1 批', 'value': 0, 'date': 12},
                 {'label': '11月17日 第 1 批', 'value': 0, 'date': 13},

    ]
    # dataDF = None
    # batchDateNo = 0
    # batchNo = 0
    # step = 10
    # batchRunProcess = None

    # def __init__(self,_batchDateNo,_batchNo,_step = 10):
    #     self.batchDateNo = _batchDateNo
    #     self.batchNo = _batchNo
    #     self.step = _step
    #     self.dataDF = rd.batch_sim_run(_dateNo=_batchDateNo)
    #     self.batchRunProcess = rd.batch_running_process()
    #     self.dfAll = DataFrame()
    #     self.r2 = None
    #     self.mse = None
    #     self.mae = None

    @staticmethod
    def import_data_once(_batchDateNo,_batchNo,_n=0,_step=10):
        # step = self.step
        # nLoc = _n * step
        # df1 = self.dataDF.retrive_data_step(_batchNo=self.batchNo, _startLoc=nLoc, _step=step)
        # scores = self.batchRunProcess.import_running_data(df1)
        # self.r2 = scores['R2']
        # self.mse = scores['MSE']
        # self.mae = scores['MAE']
        #
        # rList = self.batchRunProcess.realYList[:]
        # pList = self.batchRunProcess.predictYList[:]
        # cList = list(map(lambda x: x[0] - x[1], zip(rList, pList)))
        # trList = self.batchRunProcess.realYListTimeseries
        # tpList = self.batchRunProcess.predictYListTimeseries
        # self.dfAll = self.batchRunProcess.dfALL
        # df_return = DataFrame([rList,pList,cList,trList,tpList]).T
        # return df_return
        # # return rList,pList,cList,trList,tpList
        steps = (_n+1) * _step
        dataDF = rd.batch_sim_run(_dateNo=_batchDateNo)
        df1 = dataDF.retrive_data_step(_batchNo=_batchNo, _startLoc=0, _step=steps)
        brp = rd.batch_running_process()
        score,rtlDF = brp.import_running_data(_df=df1)
        return score,rtlDF

app.layout = html.Div([ 
    html.Div([
        html.H2('松散回潮水份预测'),
        html.H1(' '),
        html.Div([
            html.Div([html.Label('生产日期选择:')],style={"float":"left","width":"150px"}),
            html.Div([dcc.Dropdown(id='input-dropdown', options=dash_run.dateList)],style={"float":"left","width":"200px"}),
            html.Div([html.Label('批次选择:')],style={"float":"left","width":"150px"}),
            html.Div([dcc.Dropdown(id='batch-dropdown')],style={"float":"left","width":"300px"}),
            html.Div([html.Button(id='submit-button', n_clicks=0, children='提交')],style={"float":"left","width":"150px"}),
            html.Div([dcc.Input(id='n-state',value='-1')],style={"float":"left","width":"150px"}),
            html.Div([],style={"clear":"left"})
            ],style={'display':'inline',"height":"30px"}),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000,
            n_intervals=0,disabled=False
        )],style={'text-align':'center'}),
        html.Div(id='batch-state', style={'display': 'none'})
    # html.Div([html.Div([html.H4('')],style={"float":"left","width":"50px"}),
    #             # html.Div([html.H4('最近水分明细'),html.Table(id='detail-table')],style={"float":"left","width":"300px",'text-align':'center'}),
    #             html.Div([html.H4('')],style={"float":"left","width":"50px"}),
    #             # html.Div([html.H4('最近水分预测指标',id='output-state'),html.Table(id='predict-table')],style={"float":"left","width":"200px",'text-align':'center'}),
    #             html.Div([dcc.Graph(id='water-live-update-graph')],style={"float":"right"}),
    #             html.Div([],style={"clear":"left"})
    # ],style={'display':'inline',"height":"300px"})
])



@app.callback(Output('batch-dropdown', 'options'),
    [Input('input-dropdown', 'value')])
def update_output_div(input_value):
    if input_value == None:
        return []
    return batch_splite(input_value)

@app.callback(Output('batch-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-dropdown', 'value'),
               State('batch-dropdown', 'value')])
def update_output(n_clicks, input1, input2):
    if input2 == None:
        return None
    return str(input2)
#定时器清零
@app.callback(Output('interval-component', 'n_intervals'),
    [Input('submit-button', 'n_clicks')])
def update_interval(input_value):
    return 0
@app.callback(Output('n-state', 'value'),
              [Input('interval-component', 'n_intervals')],)
def update_n(n):
    return str(n)



# @app.callback(Output('predict-table', 'children'),
#     [Input('interval-component', 'n_intervals')])
# def update_detail_table(n):
#     return create_html()
#
# @app.callback(Output('detail-table', 'children'),
#     [Input('interval-component', 'n_intervals')])
# def update_detail_table(n):
#     return create_table()
#

#
# #定时器开启
# @app.callback(Output('interval-component', 'disabled'),
#     [Input('batch-dropdown', 'value')])
# def update_interval(input_value):
#     if input_value == None:
#         return True
#     # res = input_value.split('-')
#     # selectDate = int(res[0])
#     # selectBatch = int(res[1])
#     # global  run1
#     # run1 =  dash_run(selectDate,selectBatch)
#     return False
# #
# #存储日期、批次
# @app.callback(Output('intermediate-value', 'children'),
#     [Input('batch-dropdown', 'value')])
# def update_interval(input_value):
#     if input_value == None:
#         return None
#     res = input_value.split('-')
#     selectDate = int(res[0])
#     selectBatch = int(res[1])
#     # run2 =  dash_run(selectDate,selectBatch)
#
#     return False
#
# #
# @app.callback(Output('interval-component', 'n_intervals'),
#     [Input('batch-dropdown', 'value')])
# def update_interval(input_value):
#     return 0
# #
# #
# @app.callback(Output('water-live-update-graph', 'figure'),[Input('interval-component', 'n_intervals')])
# def water_update_graph_live(n):
#     global run1
#     if run1 == None:
#         return plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2,
#                                              subplot_titles=['加水量趋势', '预测值-实际值差', '全批次水分对比'])
#     if run1.dfAll.empty:
#         return plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2,
#                                              subplot_titles=['加水量趋势', '预测值-实际值差', '全批次水分对比'])
#     df = run1.dfAll
#     dt1 = df.values[:,0]
#     dt2 = df.values[:,10]
#     dt3 = df.values[:, 9]
#     fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2,
#                                         subplot_titles=['加水量趋势', '预测值-实际值差', '全批次水分对比'])
#     fig['layout']['margin'] = {
#         'l': 10, 'r': 10, 'b': 10, 't': 50
#     }
#     # fig['layout']['legend'] = {'x': 1, 'y': 0, 'xanchor': 'right', 'orientation':'h'}
#     fig.append_trace({
#         'x': dt1,
#         'y': dt2,
#         'name': '实际加水量',
#         'mode': 'lines',  # 'lines+markers',
#         'type': 'scatter'
#     }, 1, 1)
#     fig.append_trace({
#         'x': dt1,
#         'y': dt3,
#         'name': '加水量设定值',
#         'mode': 'lines',  # 'lines+markers',
#         'type': 'scatter'
#     }, 1, 1)
#     return fig
#
#
#
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')],
              [State('batch-state', 'children')])
def update_graph_live(n,batchState):
    print(str(batchState))
    if batchState == None:
        return plotly.subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.2,subplot_titles=['最近五分钟水分对比','预测值-实际值差','全批次水分对比'])
    res = batchState.split('-')
    selectDate = int(res[0])
    selectBatch = int(res[1])
    score , rtlDF = dash_run.import_data_once(selectDate,selectBatch,_n=n)

    if rtlDF.empty :
        return plotly.subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.2,subplot_titles=['最近五分钟水分对比','预测值-实际值差','全批次水分对比'])

    # rList, pList, cList ,trList,tpList= run1.import_data(n)
    trList = rtlDF.values[:,0]
    tpList = trList
    rList = rtlDF.values[:,1]
    pList = rtlDF.values[:,2]
    cList = rtlDF.values[:,3]
    srlist = rList[-50:]
    splist = pList[-50:]
    sclist = cList[-50:]
    strList = trList[-50:]
    stpList = tpList[-50:]

    fig = plotly.subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.2,subplot_titles=['最近五分钟水分对比','预测值-实际值差','全批次水分对比'])
    fig['layout']['margin'] = {
        'l': 10, 'r': 10, 'b': 10, 't': 50
    }
    # fig['layout']['legend'] = {'x': 1, 'y': 0, 'xanchor': 'right', 'orientation':'h'}
    fig.append_trace({
        'x': strList,
        'y': srlist,
        'name': '5分钟实际值',
        'mode': 'lines',#'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': strList,
        'y': splist,
        'name': '5分钟预测值',
        'mode': 'lines',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': trList,
        'y': rList,
        'name': '总览实际值',
        'mode': 'lines',
        'type': 'scatter'
    }, 3, 1)
    fig.append_trace({
        'x': trList,
        'y': pList,
        'name': '总览预测值',
        'mode': 'lines',
        'type': 'scatter'
    }, 3, 1)
    fig.append_trace({
        'x': strList,
        'y': sclist,
        'name': '五分钟预测-实际差',
        'type': 'bar'
    }, 2, 1)
    return fig



if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)