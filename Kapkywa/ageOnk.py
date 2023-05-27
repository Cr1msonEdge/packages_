import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel("Data_exam.xlsx", header=1)
#sns.histplot(data=df, x="Возраст, лет", hue="Онк/Неонк", bins=10, multiple="dodge", shrink=0.8)
sns.histplot(data=df, x="Возраст, лет", hue="Онк/Неонк", bins=20)
plt.show()