from py3d.core.matrix import Matrix
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.object3d import Object3D

from rubik.cubie_data import CubieData
from rubik.orientation import Orientation

import numpy as np
import math

def sync_cubie_mesh(cubie: CubieData, object3d: Object3D, spacing=1.02):
    transform = Matrix.make_identity()
    transform[:3, :3] = np.array(cubie.orientation.matrix, dtype=float)
    transform[:3, 3] = np.array(cubie.current_position, dtype=float) * spacing
    object3d.local_matrix = transform


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


def select_r_cubies(cubie_objects: list[Object3D], spacing=1.02):
    return [cubie_obj for cubie_obj in cubie_objects if round((np.array(cubie_obj.local_position) / spacing)[0]) == 1]

def select_l_cubies(cubie_objects: list[Object3D], spacing=1.02):
    return [cubie_obj for cubie_obj in cubie_objects if round((np.array(cubie_obj.local_position) / spacing)[0]) == -1]

def select_u_cubies(cubie_objects: list[Object3D], spacing=1.02):
    return [cubie_obj for cubie_obj in cubie_objects if round((np.array(cubie_obj.local_position) / spacing)[1]) == 1]

def select_d_cubies(cubie_objects: list[Object3D], spacing=1.02):
    return [cubie_obj for cubie_obj in cubie_objects if round((np.array(cubie_obj.local_position) / spacing)[1]) == -1]

def select_f_cubies(cubie_objects: list[Object3D], spacing=1.02):
    return [cubie_obj for cubie_obj in cubie_objects if round((np.array(cubie_obj.local_position) / spacing)[2]) == 1]

def select_b_cubies(cubie_objects: list[Object3D], spacing=1.02):
    return [cubie_obj for cubie_obj in cubie_objects if round((np.array(cubie_obj.local_position) / spacing)[2]) == -1]