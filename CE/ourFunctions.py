import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

hyst = "Гистологический диагноз"
onkDict = ["Неонк", "Онк"]
onk = "Онк/Неонк"
smoke = "Анамнез курения"
age = "Возраст, лет"
sex = "Пол"
minSize = "Мин. размер, мм"
maxSize = "Макс. размер, мм"
avgSize = "Сред. размер, мм"
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
    g = sns.histplot(data=df, x=age, hue="Онк/Неонк", bins=20, palette="Pastel1", edgecolor="white")
    red_patch = mpatches.Patch(color=[252 / 255, 217 / 255, 214 / 255], label="Онк")
    blue_patch = mpatches.Patch(color=[216 / 255, 229 / 255, 240 / 255], label="Неонк")
    g.legend(handles=[red_patch, blue_patch])
    plt.ylabel("Количество пациентов")
    plt.title("Распределение пациентов по возрасту")
    plt.show()


def ageSexOnk():
    tmpDF = df[[onk, sex, age]]
    tmpDF = tmpDF.assign(OnkSex=[tmpDF.iloc[i, 1].upper() + "/" + onkDict[tmpDF.iloc[i, 0]] for i in range(len(tmpDF))])
    print(pd.pivot_table(df[[sex, onk]], index=sex, columns=onk, aggfunc=len))
    print(tmpDF)
    g = sns.histplot(data=tmpDF, x=age, hue="OnkSex", bins=12, multiple="dodge", shrink=0.9, palette="Paired",
                     edgecolor="white")
    light_blue_patch = mpatches.Patch(color=[188 / 255, 218 / 255, 234 / 255], label="Ж/онк")
    blue_patch = mpatches.Patch(color=[87 / 255, 154 / 255, 198 / 255], label="М/онк")
    light_green_patch = mpatches.Patch(color=[197 / 255, 231 / 255, 167 / 255], label="Ж/неонк")
    green_patch = mpatches.Patch(color=[102 / 255, 184 / 255, 97 / 255], label="М/неонк")
    g.legend(handles=[light_blue_patch, blue_patch, light_green_patch, green_patch])
    plt.ylabel(" ")
    plt.title("Распределение пациентов по полу")
    plt.show()


def smokeOnk():
    print(pd.pivot_table(df[[onk, smoke]], index=smoke, columns=onk, aggfunc=len))
    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("Некурящие")
    axes[1].set_title("Курящие")
    red_patch = mpatches.Patch(color=[252 / 255, 217 / 255, 214 / 255], label="Онк")
    blue_patch = mpatches.Patch(color=[216 / 255, 229 / 255, 240 / 255], label="Неонк")
    g = sns.histplot(ax=axes[0], data=df[df[smoke] == 0], x=age, hue=onk, palette="Pastel1", edgecolor="white")
    g.set(xlabel=None, ylabel=None)
    g.legend(handles=[red_patch, blue_patch])
    g1 = sns.histplot(ax=axes[1], data=df[df[smoke] == 1], x=age, hue=onk, palette="Pastel1", edgecolor="white")
    g1.set(xlabel=None, ylabel=None)
    g1.legend(handles=[red_patch, blue_patch])
    fig.supxlabel("Возраст")
    fig.supylabel("Количество пациентов")
    fig.suptitle("Соотношение пациентов по анамнезу курения")
    plt.show()


def hystologyOnkNonOnk():
    patCount = "Количество пациентов"
    hystDfNonOnk = pd.DataFrame(
        {hyst: [hystDict[x] for x in hystNonOnk], patCount: [len(df[df[hyst] == x]) for x in hystNonOnk]})
    hystDfOnk = pd.DataFrame(
        {hyst: [hystDict[x] for x in hystOnk], patCount: [len(df[df[hyst] == x]) for x in hystOnk]})
    print(hystDfNonOnk)
    print(hystDfOnk)
    print(pd.pivot_table(df[[onk, hyst]], index=onk, columns=hyst, aggfunc=len))
    fig, axes = plt.subplots(2, 1)
    axes[0].set_title("Неонкология")
    axes[1].set_title("Онкология")
    g = sns.barplot(ax=axes[0], data=hystDfNonOnk, x=patCount, y=hyst, orient="h")
    g1 = sns.barplot(ax=axes[1], data=hystDfOnk, x=patCount, y=hyst, orient="h")
    g.set(xlabel=None)
    g1.set(xlabel=None)
    fig.supxlabel("Количество пациентов")
    fig.suptitle("Общее распределение болезней")
    plt.show()


