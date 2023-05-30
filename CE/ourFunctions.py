import pandas as pd
import numpy as np
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
suvOchSizeF = "SUVочаг/размер_18F"
suvOchLungF = "SUVочаг/SUVлегк_18F"
suvOchPoolF = "SUVочаг/SUVпул_18F"
suvOchF = "SUVочаг_18F"
suvOchC = "SUVочаг_11С"
struct = "Структура очага"
outline = "Контуры очага"
comorbide_patology = "Коморбидная патология "
ochType = "Тип "
patolog = "Коморбидная патология "

patDict = {0: "Нет", 1: "бронх. астма", 2: "ХОБЛ", 3: "вредное производство", 5: "петрификаты в легких", 6: "ХОБЛ, метатуб.изм."}
hystForChoose = [1, 2, 3, 4, 5, 7, 8, 9, 10, 16]
hystVals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20, 23]
hystOnk = [1, 2, 3, 6, 12, 13, 14, 15]
hystNonOnk = [4, 5, 7, 8, 9, 10, 16, 17, 19, 20, 23]
hystDict = {1: "Аденокарцинома", 2: "Карциноид", 3: "Плоскоклеточный рак", 4: "Туберкулема", 5: "Гамартома",
            6: "Мукоэпидермоидный рак", 7: "Нетуберкулезный\nмикобактериоз", 8: "Пневмофиброз",
            9: "Пневмония", 10: "Гранулематоз Вегенера",
            12: "Склерозирующая опухоль", 13: "Смешанный рак", 14: "Мелкоклеточный рак", 15: "Гиперплазия",
            16: "Регенционная киста", 17: "Склерозирующая\nгемангиома", 19: "Муцинозная цистаденома",
            20: "Амилоидоз", 23: "Внутрилегочный\nлимфоузел"}
structDict = ["Нет", "Кальцинаты", "Кавитация", "Кавитация + кальцинаты", "ВБ"]


df = pd.read_excel("Data_exam.xlsx", header=1)


def illnessTendency(illnessType):
    illnessIndex = -1
    for i in hystDict.keys():
        if hystDict[i] == illnessType:
            illnessIndex = i
            break
    if illnessIndex == -1:
        print("Некорректное наименование диагноза. Проверьте ввод.")
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
    red_patch = mpatches.Patch(color=[252 / 255, 217 / 255, 214 / 255], label="Неонк")
    blue_patch = mpatches.Patch(color=[216 / 255, 229 / 255, 240 / 255], label="Онк")
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
    red_patch = mpatches.Patch(color=[252 / 255, 217 / 255, 214 / 255], label="Неонк")
    blue_patch = mpatches.Patch(color=[216 / 255, 229 / 255, 240 / 255], label="Онк")
    g = sns.histplot(ax=axes[0], data=df[df[smoke] == 0], x=age, hue=onk, palette="Pastel1", edgecolor="white")
    g.set(ylim=(0, 40), xlabel=None, ylabel=None)
    g.legend(handles=[red_patch, blue_patch])
    g1 = sns.histplot(ax=axes[1], data=df[df[smoke] == 1], x=age, hue=onk, palette="Pastel1", edgecolor="white")
    g1.set(ylim=(0, 40), xlabel=None, ylabel=None)
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
    red_patch = mpatches.Patch(color=[252 / 255, 217 / 255, 214 / 255], label="Неонк")
    blue_patch = mpatches.Patch(color=[216 / 255, 229 / 255, 240 / 255], label="Онк")
    g.legend(handles=[red_patch, blue_patch])
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
                     palette="Pastel1", edgecolor="white")
    patches = [mpatches.Patch(color=colors[i], label=getGap_index(gapsNonOnk, i)) for i in range(len(gapsNonOnk) - 1)]
    g.legend(handles=patches, title="Процент изменения от среднего")
    g.set(xlabel=None, ylabel=None)
    g.set_yticklabels([i for i in range(0, 31, 5)])
    g1 = sns.histplot(ax=axes[1], data=onkDF, x=avgSize, hue="Deviation", bins=20, multiple="dodge", shrink=0.8,
                      palette="Pastel2", edgecolor="white")
    patches1 = [mpatches.Patch(color=colors[i + len(gapsNonOnk) - 1], label=getGap_index(gapsOnk, i)) for i in
                range(len(gapsOnk) - 1)]
    g1.legend(handles=patches1, title="Процент изменения от среднего")
    g1.set(xlabel=None, ylabel=None)

    fig.supxlabel("Средний размер, мм")
    fig.supylabel("Количество пациентов")

    fig.suptitle("Распределение изменения размеров образований от их средней величины")
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


