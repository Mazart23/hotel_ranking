from typing import List,Callable
from RSM.nzd_zd import zdominowane
import numpy as np
from RSM.waga_metryka import wage, metric


# def RSM(A : List[List[float]], C :  List[List[float]],min_max_criterial_funct : List[Callable[[np.ndarray],float]],metr = None):
#     """
#     RSM metoda zbiorów odniesienia

#     args:
#         A - zbiór punktów odniesienia
#         C - zbiór punktów dopuszczalnych

#     return
#         lst_skoring - punkty skoringowe zbioru B
#         lst - posortowane punkty ze zbioru B względem punktów skoringowych
#     """
#     if metr == None:
#         metr = metric
#     A0,rest = zdominowane(A,min_max_criterial_funct)
#     A1,rest = zdominowane(rest,min_max_criterial_funct)
#     # ## testy
#     # A0 = [[1,1],[2,2]]
#     # A1 = [[2,3],[-1,1],[1,3]]
#     # ## koniec testów
#     if len(A1) == 0:
#         return "error"
#     wages = np.zeros([len(A0),len(A1)])
#     for i in range(len(wages)):
#         for j in range(len(wages[0])):
#             wages[i,j] = wage(A0[i],A1[j])
#     ## Normalization
#     wages = wages/np.sum(wages)
#     lst_skoring = []
#     for i in range(len(C)):
#         lst_skoring.append(0)
#         for j in range(len(wages)):
#             for k in range(len(wages[0])):
#                 lst_skoring[i] += wages[j,k] * metr(C[i],A1[k])/(metr(C[i],A0[j])+metr(C[i],A1[k]))
#     lst = list(zip(C,lst_skoring))
#     lst.sort(key=lambda x: x[1],reverse=True)
#     lst = list(zip(*lst))[0]
    
#     return lst_skoring,lst


def RSM(df, additional_params):
    """
    RSM metoda zbiorów odniesienia

    args:
        A - zbiór punktów odniesienia
        C - zbiór punktów dopuszczalnych

    return
        lst_skoring - punkty skoringowe zbioru B
        lst - posortowane punkty ze zbioru B względem punktów skoringowych
    """
    min_max = [np.min if i == 'min' else np.max for i in additional_params]

    A = [[120,6,6,3,1],[10,1,1,12,100],[1,1,7,3,100],[120,1,1,13,10],[120,1,0,4,10],[1,1,1,2,10],[130,7,1,1,10],[5,7,1,1,10]]
    B = df[df.columns[3: 8]].values
    
    A0, rest = zdominowane(A, min_max)
    A1, rest = zdominowane(rest, min_max)
    
    if len(A1) == 0:
        raise ValueError("Nieprawidłowe A1")

    wages = [[wage(A0[i], A1[j]) for j in range(len(A1))] for i in range(len(A0))]

    wages = wages/np.sum(wages)
    score = []
    for i in range(len(B)):
        score.append(0)
        for j in range(len(wages)):
            for k in range(len(wages[0])):
                score[i] += wages[j,k] * metric(B[i],A1[k]) / (metric(B[i],A0[j]) + metric(B[i],A1[k]))
    
    df['RSM_score'] = score
    return df
