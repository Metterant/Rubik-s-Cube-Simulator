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
from py3d.core.matrix import Matrix

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
        self.rig.set_position([0, 0, 7])
        self.is_holding_shift = False
        self.turn_duration = 0.4
        self.t = 0
        self.clicked = 0
        # self.rig.set_direction([0, 0, 1])
        
        cube_mat = SurfaceMaterial(property_dict={"baseColor": [1.0, 0.0, 0.0]})
        cube_geometry = BoxGeometry()
        self.cube = Mesh(cube_geometry, cube_mat)
        
        self.yaw_pivot = Object3D()
        self.pitch_pivot = Object3D()
        
        self.yaw_pivot.add(self.pitch_pivot)
        self.scene.add(self.yaw_pivot)
        
        self.rubiks_cube = RubiksCube()
        self.cubie_objects: list[Object3D] = []
        
        for cubie in self.rubiks_cube.cubies:
            cubie_obj = create_objects.create_cubie(cubie.home_position)
            self.cubie_objects.append(cubie_obj)
            util.sync_cubie_mesh(cubie=cubie, object3d=cubie_obj)
            
            self.pitch_pivot.add(cubie_obj)

    def _sync_cubies(self):
        for cubie, cubie_obj in zip(self.rubiks_cube.cubies, self.cubie_objects):
            util.sync_cubie_mesh(cubie, cubie_obj)
    
    def _check_mouse_input(self):
        if self.is_holding_shift and self.input.is_mouse_down(self.input.LEFT_CLICK_MOUSE):
            mouse_rel = self.input.mouse_rel
            self.yaw_pivot.rotate_y(mouse_rel[0] * 0.005)
            self.pitch_pivot.rotate_x(mouse_rel[1] * 0.005)
        if self.input.is_mouse_down(self.input.RIGHT_CLICK_MOUSE):
            self.pitch_pivot._matrix = Matrix.make_identity()
            self.yaw_pivot._matrix = Matrix.make_identity()
    
    def _check_keyboard_input(self):   
        self.is_holding_shift = self.input.is_key_pressed("left shift") or self.input.is_key_pressed("right shift")
             
        if self.input._key_down_list:
            self.clicked = self.time
        
        if self.input.is_key_down("f"):
            self.rubiks_cube.perform_f_move(prime=self.is_holding_shift)
        if self.input.is_key_down("b"):
            self.rubiks_cube.perform_b_move(prime=self.is_holding_shift)
        if self.input.is_key_down("u") or self.input.is_key_down("up"):
            self.rubiks_cube.perform_u_move(prime=self.is_holding_shift)
        if self.input.is_key_down("d") or self.input.is_key_down("down"):
            self.rubiks_cube.perform_d_move(prime=self.is_holding_shift)
        if self.input.is_key_down("r") or self.input.is_key_down("right"):
            self.rubiks_cube.perform_r_move(prime=self.is_holding_shift)
        if self.input.is_key_down("l") or self.input.is_key_down("left"):
            self.rubiks_cube.perform_l_move(prime=self.is_holding_shift)
        if self.input.is_key_down("m"):
            self.rubiks_cube.perform_m_move(prime=self.is_holding_shift)
        if self.input.is_key_down("e"):
            self.rubiks_cube.perform_e_move(prime=self.is_holding_shift)
        if self.input.is_key_down("s"):
            self.rubiks_cube.perform_s_move(prime=self.is_holding_shift)
        if self.input.is_key_down("x"):
            self.rubiks_cube.perform_x_move(prime=self.is_holding_shift)
        if self.input.is_key_down("y"):
            self.rubiks_cube.perform_y_move(prime=self.is_holding_shift)
        if self.input.is_key_down("z"):
            self.rubiks_cube.perform_z_move(prime=self.is_holding_shift)

    def _check_input(self):
        self._check_keyboard_input()
        self._check_mouse_input()
    
    def _animate_turn(self):
        self.turn_elapsed = min(self.turn_elapsed + self.delta_time, self.turn_duration)
        t = self.turn_elapsed / self.turn_duration
        eased = t * t * (3 - 2 * t)  # smoothstep
        angle = math.pi / 2 * eased
        
        util.rotate_about_pivot([0, 1.02 * 1.5, 0], "x", 0.01)
    
    def update(self):
        # self.rig.update(self.input, self.delta_time)
        
        self._check_input()
        
        self._sync_cubies()
        self.renderer.render(self.scene, self.camera)

Game(screen_size=[800, 600]).run()