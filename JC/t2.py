import base.sql_help as sql_help

conn = sql_help.Sql_jc()
str = (" SELECT  e.CHINESE_TEXT,f.CHINESE_TEXT,   case when  b.i is null then 'x' else b.i end as i,case when  b.j is null then 'y' else b.j end as j,a.reg_no AS 飞机注册号, c.unitName AS 保障单位, c.nodeName AS 节点名称, a.node_time AS 节点时间, "
"c.isBridgeName AS 机位类型, c.modelTypeName AS 机型类别, b.CW AS 计划离港时间, b.C AS 实际离港时间, "
"c.TimeMsg AS 保障节点要求时间, DATEDIFF(minute, b.CW, a.node_time) AS 保障节点实际时间, "
"CASE WHEN ISNUMERIC(c.TimeMsg) = 0 THEN '~' WHEN datediff(minute, b.CW, a.node_time) <= CONVERT(float, "
"c.TimeMsg) THEN '正常' WHEN datediff(minute, b.CW, a.node_time) > CONVERT(float, c.TimeMsg) " 
"THEN '异常' ELSE '~' END AS 状态, a.run_date, a.flight_num, c.nodeSort, a.node_time " 
"   FROM      dbo.V_MaxDistinctNodes AS a INNER JOIN "
"dbo.t_flightOut AS b ON a.flight_num = b.AU + b.AV AND a.run_date = b.CU AND a.reg_no = b.CQ INNER JOIN " 
"dbo.v_protectionProcessTime AS c ON c.node = a.node AND b.bridge = c.isBridge  INNER JOIN "
"dbo.t_flightRelation AS d ON d.flightModel = b.BG AND d.modelType = c.modelType LEFT JOIN " 
"dbo.b_delayGroupClass AS e ON b.i = e.CATEGORY LEFT JOIN "
"dbo.b_delayClass AS f ON b.j = f.CODE and f.CATEGORY = e.CATEGORY "                 
"order by a.run_date,a.flight_num,c.nodeSort")




df = conn.ExecQuery(str)

# df1 = df.loc[(df["i"] != 'x')&(df["状态"] == '异常')&(df["机位类型"]=='近') & (df["机型类别"]=='C类机型（61-150）') ,["机型类别","机位类型","run_date","flight_num","i","j","节点名称","状态","保障节点要求时间","保障节点实际时间"]]
# df1['nodeCum'] = int(df1['保障节点实际时间']) - int(df1['保障节点要求时间'])
df1 = df.loc[(df["i"] != 'x')&(df["状态"] == '异常')&(df["机位类型"]=='近') & (df["机型类别"]=='C类机型（61-150）') ,["机型类别","机位类型","run_date","flight_num","i","j","节点名称","状态","保障节点要求时间","保障节点实际时间"]]
df2 = df1.groupby(['run_date','flight_num'])
ls = list()
str=""
for name,group in df2:

    for i in range(0,group.shape[0],1):
        if (i  == group.shape[0] - 1):
            str = str + group.values[i, 6]
        else:
            str=str + group.values[i,6]+","
    ls.append(str)
    str=""

from pandas import  DataFrame
df =DataFrame({"a":ls})
df.to_excel("c://jc-t1.xls")

from collections import Counter
result = Counter(ls)
print(result.most_common(30))


print(ls)

# lsNode=list({"机组到位","加油开始","加油结束","开始配餐","配餐完成","机务放行","开始上客","催促登机","上客完成","关客舱门","撤轮挡","实际推出"})
# for name,group in df2:
#     ls1 = list()
#     ls1.append('a'+group.values[0, 4])
#     ls1.append('b'+group.values[0, 5])
#     for i in range(0,group.shape[0],1):
#         ls1.append(group.values[i,6])
#         x=0
#         for j in lsNode:
#             if (j == group.values[i,6]):
#
#             x=x+1
#
#     ls.append(ls1)
#
#
# from pandas import  DataFrame
#
# from pymining import itemmining
# relim_input = itemmining.get_relim_input(ls)
# report = itemmining.relim(relim_input, min_support=5)
# ls_1 = list()
# ls_2 = list()
# for it in report:
#     ls_1.append(it)
#     ls_2.append(report[it])
#
# df =DataFrame({"a":ls_1,"b":ls_2})
# df = df.sort_values(by='b',ascending=False)
# df.to_excel("c://jc4.xls")