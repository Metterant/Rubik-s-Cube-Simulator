from py3d.core.matrix import Matrix
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.object3d import Object3D

from rubik.cubie_data import CubieData

import numpy as np

def sync_cubie_mesh(cubie: CubieData, object3d: Object3D, spacing=1.02):
    transform = Matrix.make_identity()
    transform[:3, :3] = np.array(cubie.orientation.matrix, dtype=float)
    transform[:3, 3] = np.array(cubie.current_position, dtype=float) * spacing
    object3d.local_matrix = transform