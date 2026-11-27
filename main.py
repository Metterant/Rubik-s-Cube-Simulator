import os
import OpenGL.GL as GL
from collections import deque
from functools import partial


os.chdir(os.path.dirname(os.path.abspath(__file__)))

from py3d.core_ext.object3d import Object3D
from py3d.geometry.box import BoxGeometry
from py3d.material.surface import SurfaceMaterial
from py3d.material.material import Material
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
from py3d.extras.postprocessor import Postprocessor


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
        
        # Post-rendering vignette effect
        default_vs_code = """
        in vec2 vertexPosition;
        in vec2 vertexUV;
        out vec2 UV;
        void main()
        {
            gl_Position = vec4(vertexPosition, 0.0, 1.0);
            UV = vertexUV;
        }
        """
        
        vignette_fs_code = """
        uniform sampler2D textureSampler;
        uniform vec2 resolution;
        uniform float strength;
        in vec2 UV;
        out vec4 fragColor;

        void main() {
            vec4 color = texture(textureSampler, UV);

            vec2 centered = UV * 2.0 - 1.0;
            centered.x *= resolution.x / resolution.y;

            float edge = smoothstep(0.35, 1.15, length(centered));
            color.rgb *= 1.0 - strength * edge;

            fragColor = color;
        }
        """
        vignette_material = Material(
            vertex_shader_code=default_vs_code,
            fragment_shader_code=vignette_fs_code,
        )
        # postprocessor renders the scene into textureSample which is then passed to this shader
        vignette_material.add_uniform("sampler2D", "textureSampler", [0, 1]) 
        vignette_material.add_uniform(
            "vec2", "resolution", [self.screen_width, self.screen_height]
        )
        vignette_material.add_uniform("float", "strength", 0.45)
        vignette_material.locate_uniforms()
        
        # Code taken from https://github.com/raysan5/raylib/issues/4038 with minor fixes
        # - texture0 uniform changed to textureSampler
        # - fragTexCoord changed to UV (output of default_vs_code)
        fxaa_fs_code = """
        #define FXAA_REDUCE_MIN (1.0/128.0)
        #define FXAA_REDUCE_MUL (1.0/8.0)
        #define FXAA_SPAN_MAX 8.0

        in vec2 UV;
        in vec4 fragColor;

        out vec4 finalColor;

        uniform sampler2D textureSampler;
        uniform vec2 resolution;
        
        void main()
        {
            vec2 inverse_resolution = vec2(1.0/resolution.x,1.0/resolution.y);
            
            vec3 rgbNW = texture2D(textureSampler, UV.xy + (vec2(-1.0,-1.0)) * inverse_resolution).xyz;
            vec3 rgbNE = texture2D(textureSampler, UV.xy + (vec2(1.0,-1.0)) * inverse_resolution).xyz;
            vec3 rgbSW = texture2D(textureSampler, UV.xy + (vec2(-1.0,1.0)) * inverse_resolution).xyz;
            vec3 rgbSE = texture2D(textureSampler, UV.xy + (vec2(1.0,1.0)) * inverse_resolution).xyz;
            
            vec3 rgbM  = texture2D(textureSampler, UV.xy).xyz;
            
            vec3 luma = vec3(0.299, 0.587, 0.114);

            float lumaNW = dot(rgbNW, luma);
            float lumaNE = dot(rgbNE, luma);
            float lumaSW = dot(rgbSW, luma);
            float lumaSE = dot(rgbSE, luma);
            float lumaM  = dot(rgbM,  luma);
            float lumaMin = min(lumaM, min(min(lumaNW, lumaNE), min(lumaSW, lumaSE)));
            float lumaMax = max(lumaM, max(max(lumaNW, lumaNE), max(lumaSW, lumaSE))); 

            vec2 dir;
            dir.x = -((lumaNW + lumaNE) - (lumaSW + lumaSE));
            dir.y =  ((lumaNW + lumaSW) - (lumaNE + lumaSE));

            float dirReduce = max((lumaNW + lumaNE + lumaSW + lumaSE) * (0.25 * FXAA_REDUCE_MUL),FXAA_REDUCE_MIN);
            float rcpDirMin = 1.0/(min(abs(dir.x), abs(dir.y)) + dirReduce);

            dir = min(vec2( FXAA_SPAN_MAX,  FXAA_SPAN_MAX),max(vec2(-FXAA_SPAN_MAX, -FXAA_SPAN_MAX),dir * rcpDirMin)) * inverse_resolution;

            vec3 rgbA = 0.5 * (texture2D(textureSampler, UV.xy   + dir * (1.0/3.0 - 0.5)).xyz + texture2D(textureSampler,  UV.xy   + dir * (2.0/3.0 - 0.5)).xyz);
            vec3 rgbB = rgbA * 0.5 + 0.25 * (texture2D(textureSampler, UV.xy   + dir *  - 0.5).xyz + texture2D(textureSampler, UV.xy   + dir * 0.5).xyz);
            
            float lumaB = dot(rgbB, luma);

            if((lumaB < lumaMin) || (lumaB > lumaMax)) 
            {
                finalColor = vec4(rgbA, 1.0);
            } 
            else 
            {
                finalColor = vec4(rgbB,1.0);
            }
        } 
        """
        fxaa_material = Material(
            vertex_shader_code=default_vs_code,
            fragment_shader_code=fxaa_fs_code,
        )
        # postprocessor renders the scene into textureSample which is then passed to this shader
        fxaa_material.add_uniform("sampler2D", "textureSampler", [0, 1]) 
        fxaa_material.add_uniform(
            "vec2", "resolution", [self.screen_width, self.screen_height]
        )
        fxaa_material.locate_uniforms()
        
        self.renderer = Renderer(clear_color=(0.0, 0.8, 0.8))
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=self.screen_width/self.screen_height) # type: ignore
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.set_position([0, 0, 7])

        self.postprocessor = Postprocessor(self.renderer, self.scene, self.camera)
        self.postprocessor.add_effect(vignette_material)
        self.postprocessor.add_effect(fxaa_material)
        
        # Values
        self.rig_z_range = [5, 14]
        self.turn_duration = 0.25
        self.turn_speed = 1.0
        self.mouse_rotate_multiplier = 0.005
        self.mouse_wheel_zoom_multiplier = 0.4
        self.moves_turned = 0
        
        # Times
        self.turn_elapsed = 0.0
        
        # Configurations
        self.is_locked = False
        self.is_manual = False
        
        # Input Logics
        self.is_holding_shift = False

        # Turn
        self.turn_queue = deque() # Element structure: (move: str)
        self.turn_stack = deque() # Turn history
        self.turn_stack_max_size = 30
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
        
        # UI scene
        self.gui = GUIOverlay(self.screen_width, self.screen_height)
        self.gui.add_button(x=10, y=10, width=100, height=32, callback=self._scramble, text="Scramble")
        self.gui.add_button(x=10, y=50, width=100, height=32, callback=self._solve, text="Solve", text_offset=(12, 0))
        
        self.gui.add_button(x=self.screen_width - 110, y=10, width=100, height=32, callback=self._undo, text="Undo", text_offset=(20, 0))
        
        self.gui.quarter_speed_button.callback = partial(self._set_turn_speed, 0.25)
        self.gui.half_speed_button.callback = partial(self._set_turn_speed, 0.5)
        self.gui.normal_speed_button.callback = partial(self._set_turn_speed, 1.0)
        self.gui.double_speed_button.callback = partial(self._set_turn_speed, 2.0)
        self.gui.serialize_button.callback = self._serialize
    
    def _rotate_rubiks(self, horizontal_amount, vertical_amount):
        self.yaw_pivot.rotate_y(horizontal_amount)
        self.pitch_pivot.rotate_x(vertical_amount)
    
    def _reset_rotations(self):
        self.pitch_pivot._matrix = Matrix.make_identity()
        self.yaw_pivot._matrix = Matrix.make_identity()  
    
    def _feed_moves(self, moves, clear=True, lock_until_complete=True, add_to_history=True):
        self.is_locked = lock_until_complete
        if clear:
            self.turn_queue.clear()
        
        for move in moves:
            self.turn_queue.append((move, add_to_history))
    
    def _process_queue(self):
        if self.turn_queue:
            self.moves_turned += 1
            self.curr_turn, add_to_history = self.turn_queue.popleft()

            if add_to_history:
                self._push_stack(self.curr_turn)

            self.rubiks_cube.consume_move(self.curr_turn)
        else:
            self.curr_turn = ""

    def _push_stack(self, move):
        while len(self.turn_stack) >= self.turn_stack_max_size:
            self.turn_stack.popleft()
            
        self.turn_stack.append(move)
        
    def _get_undo_move(self):
        if not self.turn_stack:
            return ""
        
        prime = False
        number_of_repeats = 1
        move = self.turn_stack.pop()
        
        if len(move) > 1:
            if move[1] == "'": prime = True
            else: number_of_repeats = max(1, int(move[1]))
        
        if prime == True:
            return move[0]
        if number_of_repeats == 1:
            return move[0] + "'"
        return move[0] + str(4 - (number_of_repeats % 4))

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
            self._feed_moves([move], False, False)
    
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
        
        t = self.delta_time / self.turn_duration * self.turn_speed * number_of_repeats
        
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
        solution_sequence = sequences.generate_solution_sequence(self.rubiks_cube)
        
        print("Solution sequence: ", solution_sequence)
        self._feed_moves(solution_sequence)

    def _undo(self):
        move = self._get_undo_move()
        self._feed_moves([move], False, False, False)
    
    def _set_turn_speed(self, speed):
        self.turn_speed = speed
        print(f"Set speed to x{speed}")
    
    def _set_manual_turn(self):
        self.is_manual = not self.is_manual
    
    def _manual_turn(self):
        if self.is_manual:
            self._process_queue()
    
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
            if self.turn_elapsed >= self.turn_duration / self.turn_speed:
                self.turn_elapsed = 0
                self._sync_cubies()
                if not self.is_manual:
                    self._process_queue()
        else:
            self.is_locked = False
            self.turn_elapsed = 0
        
        # self.renderer.render(self.scene, self.camera)
        self.postprocessor.render()
        self.renderer.render(
            self.gui.scene,
            self.gui.camera,
            clear_color=False, # Keep color buffer
            clear_depth=True, # Make sure other objects will not block the UI
        )
        # pygame.display.flip() presents the combined result
    
    

if __name__ == "__main__":
    Game(screen_size=[800, 600]).run()