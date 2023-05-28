import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

onk = "Онк/Неонк"
onkDict = ["Неонк", "Онк"]
hyst = "Гистологический диагноз"
hystVals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20, 23]
hystOnk = [1, 2, 3, 6, 12, 13, 14, 15]
hystNonOnk = [4, 5, 7, 8, 9, 10, 16, 17, 19, 20, 23]
hystDict = { 1: "Аденокарцинома", 2: "Карциноид", 3: "Плоскоклеточный рак", 4: "Туберкулема", 5: "Гамартома",
             6: "Мукоэпидермоидный рак", 7: "Нетуберкулезный\nмикобактериоз", 8: "Пневмофиброз",
             9: "Пневмония", 10: "Гранулематоз Вегенера",
             12: "Склерозирующая опухоль", 13: "Смешанный рак", 14: "Мелкоклеточный рак", 15: "Гиперплазия",
             16: "Регенционная киста", 17: "Склерозирующая\nгемангиома", 19: "Муцинозная цистаденома",
             20: "Амилоидоз", 23: "Внутрилегочный\nлимфоузел" }
age = "Возраст, лет"
smoke = "Анамнез курения"
smokeDict = ["Некур", "Кур"]
sex = "Пол"
minSize = "Мин. размер, мм"
maxSize = "Макс. размер, мм"
avgSize = "Сред. размер, мм"

df = pd.read_excel("Data_exam.xlsx", header=1)

def hystologyOnkNonOnk():
    patCount = "Количество пациентов"
    hystDfNonOnk = pd.DataFrame({hyst: [hystDict[x] for x in hystNonOnk], patCount: [len(df[df[hyst] == x]) for x in hystNonOnk]})
    hystDfOnk = pd.DataFrame({hyst: [hystDict[x] for x in hystOnk], patCount: [len(df[df[hyst] == x]) for x in hystOnk]})
    print(hystDfNonOnk)
    print(hystDfOnk)
    fig, axes = plt.subplots(2, 1)
    axes[0].set_title("Неонкология")
    axes[1].set_title("Онкология")
    sns.barplot(ax=axes[0], data=hystDfNonOnk, x=patCount, y=hyst, orient="h")
    sns.barplot(ax=axes[1], data=hystDfOnk, x=patCount, y=hyst, orient="h")
    plt.show()

def smokeOnk():
    print(pd.pivot_table(df[[onk, smoke]], index=smoke, columns=onk, aggfunc=len))
    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("Некурящие")
    axes[1].set_title("Курящие")
    sns.histplot(ax=axes[0], data=df[df[smoke] == 0], x=age, hue=onk)
    sns.histplot(ax=axes[1], data=df[df[smoke] == 1], x=age, hue=onk)
    plt.show()
    # tmpDF = df[[onk, age, smoke]]
    # tmpDF = tmpDF.assign(OnkSmoke = [smokeDict[tmpDF.iloc[i, 2]] + "/" + onkDict[tmpDF.iloc[i, 0]] for i in range(len(tmpDF))])
    # print(tmpDF)
    # sns.histplot(data=tmpDF, x=age, hue="OnkSmoke", bins=12, multiple="dodge", shrink=0.9)
    # plt.show()

def ageOnk():
    # sns.histplot(data=df, x="Возраст, лет", hue="Онк/Неонк", bins=10, multiple="dodge", shrink=0.8)
    sns.histplot(data=df, x="Возраст, лет", hue="Онк/Неонк", bins=20)
    plt.show()

def ageSexOnk():
    tmpDF = df[[onk, sex, age]]
    tmpDF = tmpDF.assign(OnkSex=[tmpDF.iloc[i, 1].upper() + "/" + onkDict[tmpDF.iloc[i, 0]] for i in range(len(tmpDF))])
    print(tmpDF)
    sns.set_palette("Paired")
    sns.histplot(data=tmpDF, x=age, hue="OnkSex", bins=12, multiple="dodge", shrink=0.9)
    plt.show()

def sizeOnk():
    sns.histplot(data=df, x=avgSize, bins=20)
    plt.show()

def sizeOnkNonOnk(var):
    #fig, axes = plt.subplots(1, 2)
    #axes[0].set_title("Неонкология")
    #axes[1].set_title("Онкология")
    #sns.histplot(ax=axes[0], data=df[df[onk] == 0], x=avgSize, bins=20)
    #sns.histplot(ax=axes[1], data=df[df[onk] == 1], x=avgSize, bins=20)
    #plt.show()
    sns.histplot(data=df, x=avgSize, hue=onk, bins=20)
    plt.show()

def sizeDivOnk():
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
    # diff = (maxDiv - minDiv) / 4
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
    # diff = (maxDiv - minDiv) / 4.0
    gapsOnk = [minDiv, 0.07, 0.14, 0.21, maxDiv]
    onkDF = onkDF.assign(Deviation=[getGap(onkDF.iloc[i, 4], gapsOnk) for i in range(len(onkDF))])
    print(onkDF)

    fig, axes = plt.subplots(2, 1)
    axes[0].set_title("Неонкология")
    axes[1].set_title("Онкология")

    colors = [[252 / 255, 198 / 255, 194 / 255], [198 / 255, 217 / 255, 234 / 255], [216 / 255, 240 / 255, 211 / 255],
              [230 / 255, 216 / 255, 234 / 255], [198 / 255, 233 / 255, 217 / 255], [253 / 255, 217 / 255, 193 / 255],
              [216 / 255, 233 / 255, 237 / 255], [246 / 255, 215 / 255, 234 / 255]]

    g = sns.histplot(ax=axes[0], data=nonOnkDF, x=avgSize, hue="Deviation", bins=20, multiple="dodge", shrink=0.8,
                     palette="Pastel1", edgecolor="black")
    patches = [mpatches.Patch(color=colors[i], label=getGap_index(gapsNonOnk, i)) for i in range(len(gapsNonOnk) - 1)]
    g.legend(handles=patches, title="Процент изменения от среднего")
    g.set(xlabel=None, ylabel=None)

    g1 = sns.histplot(ax=axes[1], data=onkDF, x=avgSize, hue="Deviation", bins=20, multiple="dodge", shrink=0.8,
                      palette="Pastel2", edgecolor="black")
    patches1 = [mpatches.Patch(color=colors[i + len(gapsNonOnk) - 1], label=getGap_index(gapsOnk, i)) for i in
                range(len(gapsOnk) - 1)]
    g1.legend(handles=patches1, title="Процент изменения от среднего")
    g1.set(xlabel=None, ylabel=None)

    fig.supxlabel("Средний размер, мм")
    fig.supylabel("Количество пациентов")

    fig.suptitle("Распределение изменения размеров образований от их средней величины")
    plt.show()


sizeDivOnk()