def suvHyst():
    tmpDF = df[[hyst, suvOchSizeF, suvOchLungF, suvOchPoolF]]

    suvMeanNonOnk = pd.DataFrame({hyst: [hystDict[x] for x in hystNonOnk],
                                  suvOchSizeF: [tmpDF[tmpDF[hyst] == x][suvOchSizeF].mean() for x in hystNonOnk],
                                  suvOchLungF: [tmpDF[tmpDF[hyst] == x][suvOchLungF].mean() for x in hystNonOnk],
                                  suvOchPoolF: [tmpDF[tmpDF[hyst] == x][suvOchPoolF].mean() for x in hystNonOnk]})
    suvMeanNonOnk = pd.melt(suvMeanNonOnk, id_vars=[hyst], value_vars=[suvOchSizeF, suvOchLungF, suvOchPoolF])

    suvMeanOnk = pd.DataFrame({hyst: [hystDict[x] for x in hystOnk],
                               suvOchSizeF: [tmpDF[tmpDF[hyst] == x][suvOchSizeF].mean() for x in hystOnk],
                               suvOchLungF: [tmpDF[tmpDF[hyst] == x][suvOchLungF].mean() for x in hystOnk],
                               suvOchPoolF: [tmpDF[tmpDF[hyst] == x][suvOchPoolF].mean() for x in hystOnk]})
    suvMeanOnk = pd.melt(suvMeanOnk, id_vars=[hyst], value_vars=[suvOchSizeF, suvOchLungF, suvOchPoolF])

    colors = [[252 / 255, 198 / 255, 194 / 255], [198 / 255, 217 / 255, 234 / 255], [216 / 255, 240 / 255, 211 / 255]]

    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("Неонкология")
    axes[1].set_title("Онкология")
    g1 = sns.barplot(ax=axes[0], data=suvMeanNonOnk, x=hyst, y="value", hue="variable", palette="Pastel1",
                     edgecolor="white")
    g2 = sns.barplot(ax=axes[1], data=suvMeanOnk, x=hyst, y="value", hue="variable", palette="Pastel1",
                     edgecolor="white")
    g1.set_xticklabels(labels=[hystDict[x] for x in hystNonOnk], rotation=45, horizontalalignment="right")
    g2.set_xticklabels(labels=[hystDict[x] for x in hystOnk], rotation=45, horizontalalignment="right")
    g1.set(ylim=(0.0, 32.0), xlabel="", ylabel="")
    g2.set(ylim=(0.0, 32.0), xlabel="", ylabel="")
    fig.suptitle("Средние значения соотношений suv для разных диагнозов ")
    fig.supxlabel(hyst)
    fig.supylabel("Значение")
    patches = [mpatches.Patch(color=colors[0], label=suvOchSizeF),
               mpatches.Patch(color=colors[1], label=suvOchLungF),
               mpatches.Patch(color=colors[2], label=suvOchPoolF)]
    g1.legend(handles=patches, title="Соотношения")
    g2.legend(handles=patches, title="Соотношения")

    plt.show()


