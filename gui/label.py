from OpenGL import GL

from py3d.core_ext.mesh import Mesh
from py3d.geometry.rectangle import RectangleGeometry
from py3d.material.texture import TextureMaterial
from py3d.extras.text_texture import TextTexture

class Label:
    def __init__(self, pos_x = 0, pos_y = 0, text="label", font_size=28) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        
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
        
        self.mesh = Mesh(text_geometry, TextureMaterial(text_texture))