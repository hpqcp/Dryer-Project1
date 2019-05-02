
import base.sql_help as sql_help


conn = sql_help.Sql_jc()
str = ("  SELECT  b.i ,b.J, a.reg_no AS 飞机注册号, c.unitName AS 保障单位, c.nodeName AS 节点名称, a.node_time AS 节点时间, "
                "c.isBridgeName AS 机位类型, c.modelTypeName AS 机型类别, b.CW AS 计划离港时间, b.C AS 实际离港时间, "
                "c.TimeMsg AS 保障节点要求时间, DATEDIFF(minute, b.CW, a.node_time) AS 保障节点实际时间, "
                "CASE WHEN ISNUMERIC(c.TimeMsg) = 0 THEN '' WHEN datediff(minute, b.CW, a.node_time) <= CONVERT(float,"
                "c.TimeMsg) THEN '正常' WHEN datediff(minute, b.CW, a.node_time) > CONVERT(float, c.TimeMsg) "
               " THEN '异常' ELSE '' END AS 状态, a.run_date, a.flight_num, c.nodeSort, a.node_time "
                   " FROM      dbo.V_MaxDistinctNodes AS a INNER JOIN "
                " dbo.t_flightOut AS b ON a.flight_num = b.AU + b.AV AND a.run_date = b.CU AND a.reg_no = b.CQ INNER JOIN "
                " dbo.v_protectionProcessTime AS c ON c.node = a.node AND b.bridge = c.isBridge INNER JOIN "
            " dbo.t_flightRelation AS d ON d.flightModel = b.BG AND d.modelType = c.modelType "
                " WHERE b.i is not null "
                " order by a.run_date,a.reg_no")

df = conn.ExecQuery(str)

df1 = df.loc[df["状态"] == '异常',["run_date","flight_num","节点名称","机位类型","机型类别"]]
df2 = df1.groupby(['run_date','flight_num'])
ls = list()
for name,group in df2:
    ls1 = list()
    for i in range(0,group.shape[0],1):
        ls1.append(group.values[i,2])
    ls.append(ls1)

from pandas import  DataFrame

# from pymining import itemmining
# relim_input = itemmining.get_relim_input(ls)
# report = itemmining.relim(relim_input, min_support=100)
# ls_1 = list()
# ls_2 = list()
# for it in report:
#     ls_1.append(it)
#     ls_2.append(report[it])

# df =DataFrame({"a":ls_1,"b":ls_2})
# df = df.sort_values(by='b',ascending=False)
# df.to_excel("c://jc2.xls")
print(ls)

# from pymining import itemmining, assocrules, perftesting
# # transactions = perftesting.get_default_transactions()
# relim_input = itemmining.get_relim_input(ls)
# item_sets = itemmining.relim(relim_input, min_support=3)
# rules = assocrules.mine_assoc_rules(item_sets, min_support=3, min_confidence=0.5)
# print(rules)

# import orangecontrib.associate.fpgrowth as oaf  #进行关联规则分析的包
# # fpgrowth.frequent_itemsets(X, min_support=0.2)
# itemsets = oaf.frequent_itemsets(ls,min_support=3)
# # a = list(itemsets)
# # itemsets = dict(itemsets) #这里设置支持度
# rules = oaf.association_rules(itemsets,)   #这里设置置信度
# # rules = list(rules)
# print(rules)

# from fp_growth import find_frequent_itemsets
# for itemset in find_frequent_itemsets(ls, 0.5):
#     print(itemset)

# import fp_growth as fp
# items = fp.find_frequent_itemsets(ls,3)
# print(items)

from orangecontrib.associate.fpgrowth import *
itemsets = dict(frequent_itemsets(ls))
print(list(itemsets))