def suvHystOchVal():
    tmpDF = df[[hyst, suvOchF, suvOchC]]
    newC = []
    for i in range(len(tmpDF)):
        newVal = tmpDF.iloc[i, 2]
        if type(newVal) == str:
            newVal = np.NaN
        newC.append(newVal)
    tmpDF.iloc[:, 2] = newC

    suvMeanNonOnk = pd.DataFrame({hyst: [hystDict[x] for x in hystNonOnk],
                                  suvOchF: [tmpDF[tmpDF[hyst] == x][suvOchF].dropna().mean() for x in hystNonOnk],
                                  suvOchC: [tmpDF[tmpDF[hyst] == x][suvOchC].dropna().mean() for x in
                                            hystNonOnk]}).fillna(0)
    suvMeanNonOnk = pd.melt(suvMeanNonOnk, id_vars=[hyst], value_vars=[suvOchF, suvOchC])

    suvMeanOnk = pd.DataFrame({hyst: [hystDict[x] for x in hystOnk],
                               suvOchF: [tmpDF[tmpDF[hyst] == x][suvOchF].dropna().mean() for x in hystOnk],
                               suvOchC: [tmpDF[tmpDF[hyst] == x][suvOchC].dropna().mean() for x in hystOnk]}).fillna(0)
    suvMeanOnk = pd.melt(suvMeanOnk, id_vars=[hyst], value_vars=[suvOchF, suvOchC])

    colors = [[252 / 255, 198 / 255, 194 / 255], [198 / 255, 217 / 255, 234 / 255]]

    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("Неонкология")
    axes[1].set_title("Онкология")
    g1 = sns.barplot(ax=axes[0], data=suvMeanNonOnk, x=hyst, y="value", hue="variable", palette="Pastel1",
                     edgecolor="white")
    g2 = sns.barplot(ax=axes[1], data=suvMeanOnk, x=hyst, y="value", hue="variable", palette="Pastel1",
                     edgecolor="white")
    g1.set_xticklabels(labels=[hystDict[x] for x in hystNonOnk], rotation=45, horizontalalignment="right")
    g2.set_xticklabels(labels=[hystDict[x] for x in hystOnk], rotation=45, horizontalalignment="right")
    g1.set(ylim=(0.0, 14.5), xlabel="", ylabel="")
    g2.set(ylim=(0.0, 14.5), xlabel="", ylabel="")

    fig.suptitle("Средние значения соотношений SUV очага для каждого диагноза")
    fig.supxlabel(hyst)
    fig.supylabel("Значение")
    patches = [mpatches.Patch(color=colors[0], label="18F"),
               mpatches.Patch(color=colors[1], label="11C")]
    g1.legend(handles=patches, title="SUV очаг")
    g2.legend(handles=patches, title="SUV очаг")
    plt.show()


def outlineType():
    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("Неонкология")
    axes[1].set_title("Онкология")
    red_color = [i / 255 for i in [241, 188, 184]]
    blue_color = [i / 255 for i in [185, 204, 221]]
    green_color = [i / 255 for i in [207, 230, 202]]
    patches = [mpatches.Patch(color=red_color, label="чёткие ровные"),
               mpatches.Patch(color=blue_color, label="спикулы / нечёткие неровные"),
               mpatches.Patch(color=green_color, label="чёткие неровные")]
    tmpDF = df[[hyst, outline, onk]]
    tmpDFnonOnk = pd.DataFrame({hyst: [hystDict[i] for i in hystNonOnk],
                                1: [100 * len(tmpDF[(tmpDF[outline] == 1) & (tmpDF[hyst] == i)]) /
                                    len(tmpDF[tmpDF[hyst] == i]) for i in hystNonOnk],
                                2: [100 * len(tmpDF[(tmpDF[outline] == 2) & (tmpDF[hyst] == i)]) /
                                    len(tmpDF[tmpDF[hyst] == i]) for i in hystNonOnk],
                                3: [100 * len(tmpDF[(tmpDF[outline] == 3) & (tmpDF[hyst] == i)]) /
                                    len(tmpDF[tmpDF[hyst] == i]) for i in hystNonOnk]
                                })

    tmpDFnonOnk = pd.melt(tmpDFnonOnk, id_vars=[hyst], value_vars=[1, 2, 3])
    g = sns.barplot(ax=axes[0], data=tmpDFnonOnk, x=hyst, y="value", hue="variable", palette="Pastel1",
                    edgecolor="white")
    g.set_xticklabels(labels=[hystDict[i] for i in hystNonOnk], rotation=45, horizontalalignment="right")

    tmpDFOnk = pd.DataFrame({hyst: [hystDict[i] for i in hystOnk],
                             1: [100 * len(tmpDF[(tmpDF[outline] == 1) & (tmpDF[hyst] == i)]) /
                                 len(tmpDF[tmpDF[hyst] == i]) for i in hystOnk],
                             2: [100 * len(tmpDF[(tmpDF[outline] == 2) & (tmpDF[hyst] == i)]) /
                                 len(tmpDF[tmpDF[hyst] == i]) for i in hystOnk],
                             3: [100 * len(tmpDF[(tmpDF[outline] == 3) & (tmpDF[hyst] == i)]) /
                                 len(tmpDF[tmpDF[hyst] == i]) for i in hystOnk]
                             })
    tmpDFOnk = pd.melt(tmpDFOnk, id_vars=[hyst], value_vars=[1, 2, 3])
    g1 = sns.barplot(ax=axes[1], data=tmpDFOnk, x=hyst, y="value", hue="variable", palette="Pastel1",
                     edgecolor="white")
    g1.set_xticklabels(labels=[hystDict[i] for i in hystOnk], rotation=45, horizontalalignment="right")

    g.legend(handles=patches, title="Контуры очага")
    g1.legend(handles=patches, title="Контуры очага")
    fig.suptitle("Контуры очага при разных диагнозах")
    g.set(xlabel="", ylabel="")
    g1.set(xlabel="", ylabel="")
    fig.supxlabel("Диагноз")
    fig.supylabel("Процент пациентов")

    plt.show()


