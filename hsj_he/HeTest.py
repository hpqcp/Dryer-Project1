import pandas as pd
import os
import sys
import requests
import time

def all_path(dirname):
    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        if(dirname==maindir):
            continue
        #print("1:",maindir) #当前主目录
        #print("2:",subdir) #当前主目录下的所有目录
        #print("3:",file_name_list)  #当前主目录下的所有文件
        #for filename in file_name_list:
            #apath = os.path.join(maindir, filename)#合并成一个完整路径
        result.append(maindir)
    return result

#所有文件
def allfilepath(dirname):
    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        if(dirname==maindir):
            continue
        #print("1:",maindir) #当前主目录
        #print("2:",subdir) #当前主目录下的所有目录
        #print("3:",file_name_list)  #当前主目录下的所有文件
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            result.append(apath)
    return result
BASEURL = 'http://10.130.65.221:6666'
#获取对应关系
path = "D:\data1\FROM\烘丝机数采NEW.csv"
csv_data = pd.read_csv(path, low_memory = False)#防止弹出警告
csv_df = pd.DataFrame(csv_data)
#获取目录下所有文件
fileList=allfilepath("D:\data1\TO\TO");
#for dir in dirList:
#    onefileList = all_path(dir)
#    for file in onefileList:
#        fileList.append(file)
#按照对应关系读取文件
allDataDf = pd.DataFrame(columns=['采集时间', '实时值', '计算值','TagName','ParName'])
for ImIndex, ImRow in csv_df.iterrows():
    ParName = ImRow['NAME']
    TagName = ImRow['VAL']
    for filepath in fileList:
        arr = filepath.split('\\')
        fileName=arr[len(arr)-1]
        if(ParName==fileName):
            csvfiledata = pd.read_csv(filepath, low_memory=False)  # 防止弹出警告
            csvfiledf = pd.DataFrame(csvfiledata)
            csvfiledf['TagName'] = TagName
            csvfiledf['ParName'] = ParName
            allDataDf = allDataDf.append(csvfiledf,ignore_index=True)
#将数据存入数据库
resultNum=100
resultList=[]
i=0
str1=''
for ImIndex, ImRow in allDataDf.iterrows():
    timeArray = time.strptime(ImRow['采集时间'], "%Y/%m/%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    str1 = str1 + 'hsj,tag_name=' + ImRow['TagName']+' value='+str(ImRow['实时值'])+',vvalue='+str(ImRow['计算值'])+',time='+str(timeStamp)+'\n'
    #+',par_name='+ImRow['ParName']
    #s = '''hsj,tag_name=server01 value=123,vvalue=321,time=1434055562000000000'''+'\n'
    i=i+1
    if(i>=resultNum):
        resultList.append(str1)
        i=0
        str1=''
for resultStr in resultList:
    resp = requests.post(BASEURL + '/write', params={'db': 'test_db'}, data=resultStr)
    print(resp.status_code)

print()

