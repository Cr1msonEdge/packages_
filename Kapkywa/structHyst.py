import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

onk = "Онк/Неонк"
onkDict = ["Неонк", "Онк"]
hyst = "Гистологический диагноз"
hystVals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20, 23]
hystOnk = [1, 2, 3, 6, 12, 13, 14, 15]
hystNonOnk = [4, 5, 7, 8, 9, 10, 16, 17, 19, 20, 23]
hystDict = { 1: "Аденокарцинома", 2: "Карциноид", 3: "Плоскоклеточный рак", 4: "Туберкулема", 5: "Гамартома",
             6: "Мукоэпидермоидный рак", 7: "Нетуберкулезный\nмикобактериоз", 8: "Пневмофиброз",
             9: "Пневмония", 10: "Гранулематоз Вегенера",
             12: "Склерозирующая опухоль", 13: "Смешанный рак", 14: "Мелкоклеточный рак", 15: "Гиперплазия",
             16: "Регенционная киста", 17: "Склерозирующая\nгемангиома", 19: "Муцинозная цистаденома",
             20: "Амилоидоз", 23: "Внутрилегочный\nлимфоузел" }
struct = "Структура очага"
structDict = ["Нет", "Кальцинаты", "Кавитация", "Кавитация + кальцинаты", "ВБ"]

df = pd.read_excel("Data_exam.xlsx", header=1)
pd.set_option('display.max_columns', None)

tmpDF = df[[hyst, struct]]

structCountNonOnk = pd.DataFrame({ hyst: [hystDict[x] for x in hystNonOnk],
                                   structDict[0]: [len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 0)]) * 100.0 / len(tmpDF[tmpDF[hyst] == x]) for x in hystNonOnk],
                                   structDict[1]: [len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 1)]) * 100.0 / len(tmpDF[tmpDF[hyst] == x]) for x in hystNonOnk],
                                   structDict[2]: [len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 2)]) * 100.0 / len(tmpDF[tmpDF[hyst] == x]) for x in hystNonOnk],
                                   structDict[3]: [len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 3)]) * 100.0 / len(tmpDF[tmpDF[hyst] == x]) for x in hystNonOnk],
                                   structDict[4]: [len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 4)]) * 100.0 / len(tmpDF[tmpDF[hyst] == x]) for x in hystNonOnk]})
structCountNonOnk = pd.melt(structCountNonOnk, id_vars=[hyst], value_vars=structDict)

structCountOnk = pd.DataFrame({ hyst: [hystDict[x] for x in hystOnk],
                                structDict[0]: [len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 0)]) * 100.0 / len(tmpDF[tmpDF[hyst] == x]) for x in hystOnk],
                                structDict[1]: [len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 1)]) * 100.0 / len(tmpDF[tmpDF[hyst] == x]) for x in hystOnk],
                                structDict[2]: [len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 2)]) * 100.0 / len(tmpDF[tmpDF[hyst] == x]) for x in hystOnk],
                                structDict[3]: [len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 3)]) * 100.0 / len(tmpDF[tmpDF[hyst] == x]) for x in hystOnk],
                                structDict[4]: [len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 4)]) * 100.0 / len(tmpDF[tmpDF[hyst] == x]) for x in hystOnk]})
structCountOnk = pd.melt(structCountOnk, id_vars=[hyst], value_vars=structDict)

colors = [[252 / 255, 198 / 255, 194 / 255], [198 / 255, 217 / 255, 234 / 255], [216 / 255, 240 / 255, 211 / 255],
          [230 / 255, 216 / 255, 234 / 255], [243 / 255, 215 / 255, 177 / 255]]

fig, axes = plt.subplots(1, 2)
axes[0].set_title("Неонкология")
axes[1].set_title("Онкология")
g1 = sns.barplot(ax=axes[0], data=structCountNonOnk, x=hyst, y="value", hue="variable", palette="Pastel1", edgecolor="white")
g2 = sns.barplot(ax=axes[1], data=structCountOnk, x=hyst, y="value", hue="variable", palette="Pastel1", edgecolor="white")
g1.set_xticklabels(labels=[hystDict[x] for x in hystNonOnk], rotation=45, horizontalalignment="right")
g2.set_xticklabels(labels=[hystDict[x] for x in hystOnk], rotation=45, horizontalalignment="right")
g1.set(ylim=(0.0, 100.0), xlabel="", ylabel="")
g2.set(ylim=(0.0, 100.0), xlabel="", ylabel="")
fig.supxlabel(hyst)
fig.supylabel("Процент от общего числа пациентов с диагнозом")
patches = [mpatches.Patch(color=colors[i], label=structDict[i]) for i in range(len(structDict))]
g1.legend(handles=patches, title="Структура очага")
g2.legend(handles=patches, title="Структура очага")
plt.show()