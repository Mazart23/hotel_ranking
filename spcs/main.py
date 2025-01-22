# from typing import List,Callable
# from spcs.spcs import norm, SPCS
# import pandas as pd
# import numpy as np

# if __name__ == '__main__':
#     df_og = pd.read_csv("prosimy_nie_podawac_credentials'ow")
#     lst = ["Procent zdawalności","Ocena absolwentów","Własna ocena sylabusa"]
#     df : pd.DataFrame = df_og[lst]
#     num = df.to_numpy()
#     ide = []
#     aide = []
#     for i in lst:
#         ddf = df.sort_values([i])
#         aide.append((ddf.iloc[-1]).to_numpy())
#         ide.append((ddf.iloc[0]).to_numpy())
#     rep = SPCS(ide,aide,num)
#     df_kon = df_og.assign(Wartosc=rep)
#     print(df_kon.sort_values('Wartosc',ascending=False))
#     pass

# def gui_spcs(df):
#     # lst = ["Procent zdawalności","Ocena absolwentów","Własna ocena sylabusa"]
#     # df : pd.DataFrame = df_og[lst]
#     df = df[df.columns[3:8]]
#     num = df.to_numpy()
#     aide = []
#     for i in df.columns[3:8]:
#         ddf = df.sort_values([i])
#         aide.append((ddf.iloc[-1]).to_numpy())
#         ide.append((ddf.iloc[0]).to_numpy())
#     # rep = SPCS(ide,aide,num)
#     # df_kon = df.assign(Wartosc=rep)
#     # return df_kon.sort_values('Wartosc',ascending=False)
#     df['SAFETY_PRINCIPAL_score'] = SPCS(ide,aide,num)
#     return df