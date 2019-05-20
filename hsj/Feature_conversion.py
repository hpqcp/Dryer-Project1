import base.data_transform as bsTrans

from pandas import DataFrame


##########
#1、从Rides获取数据
import utils.excel2redis as rds

# 批次
batchStr = "t1zc0000*"
# 获取批次数据
#[切叶丝含水率、叶丝增温增湿工艺流量、叶丝增温增湿蒸汽流量、薄板干燥热风温度、薄板干燥Ⅰ区筒壁温度、
# 薄板干燥Ⅱ区筒壁温度、薄板干燥出料含水率、薄板干燥出料温度、叶丝冷却出料含水率]
df = rds.getBatchData(batchStr, 0)
df = DataFrame(df.values[:, [1,2,3,4,5,6,7,8,9]])


############
#2、对齐各参数点距离（秒）
putTimes = [425, 440, 449, 0, 515, 561, 786, 804, 845]
df1 = bsTrans.data_alignment(df, putTimes) #各参数点时间对齐
df1 = df1.astype(float)


#############
#3、数据标准化
from sklearn.preprocessing import StandardScaler
# 标准化，返回值为标准化后的数据
df2 = StandardScaler().fit_transform(df1)

# #########################################
# #3、特征选取 - 方差法
# from sklearn.feature_selection import VarianceThreshold
# # 方差选择法，返回值为特征选择后的数据
# # 参数threshold为方差的阈值
# filter1 = VarianceThreshold(threshold=1).fit_transform(df2)
# print(filter1)

