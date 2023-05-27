#добавить новые столбцы и проанализировать:
# - распределение по возрасту
# - распределение по среднему размеру
# - распределение по соотношение накопление глюкозы очаг /легкое
# - распределение по соотношение накопление глюкозы очаг /пул крови
#
# - оценить, что влияет может влиять на онк/неонк
# - спрогнозировать вероятность диагностики онк/неонк

import numpy as np
import pandas as pd
import openpyxl
import seaborn as sns
import matplotlib.pyplot as plt
import ourFunctions as F


if __name__ == "__main__":
    print("-----------------------")
    # F.ageOnk()

    # F.ageSexOnk()
    # F.cancerTendency("Аденокарцинома")
    # F.smokeOnk()
    # F.hystologyOnkNonOnk()
    print("-----------------------")

    # F.sizeOnk()
    # F.sizeOnkNonOnk()
    # F.sizeDivOnk()

    print("-----------------------")

    #F.onkSuv("SUVочаг/SUVпул_18F")
    # F.onkSuv_proportion_of_smokers("SUVочаг/SUVлегк_18F")
    # F.smokeOnkSuv("SUVочаг/SUVлегк_18F")

    print("-----------------------")

    F.onkSuv("SUVочаг/SUVпул_11С")
    F.onkSuv_proportion_of_smokers("SUVочаг/SUVпул_11С")
    F.smokeOnkSuv("SUVочаг/SUVпул_11С")
