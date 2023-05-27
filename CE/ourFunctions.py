import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

hyst = "Гистологический диагноз"
onk = "Онк/Неонк"
smoke = "Анамнез курения"
age = "Возраст, лет"
sex = "Пол"
hystVals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20, 23]
hystOnk = [1, 2, 3, 6, 12, 13, 14, 15]
hystNonOnk = [4, 5, 7, 8, 9, 10, 16, 17, 19, 20, 23]
hystDict = {1: "Аденокарцинома", 2: "Карциноид", 3: "Плоскоклеточный рак", 4: "Туберкулема", 5: "Гамартома",
            6: "Мукоэпидермоидный рак", 7: "Нетуберкулезный микобактериоз", 8: "Пневмофиброз",
            9: "Пневмония", 10: "Гранулематоз Вегенера",
            12: "Внутрисосудистая склерозирующая бронхиоло-альвеолярная опухоль",
            13: "Смешанный рак", 14: "Мелкоклеточный рак", 15: "Гиперплазия",
            16: "Регенционная киста", 17: "Склерозирующая гемангиома", 19: "Муцинозная цистаденома",
            20: "Амилоидоз", 23: "Внутрилегочный лимфоузел"}

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
    plt.ylim(1)
    plt.xticks(ticks=[i for i in range(ageMin, ageMax + 1) if i % 5 == 0])
    plt.yticks(ticks=[i for i in range(50) if i % 5 == 0])
    plt.ylabel("Количество пациентов")
    plt.show()

