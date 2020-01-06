# import numpy as np
# import pandas as pd
import matplotlib.pyplot as pyplot

#多曲线在同一plot上
def pairPlot(_df,_ylim=[],_title=""):
    colNum = _df.shape[1]
    xNum = _df.shape[0]
    if colNum<1 :
        return -1
    pyplot.title=_title
    for i in range(0,colNum,1):
        pyplot.plot(range(0,xNum,1),_df.values[:,i])
    if _ylim:
        pyplot.ylim(_ylim)
    pyplot.show()
    return 0

#多subplot,每列数据一个subplot
def singlePlot(_df,_name=[],_ylim=[],_title=""):
    colNum = _df.shape[1]
    if colNum<1 :
        return -1
    pyplot.figure()
    pyplot.suptitle(_title)
    for i in range(0,colNum ,1):
        pyplot.subplot(int(colNum), 1, i+1)
        pyplot.plot(_df.iloc[:,i])
        if _name :
            pyplot.title(_name[i], y=1, loc='right')
        if _ylim :
            pyplot.ylim(_ylim)

    pyplot.show()
    return 0



def zsParmPlot(_series,_vline=[],_title=""):
    pyplot.figure()
    pyplot.suptitle(_title)
    pyplot.plot(_series)
    if _vline :
        [pyplot.axvline(_vline[i]) for i in range(0, len(_vline), 1)][:]
    pyplot.show()
    return  0
