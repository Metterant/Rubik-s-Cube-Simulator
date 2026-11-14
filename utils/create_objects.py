import math
import os

from py3d.core_ext.object3d import Object3D
from py3d.geometry.box import BoxGeometry
from py3d.material.surface import SurfaceMaterial
from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.core_ext.texture import Texture
from py3d.geometry.rectangle import RectangleGeometry
from py3d.geometry.sphere import SphereGeometry
from py3d.material.texture import TextureMaterial
from py3d.extras.movement_rig import MovementRig
from py3d.extras.text_texture import TextTexture
from py3d.material.basic import BasicMaterial

def create_cubie(home_position: tuple[int, int, int]) -> Object3D:
    cubie: Object3D = Object3D()
    
    axis_colors = {
        (1, 0, 0):  [1.0, 0.0, 0.0], # +X (red)
        (-1, 0, 0): [1.0, 0.5, 0.0], # -X (orange)
        (0, 1, 0):  [1.0, 1.0, 1.0], # +Y (white)
        (0, -1, 0): [1.0, 1.0, 0.0], # -Y (yellow)
        (0, 0, 1):  [0.0, 1.0, 0.0], # +Z (green)
        (0, 0, -1): [0.0, 0.0, 1.0]  # -Z (blue)
    }
    
    sticker_thickness = 0.1
    
    # x sticker
    sticker_position = [home_position[0], 0, 0]
    sticker_length = 0.9
    axis: tuple[int, int, int] = tuple(sticker_position) # type: ignore
    if axis != (0, 0, 0):
        x_sticker_geometry = BoxGeometry(width=sticker_thickness, height=sticker_length, depth=sticker_length) # type: ignore
        x_sticker_material = SurfaceMaterial(property_dict={"baseColor": axis_colors[axis]})
        x_sticker_mesh = Mesh(x_sticker_geometry, x_sticker_material)
        x_sticker_mesh.set_position([(home_position[0] + home_position[0] * sticker_thickness)/2, 0, 0])
        cubie.add(x_sticker_mesh)
        
    
    # y sticker
    sticker_position = [0, home_position[1], 0]
    axis: tuple[int, int, int] = tuple(sticker_position) # type: ignore
    if axis != (0, 0, 0):
        y_sticker_geometry = BoxGeometry(width=sticker_length, height=sticker_thickness, depth=sticker_length) # type: ignore
        y_sticker_material = SurfaceMaterial(property_dict={"baseColor": axis_colors[axis]})
        y_sticker_mesh = Mesh(y_sticker_geometry, y_sticker_material)
        y_sticker_mesh.set_position([0, (home_position[1] + home_position[1] * sticker_thickness)/2, 0])
        cubie.add(y_sticker_mesh)
        
    # z sticker
    sticker_position = [0, 0, home_position[2]]
    axis: tuple[int, int, int] = tuple(sticker_position) # type: ignore
    if axis != (0, 0, 0):
        z_sticker_geometry = BoxGeometry(width=sticker_length, height=sticker_length, depth=sticker_thickness) # type: ignore
        z_sticker_material = SurfaceMaterial(property_dict={"baseColor": axis_colors[axis]})
        z_sticker_mesh = Mesh(z_sticker_geometry, z_sticker_material)
        z_sticker_mesh.set_position([0, 0, (home_position[2] + home_position[2] * sticker_thickness)/2])           
        cubie.add(z_sticker_mesh)

    cubie.add(Mesh(BoxGeometry(), SurfaceMaterial(property_dict={"baseColor": [0.0, 0.0, 0.0]})))
    
    return cubie
    
    