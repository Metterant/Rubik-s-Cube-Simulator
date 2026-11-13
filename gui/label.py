from OpenGL import GL

from py3d.core_ext.mesh import Mesh
from py3d.geometry.rectangle import RectangleGeometry
from py3d.material.texture import TextureMaterial
from py3d.extras.text_texture import TextTexture

class Label(Mesh):
    def __init__(self, pos_x = 0, pos_y = 0, text="label", font_size=28):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        
        texture = TextTexture(
            text=text,
            font_size=font_size,
            transparent=True,
        )
        texture.set_properties({
            "magFilter": GL.GL_LINEAR,
            "minFilter": GL.GL_LINEAR,
        })
        # Reupload data because filters have been changed
        texture.upload_data()
    
        text_width, text_height = texture.surface.get_size() # type: ignore
    
        geometry = RectangleGeometry(
            text_width,
            text_height,
            position=(0, 0),
            alignment=(0, 0),
        )
        
        super().__init__(geometry, TextureMaterial(texture))
        self.set_position([pos_x, pos_y, 0.0])