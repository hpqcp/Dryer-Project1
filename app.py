from flask import Flask
from flask import *
import json
# import JC.jc_predict as jc_pre
# import gb.interface as gb_ine
import pandas as pd
from pandas import DataFrame
import datetime as dat

import dash
from dash.dependencies import Output,Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import sshc.simulationRun.running_datasoure as rd

app_main = Flask(__name__)
app = dash.Dash(__name__, server=app_main, url_base_pathname='/dash2/')
run1 = None
# from gevent import monkey
# from gevent.pywsgi import WSGIServer
# monkey.patch_all()
print


@app_main.route('/login.do',methods=['POST','GET'])
def login():
    print(url_for('login'))#通过函数名找函数对应的地址
    userName = request.form.get('userName')#表单提交的数据用form
    #链接提交的数据用arg
    userPwd = request.form.get('userPwd')
    if userName=='admin' and userPwd=='sshc2020':
        session['user']='admin'
        return redirect('/')
        pass
    elif userName != None and (userName != 'admin' or userPwd != ' sshc2020'):
        return render_template('login.html',message='用户名或密码错误')

    return render_template('login.html')
    pass

@app_main.route('/logout.do',methods=['POST,GET'])
def logout():
    pass

@app_main.route('/')
def index():
    # sessionLen = len(session.keys())
    # if sessionLen == 0 :
    #     return redirect('/login.do')

    if 'user' not in session.keys():
        return redirect('/login.do')
    if session['user'] == 'admin':
        return redirect('/dash1')
    else:
        return redirect('/login.do')
    pass


@app_main.route('/dash1')
def dash1():
    if 'user' not in session.keys():
        return redirect('/login.do')
    if session['user'] == 'admin':
        global app
        return redirect('/dash2')
    else:
        return redirect('/login.do')
    pass


###################################################

def create_html():
    if run1 == None or run1.dfAll.empty:
        return None
    r2 = run1.r2
    mse = run1.mse
    mae = run1.mae
    df = DataFrame([r2, mse, mae]).T.round(5)
    df.columns = ['R2', 'MSE', 'MAE']
    html1 = html.Table([
                           html.Tr(
                               [
                                   html.Th(col) for col in df.columns
                               ]
                           )]
                       + [
                           html.Tr(
                               [
                                   html.Td(
                                       df.iloc[i][col], style={'border': 'solid 1px black', 'width': '100px'}
                                   ) for col in df.columns
                               ],
                           ) for i in range(len(df))
                       ]
                       )
    return html1


# 定义表格组件
def create_table(max_rows=12):
    if run1 == None or run1.dfAll.empty:
        return None

    rList = run1.batchRunProcess.realYList[-run1.step:]
    pList = run1.batchRunProcess.predictYList[-run1.step:]
    cList = list(map(lambda x: x[0] - x[1], zip(rList, pList)))
    tList = run1.dfAll.values[-run1.step:, 0]
    df = DataFrame([rList, pList, cList]).T
    # df.loc['平均值'] = df.apply(lambda x: x.mad())
    df = df.round(2)
    df = pd.concat([DataFrame(tList), df], axis=1)
    df.columns = ['时间', '实际值', '预测值', '差值']
    df['时间'] = pd.to_datetime(df['时间'])
    df['时间'] = df['时间'].map(lambda x: x.strftime('%H:%M:%S'))

    """基于dataframe，设置表格格式"""
    table = html.Table(
        # Header
        [
            html.Tr(
                [
                    html.Th(col) for col in df.columns
                ]
            )
        ]
        # Body
        + [
            html.Tr(
                [
                    html.Td(
                        df.iloc[i][col], style={'border': 'solid 1px black', 'width': '100px'}
                    ) for col in df.columns
                ],
            ) for i in range(min(len(df), max_rows))
        ]
    )
    return table


def batch_splite(_no):
    import sshc.simulationRun.dataSource as ds
    import sshc.simulationRun.batchProcess as bp
    sshc_ds = ds.sshc_datasource(no=_no)
    batch1 = bp.batch(sshc_ds.sshc_df)
    batch1.batch_splite_byTime(interval=12)
    rtList = batch1.spliteLocList
    # dd = [{'label': '11月3日', 'value': 0},
    #                  {'label': '11月4日', 'value': 1}]
    listBatch = []
    for i in range(len(rtList)):
        dictBatch = {}
        dic1 = dash_run.dateList[int(_no)]
        # key_list = list(filter(lambda k: dic1.get(k) == _no, dic1.keys()))
        label1 = dic1['label']
        value1 = dic1['value']
        dictBatch['label'] = label1 + ' - 第 ' + str(i + 1) + ' 批'
        dictBatch['value'] = str(_no) + '-' + str(i)  # +'-'+str(rtList[i][0])+'-'+str(rtList[i][1])
        listBatch.append(dictBatch)
    # listBatch.append({'label':'All','value':str(_no)+'-0-0'})
    return listBatch


