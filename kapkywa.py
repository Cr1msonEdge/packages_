import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

hyst = "Гистологический диагноз"
onk = "Онк/Неонк"
smoke = "Анамнез курения"
hystVals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20, 23]
hystOnk = [1, 2, 3, 6, 12, 13, 14, 15]
hystNonOnk = [4, 5, 7, 8, 9, 10, 16, 17, 19, 20, 23]
hystDict = { 1 : "Аденокарцинома", 2 : "Карциноид", 3 : "Плоскоклеточный рак", 4 : "Туберкулема", 5 : "Гамартома",
             6 : "Мукоэпидермоидный рак", 7 : "Нетуберкулезный\nмикобактериоз", 8 : "Пневмофиброз",
             9 : "Пневмония", 10 : "Гранулематоз Вегенера",
             12 : "Склерозирующая опухоль", 13 : "Смешанный рак", 14 : "Мелкоклеточный рак", 15 : "Гиперплазия",
             16 : "Регенционная киста", 17 : "Склерозирующая\nгемангиома", 19 : "Муцинозная цистаденома",
             20 : "Амилоидоз", 23 : "Внутрилегочный\nлимфоузел" }

#pd.set_option("display.max_columns", None)

df = pd.read_excel("Data_exam.xlsx", header=1)
#df.rename(columns={})
#for val in df["Локализация в легком"].unique():
#    df.loc[df["Локализация в легком"]]

#df = df.iloc[:, 0:29]
print(df.info())
print(df.head())
print(pd.pivot_table(df[[onk, smoke]], index=smoke, columns=onk, aggfunc=len))

hystTable = pd.pivot_table(df[[onk, hyst]], index=hyst, columns=onk, aggfunc=len, fill_value=0)
print(hystTable)


patCount = "Количество пациентов"
hystDfNonOnk = pd.DataFrame({hyst : [hystDict[x] for x in hystNonOnk], patCount : [len(df[df[hyst] == x]) for x in hystNonOnk]})
hystDfOnk = pd.DataFrame({hyst : [hystDict[x] for x in hystOnk], patCount : [len(df[df[hyst] == x]) for x in hystOnk]})
print(hystDfNonOnk)
print(hystDfOnk)

fig, axes = plt.subplots(2, 1)
axes[0].set_title("Неонкология")
axes[1].set_title("Онкология")

sns.barplot(ax=axes[0], data=hystDfNonOnk, x=patCount, y=hyst, orient="h")
sns.barplot(ax=axes[1], data=hystDfOnk, x=patCount, y=hyst, orient="h")
plt.show()

#OncRatioNonSmok = len(df[(df[onk] == 1) & (df[smoke] == 0)]) / len(df[df[smoke] == 0])
#print(OncRatioNonSmok)

#OncRatioSmok = len(df[(df[onk] == 1) & (df[smoke] == 1)]) / len(df[df[smoke] == 1])
#print(OncRatioSmok)