def structHyst():
    tmpDF = df[[hyst, struct]]

    structCountNonOnk = pd.DataFrame({hyst: [hystDict[x] for x in hystNonOnk],
                                      structDict[0]: [
                                          len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 0)]) * 100.0 / len(
                                              tmpDF[tmpDF[hyst] == x]) for x in hystNonOnk],
                                      structDict[1]: [
                                          len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 1)]) * 100.0 / len(
                                              tmpDF[tmpDF[hyst] == x]) for x in hystNonOnk],
                                      structDict[2]: [
                                          len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 2)]) * 100.0 / len(
                                              tmpDF[tmpDF[hyst] == x]) for x in hystNonOnk],
                                      structDict[3]: [
                                          len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 3)]) * 100.0 / len(
                                              tmpDF[tmpDF[hyst] == x]) for x in hystNonOnk],
                                      structDict[4]: [
                                          len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 4)]) * 100.0 / len(
                                              tmpDF[tmpDF[hyst] == x]) for x in hystNonOnk]})
    structCountNonOnk = pd.melt(structCountNonOnk, id_vars=[hyst], value_vars=structDict)

    structCountOnk = pd.DataFrame({hyst: [hystDict[x] for x in hystOnk],
                                   structDict[0]: [
                                       len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 0)]) * 100.0 / len(
                                           tmpDF[tmpDF[hyst] == x]) for x in hystOnk],
                                   structDict[1]: [
                                       len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 1)]) * 100.0 / len(
                                           tmpDF[tmpDF[hyst] == x]) for x in hystOnk],
                                   structDict[2]: [
                                       len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 2)]) * 100.0 / len(
                                           tmpDF[tmpDF[hyst] == x]) for x in hystOnk],
                                   structDict[3]: [
                                       len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 3)]) * 100.0 / len(
                                           tmpDF[tmpDF[hyst] == x]) for x in hystOnk],
                                   structDict[4]: [
                                       len(tmpDF[(tmpDF[hyst] == x) & (tmpDF[struct] == 4)]) * 100.0 / len(
                                           tmpDF[tmpDF[hyst] == x]) for x in hystOnk]})
    structCountOnk = pd.melt(structCountOnk, id_vars=[hyst], value_vars=structDict)

    colors = [[252 / 255, 198 / 255, 194 / 255], [198 / 255, 217 / 255, 234 / 255],
              [216 / 255, 240 / 255, 211 / 255],
              [230 / 255, 216 / 255, 234 / 255], [243 / 255, 215 / 255, 177 / 255]]

    fig, axes = plt.subplots(1, 2)
    axes[0].set_title("Неонкология")
    axes[1].set_title("Онкология")
    g1 = sns.barplot(ax=axes[0], data=structCountNonOnk, x=hyst, y="value", hue="variable", palette="Pastel1",
                     edgecolor="white")
    g2 = sns.barplot(ax=axes[1], data=structCountOnk, x=hyst, y="value", hue="variable", palette="Pastel1",
                     edgecolor="white")
    g1.set_xticklabels(labels=[hystDict[x] for x in hystNonOnk], rotation=45, horizontalalignment="right")
    g2.set_xticklabels(labels=[hystDict[x] for x in hystOnk], rotation=45, horizontalalignment="right")
    g1.set(ylim=(0.0, 100.0), xlabel="", ylabel="")
    g2.set(ylim=(0.0, 100.0), xlabel="", ylabel="")
    fig.suptitle("Структуры очагов различных диагнозов")
    fig.supxlabel(hyst)
    fig.supylabel("Процент от общего числа пациентов с диагнозом")
    patches = [mpatches.Patch(color=colors[i], label=structDict[i]) for i in range(len(structDict))]
    g1.legend(handles=patches, title="Структура очага")
    g2.legend(handles=patches, title="Структура очага")
    plt.show()


