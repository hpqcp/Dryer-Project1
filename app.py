from flask import Flask
from flask import request
import json
import JC.jc_predict as jc_pre
import gb.interface as gb_ine
import pandas as pd
import datetime as dat
app = Flask(__name__)

# from gevent import monkey
# from gevent.pywsgi import WSGIServer
# monkey.patch_all()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
#http://127.0.0.1:5000/index?p=1&type=2
def index():
    try:
        p = request.args.get('p')
        type = request.args.get('type')
        msg = '{"code": 1, "msg":' + p + '_' + type + '}'
    except Exception:
        msg = '{"code":2,"msg":"操作异常!"}'
        result = json.dumps(msg,ensure_ascii=False)
        return result
    else:
        msg = '{"code": 1, "msg":' +p+'_'+type+'}'
        result = json.dumps(msg,ensure_ascii=False)
        return result

@app.route('/jc')
#http://127.0.0.1:5000/index?p=1&type=2
def jcCon():
    try:
        ls = request.args.get('ls')
        ls_list = ls.split(',');
        for s in range(0, len(ls_list), 1):
            ls_list[s]=float(ls_list[s])
        p = jc_pre.predict(ls_list)
        time = p[0]
        cycle = p[1]
        list =[]
        cycle_list = []
        if(len(time)<7):
            addNum=7-len(time)
            for s in range(0, addNum, 1):
                list.append("")
        for s in range(0, len(time), 1):
            list.append(str(round(time[s][0],1)))
        if(len(cycle)<7):
            addNum=7-len(cycle)
            for s in range(0, addNum, 1):
                cycle_list.append("")
        for s in range(0, len(cycle), 1):
            cycle_list.append(str(round(cycle[s],2)))
        a=0
    except Exception:
        msg = '{"code": 2, "msg":"操作异常!"}'
        result = json.dumps(msg,ensure_ascii=False)
        return result
    else:
        msg = {"code": 1, "msg": {"time":list,"cycle":cycle_list}}
        result = json.dumps(msg)
        return result

#gb
@app.route('/gb')
def GetUnitDayProduction():
    try:
        rsatrt=dat.datetime.now()
        _type = request.args.get('type')
        _startTime = request.args.get('startTime')
        _endTime = request.args.get('endTime')
        _tags = request.args.get('tags')

        #if((_type==None)|(_startTime==None)|(_endTime==None)|(_tags==None)):
        #    msg = '{"code":2,"msg":[],"address":"app","errCode":"-79","errMsg":"参数不完整!"}'
        #    result = json.dumps(msg,ensure_ascii=False)
        #    return json.loads(result)
        tagsList = _tags.split(',')
        resultData = gb_ine.GetUnitDayProduction(_type, _startTime, _endTime, tagsList)
        #True, ['-101', 'GetUnitDayProduction', '参数_type没有传入已知的类型！']
        rend = dat.datetime.now()
        print("***************startTime:"+str(rsatrt)+"   endTime:"+str(rend)+"******************")
    except Exception as e:
        msg = '{"code":2,"msg":[],"address":"app","errCode":"-79","errMsg":"操作异常!'+repr(e).replace('"', " ").replace("'", " ")+'"}'
        result = json.dumps(msg,ensure_ascii=False)
        return json.loads(result)
    else:
        if (resultData[0] == True):
            #True, ['0', 'GetUnitDayProduction', '本日未开机！']
            if((resultData[1])[0]=='0'):
                msg = '{"code":1,"msg":[],"address":"","errCode":"","errMsg":"本日未开机!"}'
                result = json.dumps(msg, ensure_ascii=False)
                return json.loads(result)
            else:
                msg = '{"code":2,"msg":[],"address":"' + (resultData[1])[1] + '","errCode":"' + \
                      (resultData[1])[0] + '","errMsg":"' + (resultData[1])[2] + '"}'
                result = json.dumps(msg,ensure_ascii=False)
                return json.loads(result)
        else:
            df = resultData[1]
            df['StartTimeStr'] = df['StartTime'].apply(lambda x:'NaT' if pd.isnull(x) else x.strftime("%Y-%m-%d %H:%M:%S"))
            df['EndTimeStr'] = df['EndTime'].apply(lambda x: 'NaT' if pd.isnull(x) else x.strftime("%Y-%m-%d %H:%M:%S"))
            daf = df.to_json(orient = 'records', force_ascii = False)
            msg = '{"code":1,"msg":'+daf+',"address":"","errCode":"","errMsg":"成功"}'
            result = json.dumps(msg,ensure_ascii=False)
            return json.loads(result)

@app.route('/zs')


#http://localhost:5000/zs?tags=MES2RTDATA.U_BAL_11010010002.DC_TeamCode,MES2RTDATA.U_CON_11010010003.DC_PCH,MES2RTDATA.U_CON_11010010003.DC_PH,MES2RTDATA.U_BAL_11010010002.DC_LL&freq=60000&startTime=2019-8-9 06:00:00&endTime=2019-8-10 06:00:00&delay=1800
def GetBatchInfoBySegment():
    try:
        rsatrt = dat.datetime.now()
        _freq = request.args.get('freq')
        _startTime = request.args.get('startTime')
        _endTime = request.args.get('endTime')
        _tags = request.args.get('tags')
        _delay = request.args.get('delay')
        tagsList = _tags.split(',')

        resultData = gb_ine.GetBatchInfoBySegment(tagsList,_freq,_startTime,_endTime,int(_delay)) #调用interFace接口
        rend = dat.datetime.now()
        print("***************startTime:" + str(rsatrt) + "   endTime:" + str(rend) + "******************")
    except Exception as e:
        msg = '{"code":2,"msg":[],"address":"app","errCode":"-122","errMsg":"操作异常!' + repr(e).replace('"', " ").replace(
            "'", " ") + '"}'
        result = json.dumps(msg, ensure_ascii=False)
        return json.loads(result)
    else:
        if (resultData[0] == True):
            # True, ['0', 'GetUnitDayProduction', '本日未开机！']
            if ((resultData[1])[0] == '0'):
                msg = '{"code":1,"msg":[],"address":"","errCode":"","errMsg":"本日未开机!"}'
                result = json.dumps(msg, ensure_ascii=False)
                return json.loads(result)
            # else:
            #     msg = '{"code":2,"msg":[],"address":"' + (resultData[1])[1] + '","errCode":"' + \
            #           (resultData[1])[0] + '","errMsg":"' + (resultData[1])[2] + '"}'
            #     result = json.dumps(msg, ensure_ascii=False)
            #     return json.loads(result)
        else:
            df = resultData[1]
            # df['StartTimeStr'] = df['StartTime'].apply(lambda x: 'NaT' if pd.isnull(x) else x.strftime("%Y-%m-%d %H:%M:%S"))
            # df['EndTimeStr'] = df['EndTime'].apply(lambda x: 'NaT' if pd.isnull(x) else x.strftime("%Y-%m-%d %H:%M:%S"))
            daf = df.to_json(orient='records', force_ascii=False)
            msg = '{"code":1,"msg":' + daf + ',"address":"","errCode":"","errMsg":"成功"}'
            result = json.dumps(msg, ensure_ascii=False)
            return json.loads(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,threaded=True,debug=False)
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()