def sizeOnk():
    sns.histplot(data=df, x=avgSize, bins=20, color="lightblue", edgecolor="white")
    plt.ylabel("Количество пациентов")
    plt.title("Распределение по размеру новообразований")
    plt.show()


def sizeOnkNonOnk():
    plt.ylabel("Количество пациентов")
    plt.title("Распределение по размеру новообразований")
    g = sns.histplot(data=df, x=avgSize, hue=onk, bins=20, palette="Pastel1", edgecolor="white")
    red_patch = mpatches.Patch(color=[252 / 255, 217 / 255, 214 / 255], label="Онк")
    blue_patch = mpatches.Patch(color=[216 / 255, 229 / 255, 240 / 255], label="Неонк")
    g.legend(handles=[red_patch, blue_patch])
    plt.show()


def sizeDivOnk():
    def getGap(val, gapsArg):
        for i in range(len(gapsArg) - 1):
            if val <= gapsArg[i + 1]:
                return "[" + str(int(gapsArg[i] * 100.0)) + "%; " + str(int(gapsArg[i + 1] * 100.0)) + "%]"

    # удалим некорректную запись
    tmpDF = df[[onk, minSize, maxSize, avgSize]].drop(index=[219], axis=0)

    nonOnkDF = tmpDF[tmpDF[onk] == 0]
    nonOnkDF = nonOnkDF.assign(percDiv=(nonOnkDF[maxSize] - nonOnkDF[minSize]) / (nonOnkDF[avgSize] * 2.0))
    minDiv = nonOnkDF.percDiv.min()
    maxDiv = nonOnkDF.percDiv.max()
    print(nonOnkDF[nonOnkDF.percDiv == maxDiv])
    print(minDiv, maxDiv)
    diff = (maxDiv - minDiv) / 4
    gaps = [minDiv, minDiv + diff, minDiv + diff * 2.0, minDiv + diff * 3.0, maxDiv]
    nonOnkDF = nonOnkDF.assign(Deviation=[getGap(nonOnkDF.iloc[i, 4], gaps) for i in range(len(nonOnkDF))])
    print(nonOnkDF)

    onkDF = tmpDF[tmpDF[onk] == 1]
    onkDF = onkDF.assign(percDiv=(onkDF[maxSize] - onkDF[minSize]) / (onkDF[avgSize] * 2.0))
    minDiv = onkDF.percDiv.min()
    maxDiv = onkDF.percDiv.max()
    print(onkDF[onkDF.percDiv == maxDiv])
    print(minDiv, maxDiv)
    diff = (maxDiv - minDiv) / 4.0
    gaps = [minDiv, minDiv + diff, minDiv + diff * 2.0, minDiv + diff * 3.0, maxDiv]
    onkDF = onkDF.assign(Deviation=[getGap(onkDF.iloc[i, 4], gaps) for i in range(len(onkDF))])
    print(onkDF)

    fig, axes = plt.subplots(2, 1)
    axes[0].set_title("Неонкология")
    axes[1].set_title("Онкология")

    g = sns.histplot(ax=axes[0], data=nonOnkDF, x=avgSize, hue="Deviation", bins=20, multiple="dodge", shrink=0.9,
                     palette="Pastel1", edgecolor="black")
    patch1 = mpatches.Patch(color=[198 / 255, 217 / 255, 234 / 255], label="[0%; 16%]")
    patch2 = mpatches.Patch(color=[252 / 255, 198 / 255, 194 / 255], label="[16%; 33%]")
    patch3 = mpatches.Patch(color=[216 / 255, 240 / 255, 211 / 255], label="[33%; 50%]")
    patch4 = mpatches.Patch(color=[230 / 255, 216 / 255, 234 / 255], label="[50%; 66%]")
    g.legend(handles=[patch1, patch2, patch3, patch4], title="Процент отклонения")
    g.set(xlabel=None, ylabel=None)

    g1 = sns.histplot(ax=axes[1], data=onkDF, x=avgSize, hue="Deviation", bins=20, multiple="dodge", shrink=0.9,
                      palette="Pastel2", edgecolor="black")
    patch5 = mpatches.Patch(color=[198 / 255, 233 / 255, 217 / 255], label="[0%; 14%]")
    patch6 = mpatches.Patch(color=[253 / 255, 217 / 255, 193 / 255], label="[14%; 29%]")
    patch7 = mpatches.Patch(color=[216 / 255, 233 / 255, 237 / 255], label="[29%; 44%]")
    patch8 = mpatches.Patch(color=[246 / 255, 215 / 255, 234 / 255], label="[44%; 58%]")
    g1.legend(handles=[patch5, patch6, patch7, patch8], title="Процент отклонения")
    g1.set(xlabel=None, ylabel=None)

    fig.supxlabel("Средний размер, мм")
    fig.supylabel("Количество пациентов")

    # TODO тупо звучит
    fig.suptitle("Распределение отклонений размеров образований от их средней величины")
    plt.show()