class dash_run():
    dateList = [{'label': '11月3日', 'value': 0},
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

    def __init__(self, _batchDateNo, _batchNo, _step=10):
        self.batchDateNo = _batchDateNo
        self.batchNo = _batchNo
        self.step = _step
        self.dataDF = rd.batch_sim_run(_dateNo=_batchDateNo)
        self.batchRunProcess = rd.batch_running_process()
        self.dfAll = DataFrame()
        self.r2 = None
        self.mse = None
        self.mae = None

    def import_data(self, _n=0):
        step = self.step
        nLoc = _n * step
        df1 = self.dataDF.retrive_data_step(_batchNo=self.batchNo, _startLoc=nLoc, _step=step)
        scores = self.batchRunProcess.import_running_data(df1)
        self.r2 = scores['R2']
        self.mse = scores['MSE']
        self.mae = scores['MAE']

        rList = self.batchRunProcess.realYList[:]
        pList = self.batchRunProcess.predictYList[:]
        cList = list(map(lambda x: x[0] - x[1], zip(rList, pList)))
        trList = self.batchRunProcess.realYListTimeseries
        tpList = self.batchRunProcess.predictYListTimeseries
        self.dfAll = self.batchRunProcess.dfALL
        return rList, pList, cList, trList, tpList



# app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H2('松散回潮水份预测'),
        html.H1(' '),
        html.Div([
            html.Div([html.Label('生产日期选择:')], style={"float": "left", "width": "150px"}),
            html.Div([dcc.Dropdown(id='input-dropdown', options=dash_run.dateList)],
                     style={"float": "left", "width": "200px"}),
            html.Div([html.Label('批次选择:')], style={"float": "left", "width": "150px"}),
            html.Div([dcc.Dropdown(id='batch-dropdown')], style={"float": "left", "width": "300px"}),
            html.Div([html.Button('开  始', id='confirm-button')], style={"float": "left", "width": "100px"}),
            html.Div([], style={"clear": "left"})
        ], style={'display': 'inline', "height": "30px"}),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5 * 1000,
            n_intervals=0, disabled=True
        )], style={'text-align': 'center'}),
    html.Div([html.Div([html.H4('')], style={"float": "left", "width": "50px", 'background': 'blue'}),
              html.Div([html.H4('最近水分明细'), html.Table(id='detail-table')],
                       style={"float": "left", "width": "300px", 'text-align': 'center'}),
              html.Div([html.H4('')], style={"float": "left", "width": "50px", 'background': 'blue'}),
              html.Div([html.H4('最近水分预测指标'), html.Table(id='predict-table')],
                       style={"float": "left", "width": "400px", 'text-align': 'center', 'background': 'red'}),
              html.Div([dcc.Graph(id='water-live-update-graph')], style={"float": "right"}),
              html.Div([], style={"clear": "left"})
              ], style={'display': 'inline', "height": "300px"})

])


