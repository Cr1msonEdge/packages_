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
suvOchSizeF = "SUVочаг/размер_18F"
suvOchLungF = "SUVочаг/SUVлегк_18F"
suvOchPoolF = "SUVочаг/SUVпул_18F"

df = pd.read_excel("Data_exam.xlsx", header=1)
pd.set_option('display.max_columns', None)

tmpDF = df[[hyst, suvOchSizeF, suvOchLungF, suvOchPoolF]]

suvMeanNonOnk = pd.DataFrame({ hyst: [hystDict[x] for x in hystNonOnk],
                               suvOchSizeF: [tmpDF[tmpDF[hyst] == x][suvOchSizeF].mean() for x in hystNonOnk],
                               suvOchLungF: [tmpDF[tmpDF[hyst] == x][suvOchLungF].mean() for x in hystNonOnk],
                               suvOchPoolF: [tmpDF[tmpDF[hyst] == x][suvOchPoolF].mean() for x in hystNonOnk]})
suvMeanNonOnk = pd.melt(suvMeanNonOnk, id_vars=[hyst], value_vars=[suvOchSizeF, suvOchLungF, suvOchPoolF])

suvMeanOnk = pd.DataFrame({ hyst: [hystDict[x] for x in hystOnk],
                            suvOchSizeF: [tmpDF[tmpDF[hyst] == x][suvOchSizeF].mean() for x in hystOnk],
                            suvOchLungF: [tmpDF[tmpDF[hyst] == x][suvOchLungF].mean() for x in hystOnk],
                            suvOchPoolF: [tmpDF[tmpDF[hyst] == x][suvOchPoolF].mean() for x in hystOnk]})
suvMeanOnk = pd.melt(suvMeanOnk, id_vars=[hyst], value_vars=[suvOchSizeF, suvOchLungF, suvOchPoolF])

colors = [[252 / 255, 198 / 255, 194 / 255], [198 / 255, 217 / 255, 234 / 255], [216 / 255, 240 / 255, 211 / 255]]

fig, axes = plt.subplots(1, 2)
axes[0].set_title("Неонкология")
axes[1].set_title("Онкология")
g1 = sns.barplot(ax=axes[0], data=suvMeanNonOnk, x=hyst, y="value", hue="variable", palette="Pastel1")
g2 = sns.barplot(ax=axes[1], data=suvMeanOnk, x=hyst, y="value", hue="variable", palette="Pastel1")
g1.set_xticklabels(labels=[hystDict[x] for x in hystNonOnk], rotation=45, horizontalalignment="right")
g2.set_xticklabels(labels=[hystDict[x] for x in hystOnk], rotation=45, horizontalalignment="right")
g1.set(ylim=(0.0, 32.0), xlabel="", ylabel="")
g2.set(ylim=(0.0, 32.0), xlabel="", ylabel="")
fig.supxlabel(hyst)
fig.supylabel("Значение")
patches = [mpatches.Patch(color=colors[0], label=suvOchSizeF),
           mpatches.Patch(color=colors[1], label=suvOchLungF),
           mpatches.Patch(color=colors[2], label=suvOchPoolF)]
g1.legend(handles=patches, title="Соотношения")
g2.legend(handles=patches, title="Соотношения")

plt.show()