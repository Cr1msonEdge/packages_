import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

hyst = "Гистологический диагноз"
onkDict = ["Неонк", "Онк"]
onk = "Онк/Неонк"
smoke = "Анамнез курения"
age = "Возраст, лет"
sex = "Пол"
hystVals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20, 23]
hystOnk = [1, 2, 3, 6, 12, 13, 14, 15]
hystNonOnk = [4, 5, 7, 8, 9, 10, 16, 17, 19, 20, 23]
hystDict = {1: "Аденокарцинома", 2: "Карциноид", 3: "Плоскоклеточный рак", 4: "Туберкулема", 5: "Гамартома",
            6: "Мукоэпидермоидный рак", 7: "Нетуберкулезный\nмикобактериоз", 8: "Пневмофиброз",
            9: "Пневмония", 10: "Гранулематоз Вегенера",
            12: "Склерозирующая опухоль", 13: "Смешанный рак", 14: "Мелкоклеточный рак", 15: "Гиперплазия",
            16: "Регенционная киста", 17: "Склерозирующая\nгемангиома", 19: "Муцинозная цистаденома",
            20: "Амилоидоз", 23: "Внутрилегочный\nлимфоузел"}

df = pd.read_excel("Data_exam.xlsx", header=1)


def cancerTendency(illnessType):
    illnessIndex = -1
    for i in hystDict.keys():
        if hystDict[i] == illnessType:
            illnessIndex = i
            break
    if illnessIndex == -1:
        print("Данной болезни не найдено. Проверьте ввод.")
        return
    ageMin = df[df[hyst] == illnessIndex][age].min()
    ageMax = df[df[hyst] == illnessIndex][age].max()
    plt.title(str(illnessType))
    sns.histplot(df[df[hyst] == illnessIndex], x=age, hue=sex, palette="RdBu", edgecolor="white")
    plt.xticks(ticks=[i for i in range(ageMin, ageMax + 1) if i % 5 == 0])
    plt.yticks(ticks=[i for i in range(50) if i % 5 == 0])
    plt.ylabel("Количество пациентов")
    plt.show()


def ageOnk():
    sns.histplot(data=df, x=age, hue="Онк/Неонк", bins=20, palette="RdBu", edgecolor="white")
    plt.ylabel("Количество пациентов")
    plt.show()


def ageSexOnk():
    tmpDF = df[[onk, sex, age]]
    tmpDF = tmpDF.assign(OnkSex=[tmpDF.iloc[i, 1].upper() + "/" + onkDict[tmpDF.iloc[i, 0]] for i in range(len(tmpDF))])
    print(tmpDF)
    sns.histplot(data=tmpDF, x=age, hue="OnkSex", bins=12, multiple="dodge", shrink=0.9, palette="Paired",
                 edgecolor="white")
    plt.ylabel("Количество пациентов")
    plt.show()


def smokeOnk():
    print(pd.pivot_table(df[[onk, smoke]], index=smoke, columns=onk, aggfunc=len))
    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("Некурящие")
    axes[1].set_title("Курящие")
    sns.histplot(ax=axes[0], data=df[df[smoke] == 0], x=age, hue=onk, palette="Pastel1", edgecolor="white")
    plt.ylabel("Количество пациентов")
    sns.histplot(ax=axes[1], data=df[df[smoke] == 1], x=age, hue=onk, palette="Pastel1", edgecolor="white")
    plt.ylabel("Количество пациентов")
    plt.show()


def hystologyOnkNonOnk():
    patCount = "Количество пациентов"
    hystDfNonOnk = pd.DataFrame(
        {hyst: [hystDict[x] for x in hystNonOnk], patCount: [len(df[df[hyst] == x]) for x in hystNonOnk]})
    hystDfOnk = pd.DataFrame(
        {hyst: [hystDict[x] for x in hystOnk], patCount: [len(df[df[hyst] == x]) for x in hystOnk]})
    print(hystDfNonOnk)
    print(hystDfOnk)
    fig, axes = plt.subplots(2, 1)
    axes[0].set_title("Неонкология")
    axes[1].set_title("Онкология")
    sns.barplot(ax=axes[0], data=hystDfNonOnk, x=patCount, y=hyst, orient="h")
    sns.barplot(ax=axes[1], data=hystDfOnk, x=patCount, y=hyst, orient="h")
    plt.show()