@app.callback(Output('predict-table', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_detail_table(n):
    return create_html()


@app.callback(Output('detail-table', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_detail_table(n):
    return create_table()


@app.callback(Output('batch-dropdown', 'options'),
              [Input('input-dropdown', 'value')])
def update_output_div(input_value):
    if input_value == None:
        return []
    return batch_splite(input_value)


@app.callback(Output('interval-component', 'disabled'),
              [Input('batch-dropdown', 'value')])
def update_interval(input_value):
    if input_value == None:
        return True
    res = input_value.split('-')
    selectDate = int(res[0])
    selectBatch = int(res[1])
    global run1
    run1 = dash_run(selectDate, selectBatch)
    return False


#
@app.callback(Output('interval-component', 'n_intervals'),
              [Input('batch-dropdown', 'value')])
def update_interval(input_value):
    return 0


#
#
@app.callback(Output('water-live-update-graph', 'figure'), [Input('interval-component', 'n_intervals')])
def water_update_graph_live(n):
    global run1
    if run1 == None:
        return plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2,
                                             subplot_titles=['加水量趋势', '预测值-实际值差', '全批次水分对比'])
    df = run1.dfAll
    dt1 = df.values[:, 0]
    dt2 = df.values[:, 10]
    dt3 = df.values[:, 9]
    fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2,
                                        subplot_titles=['加水量趋势', '预测值-实际值差', '全批次水分对比'])
    fig['layout']['margin'] = {
        'l': 10, 'r': 10, 'b': 10, 't': 50
    }
    # fig['layout']['legend'] = {'x': 1, 'y': 0, 'xanchor': 'right', 'orientation':'h'}
    fig.append_trace({
        'x': dt1,
        'y': dt2,
        'name': '实际加水量',
        'mode': 'lines',  # 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': dt1,
        'y': dt3,
        'name': '加水量设定值',
        'mode': 'lines',  # 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    return fig


#
@app.callback(Output('live-update-graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    print(str(n))
    global run1
    if run1 == None:
        return plotly.subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.2,
                                             subplot_titles=['最近五分钟水分对比', '预测值-实际值差', '全批次水分对比'])
    # step = run1.step
    # nLoc = n*step
    # df1 = run1.dataDF.retrive_data_step(_batchNo= batchNo ,_startLoc = nLoc,_step = step)
    # a= len(brp1.realYlist)
    # brp1.import_running_data(df1)
    # rList = brp1.realYlist[-50:]
    # pList = brp1.predictYList[-50:]
    # cList =  list(map(lambda x: x[0]-x[1], zip(rList, pList)))
    rList, pList, cList, trList, tpList = run1.import_data(n)
    srlist = rList[-50:]
    splist = pList[-50:]
    sclist = cList[-50:]
    strList = trList[-50:]
    stpList = tpList[-50:]
    # len1 = len(srlist)
    # len2 = len(rList)
    fig = plotly.subplots.make_subplots(rows=3, cols=1, vertical_spacing=0.2,
                                        subplot_titles=['最近五分钟水分对比', '预测值-实际值差', '全批次水分对比'])
    fig['layout']['margin'] = {
        'l': 10, 'r': 10, 'b': 10, 't': 50
    }
    # fig['layout']['legend'] = {'x': 1, 'y': 0, 'xanchor': 'right', 'orientation':'h'}
    fig.append_trace({
        'x': strList,
        'y': srlist,
        'name': '5分钟实际值',
        'mode': 'lines',  # 'lines+markers',
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


# @app.route('/index')
# #http://127.0.0.1:5000/index?p=1&type=2
# def index():
#     try:
#         p = request.args.get('p')
#         type = request.args.get('type')
#         msg = '{"code": 1, "msg":' + p + '_' + type + '}'
#     except Exception:
#         msg = '{"code":2,"msg":"操作异常!"}'
#         result = json.dumps(msg,ensure_ascii=False)
#         return result
#     else:
#         msg = '{"code": 1, "msg":' +p+'_'+type+'}'
#         result = json.dumps(msg,ensure_ascii=False)
#         return result
#
# @app.route('/jc')
# #http://127.0.0.1:5000/index?p=1&type=2
# def jcCon():
#     try:
#         ls = request.args.get('ls')
#         ls_list = ls.split(',');
#         for s in range(0, len(ls_list), 1):
#             ls_list[s]=float(ls_list[s])
#         p = jc_pre.predict(ls_list)
#         time = p[0]
#         cycle = p[1]
#         list =[]
#         cycle_list = []
#         if(len(time)<7):
#             addNum=7-len(time)
#             for s in range(0, addNum, 1):
#                 list.append("")
#         for s in range(0, len(time), 1):
#             list.append(str(round(time[s][0],1)))
#         if(len(cycle)<7):
#             addNum=7-len(cycle)
#             for s in range(0, addNum, 1):
#                 cycle_list.append("")
#         for s in range(0, len(cycle), 1):
#             cycle_list.append(str(round(cycle[s],2)))
#         a=0
#     except Exception:
#         msg = '{"code": 2, "msg":"操作异常!"}'
#         result = json.dumps(msg,ensure_ascii=False)
#         return result
#     else:
#         msg = {"code": 1, "msg": {"time":list,"cycle":cycle_list}}
#         result = json.dumps(msg)
#         return result
#
# #gb
# @app.route('/gb')
# def GetUnitDayProduction():
#     try:
#         rsatrt=dat.datetime.now()
#         _type = request.args.get('type')
#         _startTime = request.args.get('startTime')
#         _endTime = request.args.get('endTime')
#         _tags = request.args.get('tags')
#
#         #if((_type==None)|(_startTime==None)|(_endTime==None)|(_tags==None)):
#         #    msg = '{"code":2,"msg":[],"address":"app","errCode":"-79","errMsg":"参数不完整!"}'
#         #    result = json.dumps(msg,ensure_ascii=False)
#         #    return json.loads(result)
#         tagsList = _tags.split(',')
#         resultData = gb_ine.GetUnitDayProduction(_type, _startTime, _endTime, tagsList)
#         #True, ['-101', 'GetUnitDayProduction', '参数_type没有传入已知的类型！']
#         rend = dat.datetime.now()
#         print("***************startTime:"+str(rsatrt)+"   endTime:"+str(rend)+"******************")
#     except Exception as e:
#         msg = '{"code":2,"msg":[],"address":"app","errCode":"-79","errMsg":"操作异常!'+repr(e).replace('"', " ").replace("'", " ")+'"}'
#         result = json.dumps(msg,ensure_ascii=False)
#         return json.loads(result)
#     else:
#         if (resultData[0] == True):
#             #True, ['0', 'GetUnitDayProduction', '本日未开机！']
#             if((resultData[1])[0]=='0'):
#                 msg = '{"code":1,"msg":[],"address":"","errCode":"","errMsg":"本日未开机!"}'
#                 result = json.dumps(msg, ensure_ascii=False)
#                 return json.loads(result)
#             else:
#                 msg = '{"code":2,"msg":[],"address":"' + (resultData[1])[1] + '","errCode":"' + \
#                       (resultData[1])[0] + '","errMsg":"' + (resultData[1])[2] + '"}'
#                 result = json.dumps(msg,ensure_ascii=False)
#                 return json.loads(result)
#         else:
#             df = resultData[1]
#             df['StartTimeStr'] = df['StartTime'].apply(lambda x:'NaT' if pd.isnull(x) else x.strftime("%Y-%m-%d %H:%M:%S"))
#             df['EndTimeStr'] = df['EndTime'].apply(lambda x: 'NaT' if pd.isnull(x) else x.strftime("%Y-%m-%d %H:%M:%S"))
#             daf = df.to_json(orient = 'records', force_ascii = False)
#             msg = '{"code":1,"msg":'+daf+',"address":"","errCode":"","errMsg":"成功"}'
#             result = json.dumps(msg,ensure_ascii=False)
#             return json.loads(result)
#
# @app.route('/zs')
#
#
# #http://localhost:5000/zs?tags=MES2RTDATA.U_BAL_11010010002.DC_TeamCode,MES2RTDATA.U_CON_11010010003.DC_PCH,MES2RTDATA.U_CON_11010010003.DC_PH,MES2RTDATA.U_BAL_11010010002.DC_LL&freq=60000&startTime=2019-8-9 06:00:00&endTime=2019-8-10 06:00:00&delay=1800
# def GetBatchInfoBySegment():
#     try:
#         rsatrt = dat.datetime.now()
#         _freq = request.args.get('freq')
#         _startTime = request.args.get('startTime')
#         _endTime = request.args.get('endTime')
#         _tags = request.args.get('tags')
#         _delay = request.args.get('delay')
#         tagsList = _tags.split(',')
#
#         resultData = gb_ine.GetBatchInfoBySegment(tagsList,_freq,_startTime,_endTime,int(_delay)) #调用interFace接口
#         rend = dat.datetime.now()
#         print("***************startTime:" + str(rsatrt) + "   endTime:" + str(rend) + "******************")
#     except Exception as e:
#         msg = '{"code":2,"msg":[],"address":"app","errCode":"-122","errMsg":"操作异常!' + repr(e).replace('"', " ").replace(
#             "'", " ") + '"}'
#         result = json.dumps(msg, ensure_ascii=False)
#         return json.loads(result)
#     else:
#         if (resultData[0] == True):
#             # True, ['0', 'GetUnitDayProduction', '本日未开机！']
#             if ((resultData[1])[0] == '0'):
#                 msg = '{"code":1,"msg":[],"address":"","errCode":"","errMsg":"本日未开机!"}'
#                 result = json.dumps(msg, ensure_ascii=False)
#                 return json.loads(result)
#             # else:
#             #     msg = '{"code":2,"msg":[],"address":"' + (resultData[1])[1] + '","errCode":"' + \
#             #           (resultData[1])[0] + '","errMsg":"' + (resultData[1])[2] + '"}'
#             #     result = json.dumps(msg, ensure_ascii=False)
#             #     return json.loads(result)
#         else:
#             df = resultData[1]
#             # df['StartTimeStr'] = df['StartTime'].apply(lambda x: 'NaT' if pd.isnull(x) else x.strftime("%Y-%m-%d %H:%M:%S"))
#             # df['EndTimeStr'] = df['EndTime'].apply(lambda x: 'NaT' if pd.isnull(x) else x.strftime("%Y-%m-%d %H:%M:%S"))
#             daf = df.to_json(orient='records', force_ascii=False)
#             msg = '{"code":1,"msg":' + daf + ',"address":"","errCode":"","errMsg":"成功"}'
#             result = json.dumps(msg, ensure_ascii=False)
#             return json.loads(result)





if __name__ == '__main__':
    app_main.config['SECRET_KEY'] = '1234567890'
    app_main.run(host='127.0.0.1', port=5000,threaded=True,debug=False)
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()