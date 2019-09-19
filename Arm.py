import numpy as np
from enum import Enum

#Enum class for axis
class Axis(Enum):
    X = 0
    Y = 1
    Z = 2

#Base movement class with axis rotation and returning the rotation matrix
class Movements:
    def __init__(self):
        pass
    
    def rotation_axis_matrix(degrees, axis):
        if axis == Axis.X:
            return np.array([[1, 0, 0],
                             [0, np.cos(np.deg2rad(degrees)), -np.sin(np.deg2rad(degrees))],
                             [0, np.sin(np.deg2rad(degrees)), np.cos(np.deg2rad(degrees))]])
        elif axis == Axis.Y:
            return np.array([[np.cos(np.deg2rad(degrees)), 0, -np.sin(np.deg2rad(degrees))],
                             [0, 1, 0],
                             [np.sin(np.deg2rad(degrees)), 0, np.cos(np.deg2rad(degrees))]])
        elif axis == Axis.Z:
            return np.array([[np.cos(np.deg2rad(degrees)), -np.sin(np.deg2rad(degrees)), 0],
                             [np.sin(np.deg2rad(degrees)), np.cos(np.deg2rad(degrees)), 0],
                             [0, 0, 1]])
        else:
            raise ValueError('Axis must be of the Axis enum')
        
    def rotation_matrix(A, B):
        return np.dot(A, B)

class Arm(Movements):
    def __init__(self, length, theta=0, base=np.array([0,0,0])):
        """
        Lenght is the lenght of the arm
        End is the ending location of the arm/base location for the next arm
        Theta is the current angle of the arm
        Base is the base location of the arm (Not sure if this should always be [0,0,0] or if should be the value of the end of the 'parent' arm)
        """
        self.__length = length
        self.__base = base 
        self.__end = np.add(base, length*np.array([np.cos(np.deg2rad(theta)), 0, np.sin(np.deg2rad(theta))]))
        self.__theta = theta
            
    def set_end(self, end):
        self.__end = end
        
    def set_base(self, base):
        self.__base = base
        self.__end = np.add(base, self.__length*np.array([np.cos(np.deg2rad(self.__theta)), 0, np.sin(np.deg2rad(self.__theta))]))
        
    def rotate_arm(self, degrees, axis=Axis.Y):
        self.__theta += degrees
        rotation = rotation_axis_matrix(degrees, axis)
        self.set_end(np.matmul(self.__end, rotation))
        
    def get_arm_locations():
        return (self.__base, self.__end)
