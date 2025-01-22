import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

def get_min_max(inputPoints: np.ndarray):
    x, y = inputPoints.shape
    min = 100000* np.ones(y)
    max = np.zeros(y)
    for i in range(x): # iteruj po punktach
        for j in range(y): # iteruj po parametrach punktu
            a = inputPoints[i,j]
            b = min[j]
            if inputPoints[i,j] < min[j]:
                min[j] = inputPoints[i,j]
            if inputPoints[i,j] > max[j]:
                max[j] = inputPoints[i,j]

    return min,max

def split(min,max,partitions,max_or_min,func_utility = None):
    print(max_or_min)
    list = []
    alternatives = len(partitions) # ilość kryteriów
    for i in range(alternatives):
        row = [(0,0)]*(partitions[i]+1)
        list.append(row)

    func_utility_max = 1/alternatives  # maksymalna wartość funkcji użytecznosci przy danej liczbie kryteriów
    
    if not func_utility: 
        for i in range(alternatives):
            if max_or_min[i] == 0: # jeśli minimalizujemy   
                list[i][0] = (min[i],func_utility_max) # wpisuje maxymalną i minimalna wartość kryterium
                list[i][-1] = (max[i],0)
                diff = max[i] - min[i]      # obliczam różnice miedzy max a min wartością kryterium
                compartment = diff/partitions[i]    # wyznaczam przedziały 
                func_utility_other = func_utility_max/partitions[i] # wyznaczam wartość f. użyteczności dla przedziałów
                for j in range(1,partitions[i]): # wpisuje wartości dla konkretnych przedziałów
                    list[i][j] = (min[i]+ j*compartment,func_utility_max -func_utility_other*j)
            

            if max_or_min[i] == 1: # jeśli maksymalizujemy
                list[i][0] = (max[i],func_utility_max) 
                list[i][-1] = (min[i],0)
                diff = max[i] - min[i]
                compartment = diff/partitions[i]
                func_utility_other = func_utility_max/partitions[i]
                for j in range(1,partitions[i]):
                    list[i][j] = (max[i] - j*compartment,func_utility_max - func_utility_other*j)
    else:
        for i in range(alternatives):
            if max_or_min[i] == 0: # jeśli minimalizujemy   
                list[i][0] = (min[i],func_utility[i][0]) # wpisuje maksymalną i minimalna wartość kryterium
                list[i][-1] = (max[i],func_utility[i][-1])
                diff = max[i] - min[i]      # obliczam różnice miedzy max a min wartością kryterium
                compartment = diff/partitions[i]    # wyznaczam przedziały 
                for j in range(1,partitions[i]): # wpisuje wartości dla konkretnych przedziałów
                    list[i][j] = (min[i]+ j*compartment,func_utility[i][j])
            

            if max_or_min[i] == 1: # jeśli maksymalizujemy
                list[i][0] = (max[i],func_utility[i][0]) 
                list[i][-1] = (min[i],func_utility[i][-1])
                diff = max[i] - min[i]
                compartment = diff/partitions[i]
                for j in range(1,partitions[i]):
                    list[i][j] = (max[i] - j*compartment,func_utility[i][j])

    return list

def function_value(compartments,max_or_min):
    list = []
    idx = len(compartments) - 1
    for i in range(1,len(compartments)):
        if max_or_min == 1: # maksymalizacja
            a = (compartments[(idx-i+1)][1]-compartments[(idx-i)][1])/(compartments[(idx-i+1)][0]-compartments[(idx-i)][0])
            b = compartments[(idx-i+1)][1]-a*compartments[(idx-i+1)][0]
            list.append([a,b])
        
        if max_or_min == 0: # minimalizacja
            a = (compartments[i-1][1]-compartments[i][1])/(compartments[i-1][0]-compartments[i][0])
            b = compartments[(i-1)][1]-a*compartments[(i-1)][0]
            list.append([a,b])
    
    return list

def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)

def plot_f_utility(u,compartments,max_or_min): # u - lista współczynników a i b dla f.użyteczności
    cmap = get_cmap(len(u)+1)
    idx = len(compartments)-1     
    for i in range(len(u)):
        a,b = u[i]
        if max_or_min == 1: # maksymalizacja
            x = np.linspace(compartments[idx-i][0],compartments[idx-i-1][0],100)
            y = a*x+b
            if i == len(u)-1:
                plt.scatter(compartments[0][0],a*compartments[0][0]+b, c = 'blue')
            plt.scatter(compartments[idx-i][0],a*compartments[idx-i][0]+b, c = 'blue')
            plt.plot(x, y, c =cmap(i))

        if max_or_min == 0: # minimalizacja
            x = np.linspace(compartments[i][0],compartments[i+1][0],100)
            y = a*x+b
        if i == len(u)-1:
            plt.scatter(compartments[len(u)][0],a*compartments[len(u)][0]+b, c = 'blue')
        plt.scatter(compartments[i][0],a*compartments[i][0]+b, c = 'blue')
        plt.plot(x, y, c =cmap(i))
        
    plt.grid()
    plt.show()

def rank(utility_coef, compartments, point):
    score = 0  
    for i in range(len(compartments[0])):
        for j in range(len(compartments[i])-1):
            
            if point[i] <= compartments[i][j][0] and point[i] >= compartments[i][j+1][0]:
                score += utility_coef[i][j][0]*point[i]+utility_coef[i][j][1]

            elif point[i] >= compartments[i][j][0] and point[i] <= compartments[i][j+1][0]:
                score += utility_coef[i][j][0]*point[i]+utility_coef[i][j][1]

    return score

