from py3d.core_ext.object3d import Object3D
from py3d.core.matrix import Matrix

from rubik.cubie_data import CubieData
from rubik.orientation import Orientation

import numpy as np
import math


def sync_cubie_mesh(cubie: CubieData, object3d: Object3D, spacing=1.02):
    transform = Matrix.make_identity()
    transform[:3, :3] = np.array(cubie.orientation.matrix, dtype=float)
    transform[:3, 3] = np.array(cubie.current_position, dtype=float) * spacing
    object3d.local_matrix = transform

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

def select_m_cubies(cubie_objects: list[Object3D], spacing=1.02):
    return [cubie_obj for cubie_obj in cubie_objects if round((np.array(cubie_obj.local_position) / spacing)[0]) == 0]

def select_e_cubies(cubie_objects: list[Object3D], spacing=1.02):
    return [cubie_obj for cubie_obj in cubie_objects if round((np.array(cubie_obj.local_position) / spacing)[1]) == 0]

def select_s_cubies(cubie_objects: list[Object3D], spacing=1.02):
    return [cubie_obj for cubie_obj in cubie_objects if round((np.array(cubie_obj.local_position) / spacing)[2]) == 0]
