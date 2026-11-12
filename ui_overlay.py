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
from py3d.core.matrix import Matrix

class UIOverlay:
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
        
        self.label1 = self.create_label(0, 0, "hello there, this is my text", 18)
        self.scene.add(self.label1)
    
    def create_label(self, pos_x = 0, pos_y = 0, text="label", font_size=28) -> Mesh:
        text_texture = TextTexture(
            text=text,
            font_size=font_size,
            transparent=True,
        )
        text_texture.set_properties({
            "magFilter": GL.GL_LINEAR,
            "minFilter": GL.GL_LINEAR,
        })
        # Reupload data because filters have been changed
        text_texture.upload_data()

        text_width, text_height = text_texture.surface.get_size() # type: ignore

        text_geometry = RectangleGeometry(
            text_width,
            text_height,
            position=(pos_x, pos_y),
            alignment=(0, 0),
        )
                
        return Mesh(text_geometry, TextureMaterial(text_texture))
        