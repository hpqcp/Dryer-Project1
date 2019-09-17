import gb.excelProcess as excelPro
import datetime
import time


def everyDayJob(_h=0, _m=0,_factoryInfo=None,_startTime='05:00:00',_endTime='05:00:00',_productDate=''):
    '''h表示设定的小时，m为设定的分钟'''
    if _h is None or _m is None :
        while True:
            now = datetime.datetime.now()
            # 到达设定时间，结束内循环
            if now.hour==_h and now.minute==_m:
                break
            # 不到时间就等20秒之后再次检测
            time.sleep(60)



    for i in range(0,len(_factoryInfo),1) :
        f = _factoryInfo[i]
        dir = f[0]
        excelStr = f[1]
        sheetName = f[2]
        if _productDate=='' :
            eDate = str(datetime.datetime.now().date())
            sDate = str(datetime.datetime.now().date()-datetime.timedelta(days=1))
        else:
            sDate = _productDate
            eDate = str(datetime.datetime.strptime(_productDate,'%Y-%m-%d').date()+datetime.timedelta(days=1))
        sTime = sDate+' '+ _startTime
        eTime = eDate+' '+ _endTime
        excelPro.DayProductionByExcelFactory(dir,excelStr,sheetName,sTime,eTime)

if __name__ == "__main__":
    # deltailInfo = [[ "d://jb//ky//",'ky.xlsx','ky'],["d://jb//hy//",'hy.xlsx','Sheet1'],[ "d://jb//qy//",'qy.xlsx','Sheet1'], \
    #     ["d://jb//hz//", 'hz.xlsx', 'hz'], ["d://jb//xj//", 'xj.xlsx', 'xj'], ["d://jb//wl//", 'wl.xlsx', 'wl']]
    deltailInfo =[["d://jb//wl//", 'wl.xlsx', 'wl']]
    everyDayJob(_factoryInfo=deltailInfo,_productDate='2019-9-5',_startTime='5:00:00',_endTime='8:00:00')