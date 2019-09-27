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
    
class Joint(Movements):
    def __init__(self, location=np.array([0,0,0]), theta=0, link=None):
        self.location = location
        self.__theta = theta
        self.link = link
    
    def rotate_link(self, theta, axis):
        if link not None:
            self.link.rotate_link(theta, axis)
            
        self.theta += theta
        
    def set_theta(self, theta, axis):
        if link not None:
            self.link.set_theta(theta, axis)
            
        self.theta = theta
        
    def set_location(self, location):
        if self.link not None:
            self.link.set_base_joint(location)
            
        self.location = location
        
    def get_link(self):
        return self.link
        

class Link(Movements):
    def __init__(self, length, base_joint, end_joint=None):
        """
        Lenght is the lenght of the link
        base_joint is the base of the link
        end_joint is the ending location of the the link, if None is passed in then the joint
        is made for us to be used to store a location since a link shouldn't be responsible for that
        """
        self.length = length
        self.__base_joint = base_joint
        
        if end_joint not None:
            self.__end_joint = end_joint
        else:
            self.__end_joint = Joint(np.array([base_joint.location[0]+length, 0, 0]))
            
    def set_theta(self, theta, axis):
        self.__end_joint.rotate_link(-self.__end_joint.__theta + theta, axis)
        
    def set_base_joint(self, location):
        self.__end_joint.set_location((location - self.__base_joint.location) + self.__end_joint.location)
        
    def rotate_link(self, degrees, axis=Axis.Y):
        rotation = rotation_axis_matrix(degrees, axis)
        self.__end_joint.set_location(np.matmul(self.__end_joint.location, rotation))
        
    def get_arm_locations():
        return (self.__base_joint.location, self.__end_joint.location)
