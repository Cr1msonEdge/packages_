import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

onk = "Онк/Неонк"
minSize = "Мин. размер, мм"
maxSize = "Макс. размер, мм"
avgSize = "Сред. размер, мм"

df = pd.read_excel("Data_exam.xlsx", header=1)

sns.histplot(data=df, x=avgSize, bins=20)
plt.show()
