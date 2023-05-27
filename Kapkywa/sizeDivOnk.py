import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

onk = "Онк/Неонк"
minSize = "Мин. размер, мм"
maxSize = "Макс. размер, мм"
avgSize = "Сред. размер, мм"

df = pd.read_excel("Data_exam.xlsx", header=1)
pd.set_option('display.max_columns', None)

def getGap(val, gaps):
    for i in range(len(gaps) - 1):
        if (val <= gaps[i + 1]):
            return "[" + str(int(gaps[i] * 100.0)) + "%; " + str(int(gaps[i + 1] * 100.0)) + "%]"

tmpDF = df[[onk, minSize, maxSize, avgSize]].drop(index=[219], axis=0)

nonOnkDF = tmpDF[tmpDF[onk] == 0]
nonOnkDF = nonOnkDF.assign(percDiv = (nonOnkDF[maxSize] - nonOnkDF[minSize]) / (nonOnkDF[avgSize] * 2.0))
minDiv = nonOnkDF.percDiv.min()
maxDiv = nonOnkDF.percDiv.max()
print(nonOnkDF[nonOnkDF.percDiv == maxDiv])
print(minDiv, maxDiv)
diff = (maxDiv - minDiv) / 4.0
gaps = [minDiv, minDiv + diff, minDiv + diff * 2.0, minDiv + diff * 3.0, maxDiv]
nonOnkDF = nonOnkDF.assign(Deviation = [getGap(nonOnkDF.iloc[i, 4], gaps) for i in range(len(nonOnkDF))])
print(nonOnkDF)


onkDF = tmpDF[tmpDF[onk] == 1]
onkDF = onkDF.assign(percDiv = (onkDF[maxSize] - onkDF[minSize]) / (onkDF[avgSize] * 2.0))
minDiv = onkDF.percDiv.min()
maxDiv = onkDF.percDiv.max()
print(onkDF[onkDF.percDiv == maxDiv])
print(minDiv, maxDiv)
diff = (maxDiv - minDiv) / 4.0
gaps = [minDiv, minDiv + diff, minDiv + diff * 2.0, minDiv + diff * 3.0, maxDiv]
onkDF = onkDF.assign(Deviation = [getGap(onkDF.iloc[i, 4], gaps) for i in range(len(onkDF))])
print(onkDF)

fig, axes = plt.subplots(2, 1)
axes[0].set_title("Неонкология")
axes[1].set_title("Онкология")

sns.histplot(ax=axes[0], data=nonOnkDF, x=avgSize, hue="Deviation", bins=20, multiple="dodge", shrink=0.9)
sns.histplot(ax=axes[1], data=onkDF, x=avgSize, hue="Deviation", bins=20, multiple="dodge", shrink=0.9)
plt.show()