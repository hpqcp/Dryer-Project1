from pyecharts.charts import Line
from pyecharts import options as opts
import utils.excel2redis as rds
import sshc.timeAlignment as timeAlign
import numpy as np
import pandas as pd

df = rds.getBatchData('4000-2019-10-08*', 1)
df1 = pd.DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
df2 = pd.DataFrame(df1, dtype=np.float)
pointDiffList = [0, 80, 34, 17, 52, 14, 3, 21, 52]
df3 = timeAlign.time_align_transform(df2, pointDiffList)
df_y = df3.values[:, 0]
df_x = df3.values[:, 1:]

from sklearn.externals import joblib
from sshc.modelPredict import randomForest_predict_score

model = joblib.load('c://model1.m')
ssx = joblib.load('c://ssx1.m')
ssy = joblib.load('c://ssy1.m')
_,df_p = randomForest_predict_score(model, ssx, ssy, df_x, df_y, _isPlot=False)
xSeries=[]
x1=[]
for n in range(0,200,1):
    x1.append(n)
for n in range(0,280,1):
    xSeries.append(n)

# V1 版本开始支持链式调用
Line = (
    Line()
    .add_xaxis(xSeries)
    .add_yaxis("实际A", df_p.values[0:200,0],label_opts=None)
    .add_yaxis("预测B", df_p.values[0:280,1],label_opts=None)
    .set_global_opts(title_opts=opts.TitleOpts(title="SSHC"))
)
Line.render()

# # 不习惯链式调用的开发者依旧可以单独调用方法
# bar = Bar()
# bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
# bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
# bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
# bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
# bar.render()