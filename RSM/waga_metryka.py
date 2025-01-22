from typing import List,Callable
import numpy as np

def wage(a0 : List[float],a1: List[float]):
    v = 1
    for n,i in enumerate(a0):
        v *= np.abs(a1[n] - i)
    return v

def metric(a : List[float],b : List[float]):
    d = np.dot(np.array(a)-np.array(b),np.array(a)-np.array(b))
    return np.sqrt(d)