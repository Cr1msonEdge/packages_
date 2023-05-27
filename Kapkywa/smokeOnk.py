import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

onk = "Онк/Неонк"
onkDict = ["Неонк", "Онк"]
age = "Возраст, лет"
smoke = "Анамнез курения"
smokeDict = ["Некур", "Кур"]

df = pd.read_excel("Data_exam.xlsx", header=1)
print(pd.pivot_table(df[[onk, smoke]], index=smoke, columns=onk, aggfunc=len))

#tmpDF = df[[onk, age, smoke]]
#tmpDF = tmpDF.assign(OnkSmoke = [smokeDict[tmpDF.iloc[i, 2]] + "/" + onkDict[tmpDF.iloc[i, 0]] for i in range(len(tmpDF))])
#print(tmpDF)
#sns.histplot(data=tmpDF, x=age, hue="OnkSmoke", bins=12, multiple="dodge", shrink=0.9)
#plt.show()

fig, axes = plt.subplots(1, 2)
axes[0].set_title("Некурящие")
axes[1].set_title("Курящие")

sns.histplot(ax=axes[0], data=df[df[smoke] == 0], x=age, hue=onk)
sns.histplot(ax=axes[1], data=df[df[smoke] == 1], x=age, hue=onk)
plt.show()