import math
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

import create_objects
import util
from rubik.rubiks_cube import RubiksCube
from rubik.cubie_data import CubieData
class Game(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer(clear_color=(0.0, 0.8, 0.8))
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600) # type: ignore
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.set_position([0, 0, 4])
        # self.rig.set_direction([0, 0, 1])
        
        cube_mat = SurfaceMaterial(property_dict={"baseColor": [1.0, 0.0, 0.0]})
        cube_geometry = BoxGeometry()
        self.cube = Mesh(cube_geometry, cube_mat)
        
        self.rubiks_cube = RubiksCube()
        self.cubie_objects: list[Object3D] = []
        
        for cubie in self.rubiks_cube.cubies:
            cubie_obj = create_objects.create_cubie(cubie.home_position)
            self.cubie_objects.append(cubie_obj)
            util.sync_cubie_mesh(cubie=cubie, object3d=cubie_obj)
            
            self.scene.add(cubie_obj)

    def sync_cubies(self):
        for cubie, cubie_obj in zip(self.rubiks_cube.cubies, self.cubie_objects):
            util.sync_cubie_mesh(cubie, cubie_obj)
    
    def update(self):
        self.rig.update(self.input, self.delta_time)
        if self.input.is_key_down("u"):
            self.rubiks_cube.perform_u_move()
            
        self.sync_cubies()
        self.renderer.render(self.scene, self.camera)

Game(screen_size=[800, 600]).run()