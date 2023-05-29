import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

hyst = "Гистологический диагноз"
onk = "Онк/Неонк"
hystVals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20, 23]
hystOnk = [1, 2, 3, 6, 12, 13, 14, 15]
hystNonOnk = [4, 5, 7, 8, 9, 10, 16, 17, 19, 20, 23]
hystDict = { 1: "Аденокарцинома", 2: "Карциноид", 3: "Плоскоклеточный рак", 4: "Туберкулема", 5: "Гамартома",
             6: "Мукоэпидермоидный рак", 7: "Нетуберкулезный\nмикобактериоз", 8: "Пневмофиброз",
             9: "Пневмония", 10: "Гранулематоз Вегенера",
             12: "Склерозирующая опухоль", 13: "Смешанный рак", 14: "Мелкоклеточный рак", 15: "Гиперплазия",
             16: "Регенционная киста", 17: "Склерозирующая\nгемангиома", 19: "Муцинозная цистаденома",
             20: "Амилоидоз", 23: "Внутрилегочный\nлимфоузел" }
suvOchF = "SUVочаг_18F"
suvOchC = "SUVочаг_11С"

df = pd.read_excel("Data_exam.xlsx", header=1)
pd.set_option('display.max_columns', None)

tmpDF = df[[hyst, suvOchF, suvOchC]]

newC = []
for i in range(len(tmpDF)):
    newVal = tmpDF.iloc[i, 2]
    if type(newVal) == str:
        newVal = np.NaN
    newC.append(newVal)

tmpDF.iloc[:, 2] = newC

suvMeanNonOnk = pd.DataFrame({ hyst: [hystDict[x] for x in hystNonOnk],
                               suvOchF: [tmpDF[tmpDF[hyst] == x][suvOchF].dropna().mean() for x in hystNonOnk],
                               suvOchC: [tmpDF[tmpDF[hyst] == x][suvOchC].dropna().mean() for x in hystNonOnk]}).fillna(0)
suvMeanNonOnk = pd.melt(suvMeanNonOnk, id_vars=[hyst], value_vars=[suvOchF, suvOchC])

suvMeanOnk = pd.DataFrame({ hyst: [hystDict[x] for x in hystOnk],
                            suvOchF: [tmpDF[tmpDF[hyst] == x][suvOchF].dropna().mean() for x in hystOnk],
                            suvOchC: [tmpDF[tmpDF[hyst] == x][suvOchC].dropna().mean() for x in hystOnk]}).fillna(0)
suvMeanOnk = pd.melt(suvMeanOnk, id_vars=[hyst], value_vars=[suvOchF, suvOchC])

colors = [[252 / 255, 198 / 255, 194 / 255], [198 / 255, 217 / 255, 234 / 255]]

fig, axes = plt.subplots(1, 2)
axes[0].set_title("Неонкология")
axes[1].set_title("Онкология")
g1 = sns.barplot(ax=axes[0], data=suvMeanNonOnk, x=hyst, y="value", hue="variable", palette="Pastel1")
g2 = sns.barplot(ax=axes[1], data=suvMeanOnk, x=hyst, y="value", hue="variable", palette="Pastel1")
g1.set_xticklabels(labels=[hystDict[x] for x in hystNonOnk], rotation=45, horizontalalignment="right")
g2.set_xticklabels(labels=[hystDict[x] for x in hystOnk], rotation=45, horizontalalignment="right")
g1.set(ylim=(0.0, 14.5), xlabel="", ylabel="")
g2.set(ylim=(0.0, 14.5), xlabel="", ylabel="")
fig.supxlabel(hyst)
fig.supylabel("Значение")
patches = [mpatches.Patch(color=colors[0], label="18F"),
           mpatches.Patch(color=colors[1], label="11C")]
g1.legend(handles=patches, title="SUV очаг")
g2.legend(handles=patches, title="SUV очаг")
plt.show()