# from RSM import RSM
# from typing import List,Callable
# import numpy as np
# import pandas as pd

# def odp(A:List,B:List,min_max:List,whole,dfA):
#     k,lst_zw=RSM(A,B,min_max)
#     k1=sorted(k,reverse=True)
#     dfZW0=pd.DataFrame(k1)
#     dfZW1=pd.DataFrame(lst_zw)
#     dfZW=dfZW1.join(other=dfZW0,rsuffix="Funckja Skoringowa")
#     dfZW.set_axis(['Procent zdawalności','Ocena absolwentów','Własna ocena sylabusa','Ilość semestrów','Próg rekrutacji w poprzednim roku',"Funckja Skoringowa"], axis='columns', inplace=True)
#     dfZW["rank"]=[i for i in range(1,len(dfA)+1)]
#     dfZW = pd.merge(dfZW, whole, on=['Procent zdawalności','Ocena absolwentów','Własna ocena sylabusa','Ilość semestrów','Próg rekrutacji w poprzednim roku'])
#     dfZW.drop(columns=['Procent zdawalności','Ocena absolwentów','Własna ocena sylabusa','Ilość semestrów','Próg rekrutacji w poprzednim roku'],inplace=True)
#     return dfZW