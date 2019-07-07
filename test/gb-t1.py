import base.webSocketHelp as ws
import chart.plot as plt
import numpy as np
import pandas as pd
import scipy.signal as sci
import matplotlib.pyplot as pyplot

import base.change_point as cp


df = ws.WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",
                                     "MES2RTDATA.U_Maker_11020030001.DC_SJCL"
                                     "||2019-07-1 6:00:00||2019-07-2 6:00:00||Cyclic||60000")
df1 = ws.WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",
                                     "MES2RTDATA.U_Maker_11020030001.DC_BC"
                                     "||2019-07-1 6:00:00||2019-07-2 6:00:00||Cyclic||3600000")
df2 = ws.WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",
                                     "MES2RTDATA.U_Maker_11020030001.DC_YXSD"
                                     "||2019-07-1 6:00:00||2019-07-2 6:00:00||Cyclic||60000")
# df = ws.WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",
#                                      "MES2RTDATA.U_Maker_11020030001.DC_JTH,MES2RTDATA.U_Maker_11020030001.DC_PH,MES2RTDATA.U_Maker_11020030001.DC_BC,"
#                                      "MES2RTDATA.U_Maker_11020030001.DC_YXSD,MES2RTDATA.U_Maker_11020030001.DC_LLCL,MES2RTDATA.U_Maker_11020030001.DC_SJCL,"
#                                      "MES2RTDATA.U_Maker_11020030001.DC_ZCL,MES2RTDATA.U_Maker_11020030001.DC_FPL,MES2RTDATA.U_Maker_11020030001.DC_LYL,"
#                                      "MES2RTDATA.U_Maker_11020030001.DC_XL,MES2RTDATA.U_Maker_11020030001.DC_TJCS,MES2RTDATA.U_Maker_11020030001.DC_DQBCJSSJ,"
#                                      "MES2RTDATA.U_Maker_11020030001.DC_DQBCKSSJ"
#                                      "||2019-07-3 0:00:00||2019-07-5 6:00:00||Cyclic||3600000")
#
# df2 = ws.WebSocketHelp.RowToColumn(df, 'TagName', 'vValue', _indexName='DateTime', _havIndex=True)


# plt.zsParmPlot(df.values[:,2].astype(np.float))

# print(cp.Pettitt_change_point_detection(df.values[:,2].astype(np.float)))
vector = df.values[:,2].astype(np.float)
vector1=df1.values[:,2].astype(np.float)
vector2=df2.values[:,2].astype(np.float)
#indexes  = sci.find_peaks_cwt(df.values[:,2].astype(np.float),np.arange(1, 4),max_distances=np.arange(1, 4)*2)

#indexes = sci.argrelextrema(df.values[:,2].astype(np.float),comparator=np.greater,order=2)

indexes, _ = sci.find_peaks(vector, height=7, distance=2.1)
print('Peaks are: %s' % (indexes))

y = df.values[indexes,2].astype('float')

# vector = [vector,df1.values[:,2].astype(np.float)]
pyplot.figure()
pyplot.subplot(311)
pyplot.plot(range(0,len(vector),1),vector,'r-')
pyplot.scatter(indexes,y)
pyplot.subplot(312)
pyplot.plot(range(0,len(vector1),1),vector1,'r-')
pyplot.subplot(313)
pyplot.plot(range(0,len(vector2),1),vector2,'r-')
pyplot.show()
# print(indexes)