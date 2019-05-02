import base.sql_help as sql_help
import pandas as pd

conn = sql_help.Sql_jc()
str = (" SELECT  e.CHINESE_TEXT,f.CHINESE_TEXT,   case when  b.i is null then 'x' else b.i end as i,case when  b.j is null then 'y' else b.j end as j,a.reg_no AS 飞机注册号, c.unitName AS 保障单位, c.nodeName AS 节点名称, a.node_time AS 节点时间, "
"c.isBridgeName AS 机位类型, c.modelTypeName AS 机型类别, b.CW AS 计划离港时间, b.C AS 实际离港时间, "
"c.TimeMsg AS 保障节点要求时间, DATEDIFF(minute, b.CW, a.node_time) AS 保障节点实际时间, "
"CASE WHEN ISNUMERIC(c.TimeMsg) = 0 THEN '~' WHEN datediff(minute, b.CW, a.node_time) <= CONVERT(float, "
"c.TimeMsg) THEN '正常' WHEN datediff(minute, b.CW, a.node_time) > CONVERT(float, c.TimeMsg) " 
"THEN '异常' ELSE '~' END AS 状态, a.run_date, a.flight_num, c.nodeSort, a.node_time ,datediff(minute,b.cw, b.C) as 计划实际起飞时差" 
"   FROM      dbo.V_MaxDistinctNodes AS a INNER JOIN "
"dbo.t_flightOut AS b ON a.flight_num = b.AU + b.AV AND a.run_date = b.CU AND a.reg_no = b.CQ INNER JOIN " 
"dbo.v_protectionProcessTime AS c ON c.node = a.node AND b.bridge = c.isBridge  INNER JOIN "
"dbo.t_flightRelation AS d ON d.flightModel = b.BG AND d.modelType = c.modelType LEFT JOIN " 
"dbo.b_delayGroupClass AS e ON b.i = e.CATEGORY LEFT JOIN "
"dbo.b_delayClass AS f ON b.j = f.CODE and f.CATEGORY = e.CATEGORY "                 
"order by a.run_date,a.flight_num,c.nodeSort")


def status(_s):
    if (_s=='正常'):
        return False
    elif (_s=='异常'):
        return  True
    elif (_s=='~'):
        return 1
    else:
        return 2


df = conn.ExecQuery(str)

# df1 = df.loc[(df["i"] != 'x')&(df["状态"] == '异常')&(df["机位类型"]=='近') & (df["机型类别"]=='C类机型（61-150）') ,["机型类别","机位类型","run_date","flight_num","i","j","节点名称","状态","保障节点要求时间","保障节点实际时间"]]
# df1['nodeCum'] = int(df1['保障节点实际时间']) - int(df1['保障节点要求时间'])
df1 = df.loc[(df["机位类型"]=='近') & (df["机型类别"]=='C类机型（61-150）') ,["机型类别","机位类型","run_date","flight_num","i","j","节点名称","状态","保障节点要求时间","保障节点实际时间","计划离港时间","实际离港时间","计划实际起飞时差"]]
df2 = df1.groupby(['run_date','flight_num'])

lsNode=list({"机组到位","加油开始","加油结束","开始配餐","配餐完成","机务放行","开始上客","催促登机","上客完成","关客舱门","撤轮挡","实际推出"})

ls = list()
str=""
#研究用数据生成代码
# for name,group in df2:
#     ls1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,False,'a','b',None,None]
#     for i in range(0,group.shape[0],1):
#         if (group.values[i, 6] == '机组到位'):
#             ls1[0] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '加油开始'):
#             ls1[1] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '加油结束'):
#             ls1[2] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '开始配餐'):
#             ls1[3] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '配餐完成'):
#             ls1[4] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '机务放行'):
#             ls1[5] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '开始上客'):
#             ls1[6] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '催促登机'):
#             ls1[7] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '上客完成'):
#             ls1[8] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '关客舱门'):
#             ls1[9] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '撤轮挡'):
#             ls1[10] = status(group.values[i, 7])
#         elif (group.values[i, 6] == '实际推出'):
#             ls1[11] = status(group.values[i, 7])
#
#         if (group.values[i, 4]=='x'):
#             ls1[12] = False
#         else:
#             ls1[12] = True
#         ls1[13] = group.values[i, 2]
#         ls1[14] = group.values[i, 3]
#         ls1[15] = group.values[i, 10]
#         ls1[16] = group.values[i, 11]
#     ls.append(ls1)



for name,group in df2:
    ls1 = [None, None, None, None, None, None, None, None, None, None, None, None,None,'a','b',None,None]
    for i in range(0,group.shape[0],1):
        if (group.values[i, 6] == '机组到位'):
            ls1[0] = group.values[i, 9]
        elif (group.values[i, 6] == '加油开始'):
            ls1[1] = group.values[i, 9]
        elif (group.values[i, 6] == '加油结束'):
            ls1[2] = group.values[i, 9]
        elif (group.values[i, 6] == '开始配餐'):
            ls1[3] =group.values[i, 9]
        elif (group.values[i, 6] == '配餐完成'):
            ls1[4] = group.values[i, 9]
        elif (group.values[i, 6] == '机务放行'):
            ls1[5] = group.values[i, 9]
        elif (group.values[i, 6] == '开始上客'):
            ls1[6] = group.values[i, 9]
        elif (group.values[i, 6] == '催促登机'):
            ls1[7] = group.values[i, 9]
        elif (group.values[i, 6] == '上客完成'):
            ls1[8] = group.values[i, 9]
        elif (group.values[i, 6] == '关客舱门'):
            ls1[9] = group.values[i, 9]
        elif (group.values[i, 6] == '撤轮挡'):
            ls1[10] = group.values[i, 9]
        elif (group.values[i, 6] == '实际推出'):
            ls1[11] = group.values[i, 9]

        ls1[13] = group.values[i, 2]
        ls1[14] = group.values[i, 3]
        ls1[15] = group.values[i, 10]
        ls1[16] = group.values[i, 11]
        ls1[12] = group.values[i, 12]
    ls.append(ls1)





from pandas import  DataFrame
df =DataFrame(ls, columns=["机组到位","加油开始","加油结束","开始配餐","配餐完成","机务放行","开始上客","催促登机","上客完成","关客舱门","撤轮挡","实际推出","航班延误","运行日期","航班号","计划离港时间","实际离港时间"])
df.to_excel("c://jc-t4.xls")