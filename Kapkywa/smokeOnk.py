import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

hyst = "Гистологический диагноз"
onk = "Онк/Неонк"
smoke = "Анамнез курения"

df = pd.read_excel("Data_exam.xlsx", header=1)
print(pd.pivot_table(df[[onk, smoke]], index=smoke, columns=onk, aggfunc=len))