# from typing import List,Callable
# import numpy as np
# import pandas as pd
# from odp import odp

# names = pd.read_excel("SWD DB.xlsx", usecols='A:C,K',skiprows=lambda x: x in [0],names=["Miasto","Nazwa Kierunku","Nazwa Uczelni","Rodzaj Kierunku"],header=None)
# dfA = pd.read_excel("SWD DB.xlsx", usecols='D:H',skiprows=lambda x: x in [0],header=None)
# whole=names.join(other=dfA)
# whole.set_axis(["Miasto","Nazwa Kierunku","Nazwa Uczelni",'Rodzaj Kierunku','Procent zdawalności','Ocena absolwentów','Własna ocena sylabusa','Ilość semestrów','Próg rekrutacji w poprzednim roku'], axis='columns', inplace=True)
# whole_lst=whole.values.tolist()
# B=dfA.values.tolist()

# A=[[120,6,6,4,10],[10,1,1,12,100]]

# min_max=[]
# for i in range(len(A[0])):
#     a=input("Podaj kryterium(min lub max): ")
#     if (a=="min" or a=="max"):
#         min_max.append(np.min if a == "min" else np.max)
#     else:
#         raise ValueError("Zła wartosc")
# K=odp(A,B,min_max,whole,dfA)
# print(K)