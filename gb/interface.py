

#获取卷包单元（卷接、小包、条包、提升机等）日产量信息
#   _type : 单元类型 string , 'jj' : 卷接 ,'xb' :小包 , 'tb' : 条包
def GetUnitDayProduction(_type , _startTime , _endTime , _tags):

    #1 . 判断参数_type
    if _type == 'jj' :
        threshold = 5000     #临界值，根据单元类型不同，赋予不同数值
    elif _type == 'xb'   :
        threshold = 300
    elif _type == 'tb'   :
        threshold = 50
    else :
        return True,['-101','GetUnitDayProduction','参数_type没有传入已知的类型！']

    #2 . 准备
