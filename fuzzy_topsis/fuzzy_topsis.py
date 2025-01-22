from fuzzy_topsis.FuzzyNum import FuzzyNumb
from typing import List
import numpy as np

def normalize(fuz_num : FuzzyNumb, j, max_cols : List[float], min_cols : List[float] ,cost_ : List[str]):
    if cost_[j] == "min":
        return fuz_num.normalised_cost_criteria(min_cols[j])
    else:
        return fuz_num.normalised_benefit_criteria(max_cols[j])

def cc(d_minus : np.array,d_star : np.array):
    ## step 7 and 8
    cc_i=[d_minus[i]/(d_minus[i]+d_star[i]) for i in range(len(d_minus))]
    return cc_i

def max_fuzz(V : List[FuzzyNumb]):
    max_fuz = FuzzyNumb(-np.inf,-np.inf,-np.inf)
    for i in range(len(V)):
        if V[i]>max_fuz:
            max_fuz = V[i]
    return max_fuz

def min_fuzz(V : List[FuzzyNumb]):
    min_fuz = FuzzyNumb(np.inf, np.inf, np.inf)
    for i in range(len(V)):
        if V[i]<min_fuz:
            min_fuz = V[i]
    return min_fuz

def fuzzy_topsis_(decision_matrix : np.ndarray, weights : List[FuzzyNumb], cost_ : List[str]):
    ## step 3
    max_cols = [max(list(decision_matrix[:,i]),key = lambda x: x.c).c for i in range(len(decision_matrix[0]))]
    min_cols = [min(list(decision_matrix[:,i]),key = lambda x: x.a).a for i in range(len(decision_matrix[0]))]
    r : List[List[FuzzyNumb]] = [[normalize(decision_matrix[i,j],j,max_cols,min_cols,cost_) for j in range(len(decision_matrix[0]))] for i in range(len(decision_matrix))]
    ## step 4
    V : List[List[FuzzyNumb]] = [[r[i][j]*weights[j] for j in range(len(r[0]))] for i in range(len(r))]
    ## step 5 compute ideal solution
    A_ideal = [max_fuzz(np.array(V)[:,i]) for i in range(len(V[0]))]
    A_antyideal = [min_fuzz(np.array(V)[:,i]) for i in range(len(V[0]))]
    ## step 6
    D_star : List[List[FuzzyNumb]] = [np.sum(np.array([V[i][j].d(A_ideal[j]) for j in range(len(V[0]))])) for i in range(len(V))]
    D_minus : List[List[FuzzyNumb]] = [np.sum(np.array([V[i][j].d(A_antyideal[j]) for j in range(len(V[0]))])) for i in range(len(V))]
    ## step 7
    return cc(np.array(D_minus),np.array(D_star))

def fuzzy_topsis(decision_matrix : np.ndarray, weights : List[FuzzyNumb], cost_ : List[str]):
    return fuzzy_topsis_(np.array(decision_matrix), weights, cost_)



