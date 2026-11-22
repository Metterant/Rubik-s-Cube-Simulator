import os
import OpenGL.GL as GL
from collections import deque

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


import utils.create_objects as create_objects
import utils.cubies as cubies
import utils.rotate as rotate
import utils.sequences as sequences

from gui_overlay import GUIOverlay

from rubik.rubiks_cube import RubiksCube
from rubik.cubie_data import CubieData

class Game(Base):
    def initialize(self):
        print("Initializing program...")
        self.screen_width = 800
        self.screen_height = 600
        
        self.renderer = Renderer(clear_color=(0.0, 0.8, 0.8))
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=self.screen_width/self.screen_height) # type: ignore
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.set_position([0, 0, 7])
        
        # Values
        self.rig_z_range = [5, 14]
        self.turn_duration = 0.25
        self.mouse_rotate_multiplier = 0.005
        self.mouse_wheel_zoom_multiplier = 0.4
        self.moves_turned = 0
        
        # Times
        self.turn_elapsed = 0.0
        
        # Configurations
        self.is_locked = False
        
        # Input Logics
        self.is_holding_shift = False

        # Turn
        self.turn_queue = deque() # Element structure: (move: str)
        self.curr_turn = ""
        
        # Pivots of the Rubik's Cube
        self.yaw_pivot = Object3D()
        self.pitch_pivot = Object3D()
        
        self.yaw_pivot.add(self.pitch_pivot)
        self.scene.add(self.yaw_pivot)
        
        # Create Cubie Objects
        self.rubiks_cube = RubiksCube()
        self.cubie_objects: list[Object3D] = []
        
        for cubie in self.rubiks_cube.cubies:
            cubie_obj = create_objects.create_cubie(cubie.home_position)
            self.cubie_objects.append(cubie_obj)
            cubies.sync_cubie_mesh(cubie=cubie, object3d=cubie_obj)
            
            self.pitch_pivot.add(cubie_obj)
        
        # UI
        self.gui = GUIOverlay(self.screen_width, self.screen_height)
        self.gui.add_button(x=10, y=10, width=100, height=32, callback=self._scramble, text="Scramble")
        self.gui.add_button(x=10, y=50, width=100, height=32, callback=self._serialize, text="Serialize")
        self.gui.add_button(x=10, y=90, width=100, height=32, callback=self._solve, text="Solve")
    
    def _rotate_rubiks(self, horizontal_amount, vertical_amount):
        self.yaw_pivot.rotate_y(horizontal_amount)
        self.pitch_pivot.rotate_x(vertical_amount)
    
    def _reset_rotations(self):
        self.pitch_pivot._matrix = Matrix.make_identity()
        self.yaw_pivot._matrix = Matrix.make_identity()  
    
    def _feed_moves(self, moves, clear=True, lock_until_complete=True):
        self.is_locked = lock_until_complete
        if clear:
            self.turn_queue.clear()
        
        for move in moves:
            self.turn_queue.append(move)
    
    def _process_queue(self):
        if self.turn_queue:
            self.moves_turned += 1
            self.curr_turn = self.turn_queue.popleft()
            self.rubiks_cube.consume_move(self.curr_turn)
        else:
            self.curr_turn = ""

    def _check_mouse_input(self):        
        if self.input.buttons[0]:
            mouse_rel = self.input.mouse_rel
            self._rotate_rubiks(mouse_rel[0] * self.mouse_rotate_multiplier, mouse_rel[1] * self.mouse_rotate_multiplier)
        if self.input.is_mouse_down(self.input.RIGHT_CLICK_MOUSE):
            self._reset_rotations()
            
        self.translate_rig_z(-self.input.wheel_y * self.mouse_wheel_zoom_multiplier)
        
    def _check_keyboard_input(self):   
        self.is_holding_shift = self.input.is_key_pressed("left shift") or self.input.is_key_pressed("right shift")
        
        move = ""
        if self.input.is_key_down("f"):
            move = "F"
        if self.input.is_key_down("b"):
            move = "B"
        if self.input.is_key_down("u") or self.input.is_key_down("up"):
            move = "U"
        if self.input.is_key_down("d") or self.input.is_key_down("down"):
            move = "D"
        if self.input.is_key_down("r") or self.input.is_key_down("right"):
            move = "R"
        if self.input.is_key_down("l") or self.input.is_key_down("left"):
            move = "L"
        if self.input.is_key_down("m"):
            move = "M"
        if self.input.is_key_down("e"):
            move = "E"
        if self.input.is_key_down("s"):
            move = "S"
        if self.input.is_key_down("x"):
            move = "x"
        if self.input.is_key_down("y"):
            move = "y"
        if self.input.is_key_down("z"):
            move = "z"
        
        if move and not self.is_locked:
            if self.is_holding_shift: move += "'"
            self.turn_queue.append(move)
    
    def _check_input(self):
        self._check_keyboard_input()
        self._check_mouse_input()
    
    def _sync_cubies(self):
        for cubie, cubie_obj in zip(self.rubiks_cube.cubies, self.cubie_objects):
            cubies.sync_cubie_mesh(cubie, cubie_obj)
    
    def _animate_turn(self, move):
        if not move:
            return
        
        clockwise = True
        number_of_repeats = 1
        face = move[0]
        if len(move) > 1:
            if move[1] == "'": clockwise = False
            else: number_of_repeats = max(1, int(move[1]))
        
        t = self.delta_time / self.turn_duration * number_of_repeats
        
        match face:
            case "R":
                selected = cubies.select_r_cubies(self.cubie_objects)
                for cubie in selected:
                    rotate.rotate_about_x_axis(object3d=cubie, delta_t=t, clockwise=clockwise)
            case "L":
                selected = cubies.select_l_cubies(self.cubie_objects)
                for cubie in selected:
                    rotate.rotate_about_x_axis(object3d=cubie, delta_t=t, clockwise=not clockwise)
            case "U":
                selected = cubies.select_u_cubies(self.cubie_objects)
                for cubie in selected:
                    rotate.rotate_about_y_axis(object3d=cubie, delta_t=t, clockwise=clockwise)
            case "D":
                selected = cubies.select_d_cubies(self.cubie_objects)
                for cubie in selected:
                    rotate.rotate_about_y_axis(object3d=cubie, delta_t=t, clockwise=not clockwise)
            case "F":
                selected = cubies.select_f_cubies(self.cubie_objects)
                for cubie in selected:
                    rotate.rotate_about_z_axis(object3d=cubie, delta_t=t, clockwise=clockwise)
            case "B":
                selected = cubies.select_b_cubies(self.cubie_objects)
                for cubie in selected:
                    rotate.rotate_about_z_axis(object3d=cubie, delta_t=t, clockwise= not clockwise)
            case "M":
                selected = cubies.select_m_cubies(self.cubie_objects)
                for cubie in selected:
                    rotate.rotate_about_x_axis(object3d=cubie, delta_t=t, clockwise=clockwise)
            case "E":
                selected = cubies.select_e_cubies(self.cubie_objects)
                for cubie in selected:
                    rotate.rotate_about_y_axis(object3d=cubie, delta_t=t, clockwise=clockwise)
            case "S":
                selected = cubies.select_s_cubies(self.cubie_objects)
                for cubie in selected:
                    rotate.rotate_about_z_axis(object3d=cubie, delta_t=t, clockwise=clockwise)
            case "x":
                selected = self.cubie_objects
                for cubie in selected:
                    rotate.rotate_about_x_axis(object3d=cubie, delta_t=t, clockwise=clockwise)
            case "y":
                selected = self.cubie_objects
                for cubie in selected:
                    rotate.rotate_about_y_axis(object3d=cubie, delta_t=t, clockwise=clockwise)
            case "z":
                selected = self.cubie_objects
                for cubie in selected:
                    rotate.rotate_about_z_axis(object3d=cubie, delta_t=t, clockwise=clockwise)
    
    # ========================
    # Callbacks
    # ========================
    
    def _scramble(self):
        """
        Replace turn_queue with a sequence of 20 random moves and locks 
        the rubik's cube from getting turned until the turn_queue is empty.
        """
        
        print("Scrambling")
        sequence = sequences.generate_scramble_sequence()
        self._feed_moves(sequence)

        print("Scramble sequence: ", sequence)
                
    def _serialize(self):
        print(f"Serialized: {self.rubiks_cube.serialize()}")
    
    def _solve(self):
        rotation_sequence = sequences.generate_orientation_reset_sequence(self.rubiks_cube)
        solution_sequence = sequences.generate_solution_sequence(self.rubiks_cube)
        
        print("Solution sequence: ", solution_sequence)
        self._feed_moves(solution_sequence)
    
    def translate_rig_z(self, z_amount=0.0):
        curr_z = self.rig.local_position[2]
        
        if self.rig_z_range[0] <= curr_z + z_amount <= self.rig_z_range[1]:
            self.rig.translate(0, 0, z_amount)
        
    def update(self):
        self._animate_turn(self.curr_turn)
        
        gui_consumed = self.gui.handle_input(self.input)
        
        if not gui_consumed:
            self._check_input()
        
        if self.turn_queue or self.curr_turn:
            self.turn_elapsed += self.delta_time
            if self.turn_elapsed >= self.turn_duration:
                self.turn_elapsed = 0
                self._sync_cubies()
                self._process_queue()
        else:
            self.is_locked = False
            self.turn_elapsed = 0
        
        self.renderer.render(self.scene, self.camera)
        self.renderer.render(
            self.gui.scene,
            self.gui.camera,
            clear_color=False, # Keep color buffer
            clear_depth=True, # Make sure other objects will not block the UI
        )
        # pygame.display.flip() presents the combined result

if __name__ == "__main__":
    Game(screen_size=[800, 600]).run()