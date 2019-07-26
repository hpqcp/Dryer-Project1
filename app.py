from flask import Flask
from flask import request
import json
import JC.jc_predict as jc_pre
import gb.interface as gb_ine
app = Flask(__name__)


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
        _type = request.args.get('_type')
        _startTime = request.args.get('type')
        _endTime = request.args.get('_type')
        _tags = request.args.get('type')
        resultData = gb_ine.GetUnitDayProduction(_type , _startTime , _endTime , _tags)
        #True, ['-101', 'GetUnitDayProduction', '参数_type没有传入已知的类型！']
    except Exception:
        msg = '{"code":2,"msg":"操作异常!",address:"app",errCode:"-79"}'
        result = json.dumps(msg)
        return result
    else:
        if (resultData[0] == True):
            msg = '{"code":2,"msg":"' + (resultData[1])[2] + '",address:"' + (resultData[1])[1] + '",errCode:"' + \
                  (resultData[1])[0] + '"}'
            result = json.dumps(msg)
            return result
        else:
            msg = '{"code":2,"msg":"' + (resultData[1])[2] + '",address:"' + (resultData[1])[1] + '",errCode:"' + \
                  (resultData[1])[0] + '"}'
            result = json.dumps(msg)
            return result
if __name__ == '__main__':
    app.run()
