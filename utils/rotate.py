import math

from py3d.core_ext.object3d import Object3D

def rotate_about_x_axis(object3d: Object3D, delta_t: float, clockwise: bool):
    theta = delta_t * math.pi / 2
    if clockwise: theta *= -1
        
    object3d.rotate_x(theta, False)

def rotate_about_y_axis(object3d: Object3D, delta_t: float, clockwise: bool):
    theta = delta_t * math.pi / 2
    if clockwise: theta *= -1
        
    object3d.rotate_y(theta, False)
    
def rotate_about_z_axis(object3d: Object3D, delta_t: float, clockwise: bool):
    theta = delta_t * math.pi / 2
    if clockwise: theta *= -1
        
    object3d.rotate_z(theta, False)