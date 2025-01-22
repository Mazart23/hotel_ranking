from typing import List, Callable
import numpy as np

def Spearman_s_Footrule(ranking1 : List[int], ranking2 : List[int], weights_function : Callable[[int],float] = None, mean = 0, deviation = 8):
    """
    argv:
        ranking1 : List[int] - pierwszy ranking do porównania ()
        ranking2 : List[int] - drugi ranking do porównania
        weights_function : Callable[[int],float] - funkcja wagowa
    """
    if weights_function == None:

        weights_function = lambda x: (1/np.sqrt(2*np.pi*deviation))*np.exp(-(x-mean)**2/(2*deviation))
    if type(ranking1) != list or type(ranking2) != list:
        raise ValueError("Ranking powinien być listą !!!")

    if len(ranking1) != len(ranking2):
        raise ValueError("Rankingi nie mają takiego samego wymiaru !!!")
    ### 
    sum = 0
    for i in range(len(ranking1)):
        nr = ranking1[i]
        idx_2 = ranking2.index(nr)
        sum += ((weights_function(i)+weights_function(idx_2))/2) * abs(i-idx_2)
    return sum 