import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

onc = pd.read_excel('Data_exam.xlsx', header=1)
pd.set_option('display.max_columns', None)

print(onc.head())
sns.histplot(onc, x="Возраст, лет")

plt.show()
