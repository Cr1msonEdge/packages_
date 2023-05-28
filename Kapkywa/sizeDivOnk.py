import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

onk = "Онк/Неонк"
minSize = "Мин. размер, мм"
maxSize = "Макс. размер, мм"
avgSize = "Сред. размер, мм"

df = pd.read_excel("Data_exam.xlsx", header=1)
pd.set_option('display.max_columns', None)

def getGap(val, gapsArg):
    for i in range(len(gapsArg) - 1):
            if val <= gapsArg[i + 1]:
                return "[" + str(int(gapsArg[i] * 100.0)) + "%; " + str(int(gapsArg[i + 1] * 100.0)) + "%]"

def getGap_index(gapsArg, index):
    return "[" + str(int(gapsArg[index] * 100.0)) + "%; " + str(int(gapsArg[index + 1] * 100.0)) + "%]"

    # удалим некорректную запись
tmpDF = df[[onk, minSize, maxSize, avgSize]].drop(index=[219], axis=0)

nonOnkDF = tmpDF[tmpDF[onk] == 0]
nonOnkDF = nonOnkDF.assign(percDiv=(nonOnkDF[maxSize] - nonOnkDF[minSize]) / (nonOnkDF[avgSize] * 2.0))
nonOnkDF = nonOnkDF.sort_values(by="percDiv")
minDiv = nonOnkDF.percDiv.min()
maxDiv = nonOnkDF.percDiv.max()
print(nonOnkDF[nonOnkDF.percDiv == maxDiv])
print(minDiv, maxDiv)
#diff = (maxDiv - minDiv) / 4
gapsNonOnk = [minDiv, 0.07, 0.14, 0.21, maxDiv]
nonOnkDF = nonOnkDF.assign(Deviation=[getGap(nonOnkDF.iloc[i, 4], gapsNonOnk) for i in range(len(nonOnkDF))])
print(nonOnkDF)

onkDF = tmpDF[tmpDF[onk] == 1]
onkDF = onkDF.assign(percDiv=(onkDF[maxSize] - onkDF[minSize]) / (onkDF[avgSize] * 2.0))
onkDF = onkDF.sort_values(by="percDiv")
minDiv = onkDF.percDiv.min()
maxDiv = onkDF.percDiv.max()
print(onkDF[onkDF.percDiv == maxDiv])
print(minDiv, maxDiv)
#diff = (maxDiv - minDiv) / 4.0
gapsOnk = [minDiv, 0.07, 0.14, 0.21, maxDiv]
onkDF = onkDF.assign(Deviation=[getGap(onkDF.iloc[i, 4], gapsOnk) for i in range(len(onkDF))])
print(onkDF)

fig, axes = plt.subplots(2, 1)
axes[0].set_title("Неонкология")
axes[1].set_title("Онкология")

colors = [[252 / 255, 198 / 255, 194 / 255], [198 / 255, 217 / 255, 234 / 255], [216 / 255, 240 / 255, 211 / 255],
          [230 / 255, 216 / 255, 234 / 255], [198 / 255, 233 / 255, 217 / 255], [253 / 255, 217 / 255, 193 / 255],
          [216 / 255, 233 / 255, 237 / 255], [246 / 255, 215 / 255, 234 / 255]]

g = sns.histplot(ax=axes[0], data=nonOnkDF, x=avgSize, hue="Deviation", bins=20, multiple="dodge", shrink=0.8, palette="Pastel1", edgecolor="black")
patches = [mpatches.Patch(color=colors[i], label=getGap_index(gapsNonOnk, i)) for i in range(len(gapsNonOnk) - 1)]
g.legend(handles=patches, title="Процент изменения от среднего")
g.set(xlabel=None, ylabel=None)

g1 = sns.histplot(ax=axes[1], data=onkDF, x=avgSize, hue="Deviation", bins=20, multiple="dodge", shrink=0.8, palette="Pastel2", edgecolor="black")
patches1 = [mpatches.Patch(color=colors[i + len(gapsNonOnk) - 1], label=getGap_index(gapsOnk, i)) for i in range(len(gapsOnk) - 1)]
g1.legend(handles=patches1, title="Процент изменения от среднего")
g1.set(xlabel=None, ylabel=None)

fig.supxlabel("Средний размер, мм")
fig.supylabel("Количество пациентов")

fig.suptitle("Распределение изменения размеров образований от их средней величины")
plt.show()
