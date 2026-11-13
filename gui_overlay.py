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
        
        self.label1 = Label(0, 0, "hello there, this is my text", 18)
        self.scene.add(self.label1)
        
    def add_button(self, x, y, width, height, callback, text="Button", font_size=28):
        new_button = Button(x, y, width, height, callback, text, font_size)
        self.buttons.append(new_button)
        self.scene.add(new_button)
    
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
            # bound: (x, y, width, height)
            left, bottom, width, height = button.bound
            right = left + width
            top = bottom + height
            if left <= mouse_x <= right and bottom <= mouse_y <= top:
                button.callback()
                return True

        return False
