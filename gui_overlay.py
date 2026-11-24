import math
from OpenGL import GL

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
from py3d.core.input import Input

from gui.label import Label
from gui.button import Button

class GUIOverlay:
    def __init__(self, screen_width, screen_height) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=self.screen_width/self.screen_height) # type: ignore
        self.camera.set_orthographic( # window-pixel coordinates
            left=0,
            right=screen_width,
            bottom=0,
            top=screen_height,
        )
        self.buttons: list[Button] = []
        
        for button in self.buttons:
            self.scene.add(button)
        
        # self.label1 = Label(20, self.screen_height - 36, "hello there, this is my text", 18)
        # self.scene.add(self.label1)
        
        self.dropdown_visible = False
        
        self.dropdown_button = self.add_button(
            self.screen_width - 30 - 10,
            self.screen_height - 30 - 10,
            width = 30,
            height = 30,
            callback=self.click_dropdown,
            text="v",
            text_offset=(9, 0)
        )
        
        self.quarter_speed_button = self.add_button(x=550, y=540, width=64, height=28, text="x0.25", font_size=24, text_offset=(10, 0), add_to_scene=False)
        self.half_speed_button = self.add_button(x=620, y=540, width=64, height=28, text="x0.50", font_size=24, text_offset=(10, 0), add_to_scene=False)
        self.normal_speed_button = self.add_button(x=690, y=540, width=64, height=28, text="x1.00", font_size=24, text_offset=(10, 0), add_to_scene=False)
        self.double_speed_button = self.add_button(x=760, y=540, width=64, height=28, text="x2.00", font_size=24, text_offset=(10, 0), add_to_scene=False)
        self.serialize_button = self.add_button(x=720, y=500, width=100, height=32, text="Serialize", add_to_scene=False)
        
        self.add_to_dropdown(self.quarter_speed_button)
        self.add_to_dropdown(self.half_speed_button)
        self.add_to_dropdown(self.normal_speed_button)
        self.add_to_dropdown(self.double_speed_button)
        self.add_to_dropdown(self.serialize_button)
                
        self.set_dropdown_visible(False)
                

    def add_button(self, x=0, y=0, width=128, height=32, callback=lambda:(), text="Button", font_size=28, text_offset=(0, 0), add_to_scene=True):
        new_button = Button(x, y, width, height, callback, text, font_size, text_offset)

        self.buttons.append(new_button)
        if add_to_scene:
            self.scene.add(new_button)
        
        return new_button
    
    def handle_input(self, input: Input) -> bool:
        """
        Return True if the input is consumed
        """
        
        if input.is_mouse_down(Input.LEFT_CLICK_MOUSE):
            return self.handle_buttons(input)
        
        return False
    
    def handle_buttons(self, input: Input) -> bool:
        """
        Find buttons that bound the mouse then call each of their callbacks 
        """
        
        mouse_x, mouse_y = input.mouse_pos
        mouse_y = self.screen_height - mouse_y # Flip y direction
        
        for button in self.buttons:
            if not button.is_visible:
                continue
            
            # bound: (x, y, width, height)
            _, _, width, height = button.bound
            left, bottom = button.global_position[:2]
            right = left + width
            top = bottom + height
            if left <= mouse_x <= right and bottom <= mouse_y <= top:
                button.callback()
                return True

        return False

    # ==========================
    # DROPDOWN BUTTONS
    # ==========================
    
        
    def click_dropdown(self):
        self.dropdown_visible = not self.dropdown_visible
        self.set_dropdown_visible(self.dropdown_visible)
    
    def set_dropdown_visible(self, value):
        for descendant in self.dropdown_button.descendant_list:
            if isinstance(descendant, Button) and descendant is not self.dropdown_button:
                descendant.set_visible(value)
                
    def add_to_dropdown(self, button: Button):
        if not self.dropdown_button:
            return
        
        button.translate(-self.screen_width + 10, -self.screen_height + 10, 0)
        self.dropdown_button.add(button)