# распределения suv


def onkSuv(suv):
    g = sns.histplot(data=df, x=suv, hue=onk, bins=20, palette="Pastel1", edgecolor="white")
    red_patch = mpatches.Patch(color=[252 / 255, 217 / 255, 214 / 255], label="Неонк")
    blue_patch = mpatches.Patch(color=[216 / 255, 229 / 255, 240 / 255], label="Онк")
    g.legend(handles=[red_patch, blue_patch])
    plt.title("Распределение suv")
    plt.ylabel("Количество пациентов")
    plt.show()


def onkSuv_proportion_of_smokers(suv):
    red_patch = mpatches.Patch(color=[252 / 255, 217 / 255, 214 / 255], label="Некурящие")
    blue_patch = mpatches.Patch(color=[216 / 255, 229 / 255, 240 / 255], label="Курящие")
    g = sns.histplot(data=df, x=suv, hue=smoke, bins=20, palette="Pastel1", edgecolor="white")
    g.legend(handles=[red_patch, blue_patch])
    plt.title("Распределение suv среди курящих и не курящих")
    plt.ylabel("Количество пациентов")
    plt.show()


def smokeOnkSuv(suv):
    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("Некурящие")
    axes[1].set_title("Курящие")
    if suv == "SUVочаг/SUVлегк_18F" or suv == "SUVочаг/SUVпул_18F":
        axes[0].set_xlim([0, 95])
        axes[0].set_ylim([0, 80])
        axes[1].set_xlim([0, 95])
        axes[1].set_ylim([0, 80])
    elif suv == "SUVочаг/SUVлегк_11С" or suv == "SUVочаг/SUVпул_11С":
        axes[0].set_xlim([0, 12])
        axes[0].set_ylim([0, 20])
        axes[1].set_xlim([0, 12])
        axes[1].set_ylim([0, 20])
        axes[0].set_yticks(ticks=[i for i in range(0, 20) if i % 2 == 0])
        axes[1].set_yticks(ticks=[i for i in range(0, 20) if i % 2 == 0])
    red_patch = mpatches.Patch(color=[252 / 255, 217 / 255, 214 / 255], label="Неонк")
    blue_patch = mpatches.Patch(color=[216 / 255, 229 / 255, 240 / 255], label="Онк")
    g = sns.histplot(ax=axes[0], data=df[df[smoke] == 0], x=suv, hue=onk, palette="Pastel1", edgecolor="white")
    g.set(xlabel="", ylabel="")
    g.legend(handles=[red_patch, blue_patch])

    g1 = sns.histplot(ax=axes[1], data=df[df[smoke] == 1], x=suv, hue=onk, palette="Pastel1", edgecolor="white")
    g1.set(xlabel="", ylabel="")
    g1.legend(handles=[red_patch, blue_patch])
    fig.supxlabel(suv)
    fig.supylabel("Количество пациентов")
    fig.suptitle("Распределение suv среди курящих и не курящих")
    plt.show()
