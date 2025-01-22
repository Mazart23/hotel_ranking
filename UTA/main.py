from UTA.uta import *
import numpy as np
import pandas as pd 
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt

def uta(df, max_or_min):
    
    criteria = df[["Procent zdawalności","Ocena absolwentów","Własna ocena sylabusa","Ilość semestrów","Próg rekrutacji"]]
    column_names = list(criteria.columns)
    criteria.rename(columns = {'Procent zdawalności':'PZ','Ocena absolwentów':'OA', 'Własna ocena sylabusa':'WOS',
                              'Ilość semestrów':'IS','Próg rekrutacji':'PR'}, inplace = True)
    points =[]
    for index, rows in criteria.iterrows():
        my_list =[rows.PZ, rows.OA, rows.WOS,rows.IS, rows.PR]
        points.append(my_list)
    
    points = np.array(points)
    min,max = get_min_max(points)
    max_or_min = np.where(max_or_min=='min', 0, 1)

    # Wartości funkcji użyteczności dobrane ręcznie, kod umożliwia
    # dobranie funkcji użyteczności proporcjonalnie, dla takiego przypadku
    # współczynniki a i b wychodzą takie same dla wszystkich przedziałów

    func_utility = [[0.2,0.02,0],[0.2,0.16,0.12,0.08,0],[0.2,0.16,0.12,0.08,0],[0.2,0.16,0.12,0.08,0.04,0],[0.20,0.10,0]]
    compartments = split(min,max,np.array([2,4,4,6,2]),max_or_min,func_utility)
    
    # Wartość współczynników dla funkcji użyteczności w danych przedziałach
    u = list()
    for i in range(len(compartments)):
        u.append(function_value(compartments[i],max_or_min[i]))
    
    score = []
    for point in points:
        score.append(rank(u,compartments,point))

    df['UTA_score'] = score
    
    # for i in range(len(func_utility)):
    #     plt.title(f'Wartości funkcji użyteczności dla kryterium: {column_names[i]}')
    #     plot_f_utility(u[i],compartments[i],max_or_min[i])
    
    return df
    
