import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

onk = "Онк/Неонк"
minSize = "Мин. размер, мм"
maxSize = "Макс. размер, мм"
avgSize = "Сред. размер, мм"

df = pd.read_excel("Data_exam.xlsx", header=1)

#fig, axes = plt.subplots(1, 2)
#axes[0].set_title("Неонкология")
#axes[1].set_title("Онкология")
#sns.histplot(ax=axes[0], data=df[df[onk] == 0], x=avgSize, bins=20)
#sns.histplot(ax=axes[1], data=df[df[onk] == 1], x=avgSize, bins=20)
#plt.show()

sns.histplot(data=df, x=avgSize, hue=onk, bins=20)
plt.show()