from typing import List,Callable
import numpy as np
import pandas as pd
from RSM.nzd_zd import zdominowane

def cum_count_path(woron_points,metrics = None):
    if metrics == None:
        metrics = lambda x,y: np.sqrt(np.dot(y-x, y-x))
    paths = [0]
    for i in range(1,len(woron_points)):
        paths.append(paths[i-1]+metrics(woron_points[i-1],woron_points[i]))
    return np.array(paths)


def costam(w1:np.ndarray,w2: np.ndarray,w3: np.ndarray):
    w21=w2-w1
    w21_norm= w21/np.linalg.norm(w21)
    w3_p=w3-w1
    dot_p=np.dot(w21_norm,w3_p)
    new=dot_p*w21_norm
    if np.linalg.norm(w21)>np.linalg.norm(new):
        return np.linalg.norm(new), np.linalg.norm(w3_p - new)
    return -1,-1


def zwrot_wagi(Ide,Aide):
    waga=0
    for i in range(len(Ide)):
        waga=waga+volume(Ide[i],Aide[i])
    return waga


def volume(pkt1,pkt2):
    l=[]
    for j in range(len(pkt1)):
        if pkt2[j]>pkt1[j]:
            l.append(pkt2[j]-pkt1[j])
        else:
            l.append(pkt1[j]-pkt2[j])
    V=1
    for i in range(len(l)):
        V=V*l[i]
    return V


def czy_w_obszarze(u,pkt1,pkt2):
    isTRUE=[]
    for i in range(len(u)):
        isTRUE.append(pkt1[i]<=u[i]<=pkt2[i] or pkt2[i]<=u[i]<=pkt1[i])
    for j in range(len(isTRUE)):
        if (isTRUE[j]==False):
            return -1
    return volume(pkt1,pkt2)


def woronoj(pkt_1 : np.ndarray,pkt_2 : np.ndarray):
    N = len(pkt_1)
    pkt_2 = pkt_2-pkt_1
    pkt_1_temp = pkt_1
    pkt_1 = np.zeros(N)
    woronoj_points = [np.array([0,0,0]) for i in range(2*N)]
    woronoj_points[0] = pkt_1
    woronoj_points[-1] = pkt_2
    size_of_shift = np.abs(pkt_2 - pkt_1)/2
    sign_of_shift = np.sign(pkt_2 - pkt_1)
    mask_fixed = np.zeros(N)
    dimentions = np.ones(len(pkt_1))
    for i in range(1,N):
        woronoj_points[i] = woronoj_points[0] + np.min(size_of_shift) * sign_of_shift + mask_fixed
        woronoj_points[2*N-1-i] = woronoj_points[-1] + -1*np.min(size_of_shift) * sign_of_shift - mask_fixed
        idx = np.argmin(size_of_shift)
        mask_fixed[idx] = woronoj_points[i][idx]
        size_of_shift[idx] = np.inf
        sign_of_shift[idx] = 0
        dimentions[idx] = 0
    return np.array(woronoj_points) + pkt_1_temp


def norm(A : List[List[float]], C :  List[List[float]]):
    A1=np.array(A)
    C1=np.array(C)
    normalizedA=(A1-np.min(A1))/(np.max(A1)-np.min(A1))
    normalizedC=(C1-np.min(C1))/(np.max(C1)-np.min(C1))
    return normalizedA,normalizedC


def SPCS(idealny : List[np.ndarray], antyidealny : List[np.ndarray], punkty : List[np.ndarray]):
    scoring = []
    waga = zwrot_wagi(idealny,antyidealny)
    for pkt in range(len(punkty)):
        scoring.append(0)
        
        for ide in range(len(idealny)):
            for anty in range(len(antyidealny)):
                minimal = np.inf
                d_path = 0
                w = czy_w_obszarze(punkty[pkt],idealny[ide],antyidealny[anty])
                if w == -1:
                    continue
                woron_point = woronoj(antyidealny[anty],idealny[ide])
                cum_path = cum_count_path(woron_point)
                for i in range(1,len(woron_point)):
                    d,metric = costam(woron_point[i-1],woron_point[i],punkty[pkt])
                    if d == -1:
                        continue
                    if minimal>metric:
                        minimal = metric
                        d_path = cum_path[i-1]+d
                ### sprawdzanie punktów woronoja
                for i in range(1,len(woron_point)):
                    metric = np.linalg.norm(punkty[pkt]-woron_point[i])
                    if minimal>metric:
                        minimal = metric
                        d_path = cum_path[i]
                ###
                scoring[pkt] += w*d_path
        if waga == 0:
            scoring[pkt] = 0
        else:
            scoring[pkt] = scoring[pkt]/waga
    return scoring

def gui_spcs(df, additional_params):
    min_max = ['max','max','max']
    A = [[120,6,6],[10,1,1],[1,1,1],[120,1,1],[120,1,0],[1,1,1],[130,5,8],[5,2,1]]
    A0, rest = zdominowane(A, min_max)
    A1, rest = zdominowane(rest, min_max)
    df_data = df[df.columns[3:6]]
    num = df_data.to_numpy()

    df['SAFETY_PRINCIPAL_score'] = SPCS(np.array(A0),np.array(A1),num)
    return df