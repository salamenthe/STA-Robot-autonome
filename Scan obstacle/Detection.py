# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 19:36:45 2021

@author: damien
"""

###############################################################
#####     Imports    ##########################################
###############################################################
import math
from typing import List
from typing import Tuple

###############################################################
#####     Fonctions    ########################################
###############################################################

def Scan (Lidar : List[List[float]],Map : List[List[int]], Position : Tuple[float] ,side :float =0.5):       
    """This function fills in the room plan from what the Lidar sees
    
    Parameters
    
    Lidar : An array containing angle and the distance returned by the lidar for this angles
    Map : An array containing tiles with a value of 0 if the tile is unexplored, 1 if it is occupied and 2 if it is free from obstacles (the size of the tiles can be controlled with the side paramter)
    Position : A tuple containing the position along the x-axis, the y-axis and its orientation (in degrees) along the z-axis
    Side : A float that control the size of the tiles in meters, by default it is 0.5 meters. This parameter has to be changed according to the "Map" resolution """
    
    
    if (isDiag(Position[2])):
        raise ValueError ("The Robot must be oriented to 0°, 90°, 180° or 270° or the mapping will not work")
        return 0
    
    
    (indexX,indexY,offset) = findIndexWithPosition(Position,side) 
        #offset is a tuple representing the offset between the center of the tile and the actual position of the Robot
    if (indexX<0): return 0 
    
    
    Lidarxy = AngleToCoordinate(Lidar,Position)
    
    Around = lookAround(Lidarxy,side,offset)  #lookAround returns a Tuple containing the information about the neighbouring tiles
    
    
    if (indexY<len(Map)):                       Map[indexX][indexY+1]   = Around[0];print("1")
    if (indexY<len(Map) and indexX>0):          Map[indexX-1][indexY+1] = Around[1];print("2")
    if (indexX>0):                              Map[indexX-1][indexY]   = Around[2];print("3")
    if (indexY>0 and indexX>0):                 Map[indexX-1][indexY-1] = Around[3];print("4")
    if (indexY>0):                              Map[indexX][indexY-1]   = Around[4];print("5")
    if (indexY>0 and indexX<len(Map[0])):       Map[indexX+1][indexY-1] = Around[5];print("6")
    if (indexX<len(Map[0])):                    Map[indexX+1][indexY]   = Around[6];print("7")
    if (indexY<len(Map) and indexX<len(Map[0])):Map[indexX+1][indexY+1] = Around[7];print("8")
    #The neighbouring tiles have been completed with the data provided by the lidar, Hurah
    return Map
#End Scan

###############################################################

def lookAround(Lidar, side, offset):
    
    return (isFree(Lidar,"front",side, offset),
            isFree(Lidar,"diagTopLeft",side, offset),
            isFree(Lidar,"Left",side, offset),
            isFree(Lidar,"diagBottomLeft",side, offset),
            isFree(Lidar,"Behind",side, offset),
            isFree(Lidar,"diagBottomRight",side, offset),
            isFree(Lidar,"Right",side, offset),
            isFree(Lidar,"diagTopRight",side, offset))


##############################################################
    
def isFree(Lidar, orientation, side, offset):
    #scanne le tableau pour voir si ce n'est pas dans le carré indiqué
    count=0
    
    x_tile,y_tile = Relative_Coordinate(orientation, side, offset)#y_tile et x_ case sont les coordonnées de la case en bas à gauche de la case à scanner 
    print (x_tile,y_tile)
    
    
    for i in range(len(Lidar)):
        if (Lidar[i][0]>x_tile and Lidar[i][0]<x_tile+side and Lidar[i][1]>y_tile and Lidar[i][1]<y_tile+side):
            count+=1
            
    if (count>=5):
        return 1
    return 2

##############################################################

def AngleToCoordinate(TabAng,position):
    Tabxy = [[0,0]for i in range(len(TabAng))]
    for i in range (len(TabAng)):
        Tabxy[i][0] = TabAng[i][1] * math.cos(math.radians(TabAng[i][0]+position[2]))
        Tabxy[i][1] = TabAng[i][1] * math.sin(math.radians(TabAng[i][0]+position[2]))
    return Tabxy

##############################################################

def isDiag(Orientation): 
    eps = 10
    if (abs(Orientation%90-45)<(45.0-eps)):
        print(abs(Orientation%90-45))
        return True
    return False

##############################################################

def findIndexWithPosition(Position,side):
    indexX = int(Position[0]//side)
    indexY = int(Position[1]//side)
    offset = (Position[0]%side-side/2,Position[1]%side-side/2)
    
    if (indexX <0 or indexY<0):
        raise ValueError
        return (-1,0,(0,0))
    return (indexX,indexY,offset)
    
    
##############################################################
        
def Relative_Coordinate(orientation, side, offset):
    if (orientation=="front"):
        x_tile = side/2+offset[0]
        y_tile = -side/2+offset[1]
        
    elif (orientation=="diagTopLeft"):
        x_tile = side/2+offset[0]
        y_tile = -3*side/2+offset[1]
        
    elif (orientation=="Left"):
        x_tile =  -side/2+offset[0]
        y_tile = -3*side/2+offset[1]
        
    elif (orientation=="diagBottomLeft"):
        x_tile = -3*side/2+offset[0]
        y_tile = -3*side/2+offset[1]
        
    elif (orientation=="Behind"):
        x_tile = -3*side/2+offset[0]
        y_tile = -side/2+offset[1]
    elif (orientation=="diagBottomRight"):
        x_tile = -3*side/2+offset[0]
        y_tile = side/2+offset[1]
        
    elif (orientation=="Right"):
        x_tile = -side/2+offset[0]
        y_tile = side/2+offset[1]
        
    elif (orientation=="diagTopRight"):
        x_tile = side/2
        y_tile = side/2
    else :
        raise ValueError
        return

    return (x_tile,y_tile)


#############################FIN##############################    