def hystChoose(s):
    ill = -1
    for i in hystForChoose:
        if s == hystDict[i]:
            ill = i
            break
    if ill == -1:
        print("Некорректное наименование диагноза. Проверьте ввод.")
        return
    tmpDF = df[df[hyst] == ill]
    print(s, "\n")
    print("Всего пациентов:", len(tmpDF), "\n")

    table1 = pd.pivot_table(tmpDF[[sex, smoke]], index=smoke, columns=sex, aggfunc=len).fillna(0).astype(int)
    table2 = pd.pivot_table(tmpDF[[outline, ochType]], index=ochType, columns=outline, aggfunc=len).fillna(0).\
        astype(int)
    print(table1, "\n")
    print(table2, "\n")
    fig, axes = plt.subplots(2, 2)
    axes[0][0].set_title("Распределение по возрасту")
    axes[0][1].set_title("Распределение по среднему размеру")
    axes[1][0].set_title("Распределение по SUV очага (18F)")
    g1 = sns.histplot(ax=axes[0][0], data=tmpDF, x=age, color=[252 / 255, 198 / 255, 194 / 255], edgecolor="white")
    g2 = sns.histplot(ax=axes[0][1], data=tmpDF, x=avgSize, color=[252 / 255, 198 / 255, 194 / 255], edgecolor="white")
    g3 = sns.histplot(ax=axes[1][0], data=tmpDF, x=suvOchF, color=[252 / 255, 198 / 255, 194 / 255], edgecolor="white")
    g1.set(xlabel="", ylabel="Количество пациентов")
    g2.set(xlabel="", ylabel="Количество пациентов")
    g3.set(xlabel="", ylabel="Количество пациентов")
    if len(tmpDF[suvOchC].dropna()) != 0:
        axes[1][1].set_title("Распределение по SUV очага (11C)")
        g4 = sns.histplot(ax=axes[1][1], data=tmpDF, x=suvOchC, color=[252 / 255, 198 / 255, 194 / 255],
                          edgecolor="white")
        g4.set(xlabel="", ylabel="Количество пациентов")
    else:
        fig.delaxes(axes[1][1])
    fig.suptitle(s)
    plt.show()


def hystPat(s):
    ill = -1
    for i in hystDict:
        if s == hystDict[i]:
            ill = i
            break
    if ill == -1:
        print("Некорректное наименование диагноза. Проверьте ввод.")
        return

    tmpDF = df[df[hyst] == ill]
    print(tmpDF, "\n")
    print("Всего пациентов:", len(tmpDF), "\n")

    print(tmpDF.head())

    g = sns.histplot(data=tmpDF, x=patolog, shrink=0.8, color=[252 / 255, 198 / 255, 194 / 255],
                     edgecolor="white", discrete=True)
    plt.ylabel("Количество пациентов")
    plt.title(s)
    g.set_xticks([x for x in range(7) if x != 4])
    g.set_xticklabels(labels=[patDict[x] for x in patDict], rotation=45, horizontalalignment="right")

    plt.show()
