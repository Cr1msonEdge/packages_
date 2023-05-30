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
hystForChoose = [1, 2, 3, 4, 5, 7, 8, 9, 10, 16]
age = "Возраст, лет"
smoke = "Анамнез курения"
minSize = "Мин. размер, мм"
maxSize = "Макс. размер, мм"
avgSize = "Сред. размер, мм"
sex = "Пол"
outline = "Контуры"
ochType = "Тип "
suvOchF = "SUVочаг_18F"
suvOchC = "SUVочаг_11С"

df = pd.read_excel("Data_exam.xlsx", header=1)
pd.set_option('display.max_columns', None)

def hystChoose(s):
    ill = -1
    for i in hystForChoose:
        if s == hystDict[i]:
            ill = i
            break
    if ill == -1:
        print("Некорректное наименование диагноза")
        return
    tmpDF = df[df[hyst] == ill]
    print(s, "\n")
    print("Всего пациентов:", len(tmpDF), "\n")
    #print("Некурящие/Курящие:", len(tmpDF[tmpDF[smoke] == 0]), "/", len(tmpDF[tmpDF[smoke] == 1]))
    #print("Мужчины/Женщины:", len(tmpDF[tmpDF[sex] == "м"]), "/", len(tmpDF[tmpDF[sex] == "ж"]))
    table1 = pd.pivot_table(tmpDF[[sex, smoke]], index=smoke, columns=sex, aggfunc=len).fillna(0).astype(int)
    table2 = pd.pivot_table(tmpDF[[outline, ochType]], index=ochType, columns=outline, aggfunc=len).fillna(0).astype(int)
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
        g4 = sns.histplot(ax=axes[1][1], data=tmpDF, x=suvOchC, color=[252 / 255, 198 / 255, 194 / 255], edgecolor="white")
        g4.set(xlabel="", ylabel="Количество пациентов")
    else:
        fig.delaxes(axes[1][1])
    fig.suptitle(s)
    plt.show()

hystChoose(hystDict[2])