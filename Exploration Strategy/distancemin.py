# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 14:48:20 2021

@author: utilisateur
"""

import numpy as np
import heapq 
import matplotlib.pyplot as plt
from PIL import Image 



# Trouver la zone inexplorée la plus proche du robot
M = np.array([[0,0,1,1],
           [0,1,0.5,1],
           [0,0,1,1],
           [1,0,0,0]])

def trouvermin(mat): #On trouve la case la plus proche 
    m = 0
    n = 0
    mini= mat[0][0]
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if 0 < mat[i][j] < mini : 
                n = i
                m = j
                mini = mat[i][j]
                
    return n,m

def distancemin(mat,x,y): #mat est le tableau,x et y les positions du robot
    n= len(mat[0])
    d = [[None]*n for i in range(len(mat))]
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if(mat[i][j] == 0):
                d[i][j]= abs(i-x) + abs(j-y)
            else:
                d[i][j]=99999
    m,n = trouvermin(d)
    print(m,n)
    
    return m,n


#fonction utile pour le programme suivant
def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

#Algorithme du plus court chemin A modifier pour créer le d de la fonction précédente
def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:

        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))        
    return 0

def Consignes(cons,start,Rotation): #a pour angle, d pour distance, prend en argument deux points, et q le rapport : taille de la pièce/taille de l'image
    cons.append(start)
    cons.reverse()
    print('Chemin suivi',cons)
    L=[]
    for i in range (1,len(cons)-1):
        x1,y1=cons[i-1][0],cons[i-1][1]
        x2,y2=cons[i][0],cons[i][1]
        print(x1,x2,y1,y2)
        if (x2 != x1):
            alpha=np.arctan((y2-y1)/(x2-x1))
        else : 
            alpha =0
        d=np.sqrt((y2-y1)**2+(x2-x1)**2)
        Rotation += alpha
        print(Rotation)
        L.append((Rotation,d*0.5))
    x1,y1=cons[-2][0],cons[-2][1]
    x2,y2=cons[-1][0],cons[-1][1]
    print(x1,x2,y1,y2)
    if (x2 != x1):
        alpha=np.arctan((y2-y1)/(x2-x1))
    else : 
        alpha =0
    Rotation -=alpha
    L.append((Rotation,0))
    print(Rotation)
    # On s'arrete devant la case 0 en s'orientant pour éviter que ce soit un
    #obstacle
    return L,Rotation*180/np.pi

def Consignes2(cons,start,Rotation):
    cons.append(start)
    cons.reverse()
    L=[]
    for i in range(1,len(cons)-1):
        x1,y1=cons[i-1][0],cons[i-1][1]
        x2,y2=cons[i][0],cons[i][1]
        alpha,d=angledistance(x1,x2,y1,y2)
        L.append((alpha,d*0.5))
        Rotation+=alpha
    x1,y1=cons[-2][0],cons[-2][1]
    x2,y2=cons[-1][0],cons[-1][1]
    alpha,d=angledistance(x1,x2,y1,y2)  
    L.append((alpha-Rotation,0*5))
    Rotation+=(alpha-Rotation)
    return L,Rotation
        
        
def angledistance(x1,x2,y1,y2):
    if (x2-x1 == 0):
        if(y2-y1 == 1):
            alpha=270
            d=np.sqrt((y2-y1)**2+(x2-x1)**2)
        if(y2-y1==-1):
            alpha = 90
            d=np.sqrt((y2-y1)**2+(x2-x1)**2)
    if(x2-x1==1):
        if(y2-y1 == 1):
            alpha=225
            d=np.sqrt((y2-y1)**2+(x2-x1)**2)
        if(y2-y1==-1):
            alpha = 135
            d=np.sqrt((y2-y1)**2+(x2-x1)**2)
        if(y2==y1):
            alpha = 180
            d=np.sqrt((y2-y1)**2+(x2-x1)**2)
    if(x2-x1==-1):
        if(y2-y1 == 1):
            alpha=315
            d=np.sqrt((y2-y1)**2+(x2-x1)**2)
        if(y2-y1==-1):
            alpha = 45
            d=np.sqrt((y2-y1)**2+(x2-x1)**2)
        if(y2-y1==0):
            alpha = 0
            d=np.sqrt((y2-y1)**2+(x2-x1)**2)
    return alpha,d
    
   
            
def findstart(tab):
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if tab[i][j]==0.5:
                return (i,j)
          
            
            
            
def comp(tab,l_r,l_p): #ajouter quadrillage, adapter aux dim robot, l_r longueur du robot, l_p longueur de la pièce
    T=tab.copy()
    print(len(T),len(T[0]))
    (h, l) = len(T),len(T[0]) #on recupere la taille du tab
    seuil=2
    q=(l/2)/l_p #coefficient de prop entre im et irl, la lon de la pièce correspondant à environ la moitiè de la longueur de l'im
    print(q)
    dim=int(l_r*q) #dim du robot sur l'im
    for i in range(0,h-dim,dim):
        for j in range(0,l-dim,dim):
            s=0
            for n in range(dim):
                for m in range(dim):
                    s+=T[i+n][j+m]
            if (s>seuil):
                print(s)
                for n in range(dim):
                    for m in range(dim):
                        T[i+n][j+m]=1
            
    return T

    def send_to_ard(liste):
        l=[liste[0]]
        for i in range (1,len(liste)):
            l.append((liste[i][0]-liste[i-1][0],liste[i][1]))
        return l
    
def MsgArduino(liste):
    l=[liste[0]]
    
    for i in range (1,len(liste)):
        l.append((liste[i][0]-liste[i-1][0],liste[i][1]))
    return l

# Driver code
def main():
    M = np.array([[1,2,1,1],
                  [0,1,0.5,1],
                  [1,1,2,2],
                  [2,2,2,1]])
    
    Rotation = 0
    
    start = findstart(M)
    
    
    plt.imshow(M,cmap='afmhot')
    plt.show()
    distances = 99 *np.ones(np.shape(M)) # On initialise a 99 
    for i in range(len(M)):
        for j in range(len(M[0])):
                if astar(M,start,(i,j))!=0 and M[i][j]==0:
                    distances[i][j] = len(astar(M,start,(i,j))) # Toutes les cases
                    #où on peut se rendre sont modifiées
                
    #m,n = distancemin(M,1,2)
    print(distances)
    goal = trouvermin(distances)
    print('Objectifs = ',goal)
    chemin = astar(M,start,goal)
    if chemin !=0:
        print(chemin)
        print('Consignes =',Consignes2(chemin,start,Rotation))
    else :
        print("Exploration terminée")
    #print(MsgArduino(Consignes(chemin,start)))
    #Il faut maintenant envoyer les informations au robot
    #Recevoir les nouvelles infos 
    #Mettre a jour la carte
    #Boucle
                   
main()


    
