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
smoke = "Анамнез курения"

df = pd.read_excel("Data_exam.xlsx", header=1)
pd.set_option('display.max_columns', None)

tmpDF = df[[hyst, smoke, suvOchF]]
suvNonSmoke = "suvNonSmoke"
suvSmoke = "suvSmoke"

suvMeanNonOnk = pd.DataFrame({ hyst: [hystDict[x] for x in hystNonOnk],
                               suvNonSmoke: [tmpDF[(tmpDF[hyst] == x) & (tmpDF[smoke] == 0)][suvOchF].mean() for x in hystNonOnk],
                               suvSmoke: [tmpDF[(tmpDF[hyst] == x) & (tmpDF[smoke] == 1)][suvOchF].mean() for x in hystNonOnk]}).dropna()
suvMeanNonOnk = pd.melt(suvMeanNonOnk, id_vars=[hyst], value_vars=[suvNonSmoke, suvSmoke])

suvMeanOnk = pd.DataFrame({ hyst: [hystDict[x] for x in hystOnk],
                            suvNonSmoke: [tmpDF[(tmpDF[hyst] == x) & (tmpDF[smoke] == 0)][suvOchF].mean() for x in hystOnk],
                            suvSmoke: [tmpDF[(tmpDF[hyst] == x) & (tmpDF[smoke] == 1)][suvOchF].mean() for x in hystOnk]}).dropna()
suvMeanOnk = pd.melt(suvMeanOnk, id_vars=[hyst], value_vars=[suvNonSmoke, suvSmoke])

colors = [[252 / 255, 198 / 255, 194 / 255], [198 / 255, 217 / 255, 234 / 255]]

fig, axes = plt.subplots(1, 2)
axes[0].set_title("Неонкология")
axes[1].set_title("Онкология")
g1 = sns.barplot(ax=axes[0], data=suvMeanNonOnk, x=hyst, y="value", hue="variable", palette="Pastel1", edgecolor="white")
g2 = sns.barplot(ax=axes[1], data=suvMeanOnk, x=hyst, y="value", hue="variable", palette="Pastel1", edgecolor="white")
tmpHystNonOnk = [4, 5, 7, 8, 9, 10, 16, 17]
tmpHystOnk = [1, 2, 3, 13, 14]
g1.set_xticklabels(labels=[hystDict[x] for x in tmpHystNonOnk], rotation=45, horizontalalignment="right")
g2.set_xticklabels(labels=[hystDict[x] for x in tmpHystOnk], rotation=45, horizontalalignment="right")
g1.set(ylim=(0.0, 16.5), xlabel="", ylabel="")
g2.set(ylim=(0.0, 16.5), xlabel="", ylabel="")
fig.supxlabel(hyst)
fig.supylabel("Значение")
patches = [mpatches.Patch(color=colors[0], label="Некурящие"),
           mpatches.Patch(color=colors[1], label="Курящие")]
g1.legend(handles=patches, title="SUV_18F очаг")
g2.legend(handles=patches, title="SUV_18F очаг")
plt.show()