import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


onk = "Онк/Неонк"
onkDict = ["Неонк", "Онк"]
sex = "Пол"
age = "Возраст, лет"

df = pd.read_excel("Data_exam.xlsx", header=1)
tmpDF = df[[onk, sex, age]]
tmpDF = tmpDF.assign(OnkSex = [tmpDF.iloc[i, 1].upper() + "/" + onkDict[tmpDF.iloc[i, 0]] for i in range(len(tmpDF))])
print(tmpDF)
sns.histplot(data=tmpDF, x=age, hue="OnkSex", bins=12, multiple="dodge", shrink=0.9)
plt.show()