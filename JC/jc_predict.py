from pandas import DataFrame
import numpy as np
import base.data_preProcess as bsPre
import base.data_transform as bsTrans
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.externals import joblib
import warnings
warnings.filterwarnings("ignore")


def predict(nodes):
    model_file_1 = [["01","02","03","04","05","06"],["12","13","14","15","16"],["23","24","25","26"],["34","35","36"],["45","46"],["56"]]
    xCols = {"01":[0, 1],"02": [0, 2],"03": [0, 3],"04": [0, 4], "05":[0, 5],"06": [0, 6], \
             "12":[0, 1, 2], "13":[0, 1, 3],"14": [1, 4],"15": [0, 5], "16":[0, 1, 6], \
             "23":[0, 1, 2, 3], "24":[1, 2, 4],"25": [0, 5],"26": [0, 1, 2, 6], \
             "34":[0, 1, 2, 3, 4],"35": [0, 5], "36":[0, 1, 2, 3, 6], \
             "45":[0, 5],"46": [0, 1, 2, 3, 4, 6], \
             "56":[0, 1, 2, 3, 4, 5, 6]}

    r2 = [[0.96163478772177,0.914957694681475,0.681504569,0.719322649,0.475903522,0.866077792], \
          [0.924598852205082,0.708540895756463,0.741623476298061,0.475903522,0.814353333720976], \
          [0.746888547014805,0.747623246911593,0.475903522,0.821121815035477], \
          [0.806003279425741,0.475903522,0.802051752798695],[0.475903522,0.818602492091022],[0.856151666051536]]
    i=len(nodes)
    predictResult = list()
    if (i <= 0):
        return  None
    else:
        for f in model_file_1[i-1]:
            fileName = "c://jc_model//jc_" + f + ".m"
            rf =joblib.load(fileName)
            col = xCols[f]
            lsP=list()
            for s in range(0,len(col) - 1,1):
                lsP.append(nodes[col[s]])
            p = rf.predict([lsP])
            predictResult.append(p)

    return  predictResult,r2[i-1]


if __name__ == "__main__":
    ls = [-58]
    p=predict(ls)
    print(p)
