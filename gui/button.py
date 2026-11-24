from typing import Callable

from py3d.core_ext.mesh import Mesh
from py3d.core_ext.object3d import Object3D
from py3d.material.surface import SurfaceMaterial
from py3d.core_ext.mesh import Mesh
from py3d.geometry.rectangle import RectangleGeometry

from .label import Label

class Button(Object3D):
    def __init__(self, x=0, y=0, width=128, height=32, callback: Callable=lambda:(), text="Button", font_size=28, text_offset=(0, 0)):
        super().__init__()
        self.bound = (x, y, width, height)
        self.text = text
        self.callback = callback
        self.is_visible = True
        
        material = SurfaceMaterial(property_dict={"baseColor": [1, 1, 1]})
    
        geometry = RectangleGeometry(
            width=width,
            height=height,
            position=(0, 0),
            alignment=(0, 0),
        )
        
        self.label = Label(text=text, font_size=font_size)
        self.label.set_position((text_offset[0], text_offset[1], 0))
        self.background = Mesh(geometry, material)
        
        self.add(self.label)
        self.add(self.background)
        self.set_position([x, y, 0])
    
    def set_label_position(self, x, y):
        self.label.set_position([x, y, 0])
    
    def set_visible(self, visible):
        self.is_visible = visible
        
        for descendant in self.descendant_list:
            if isinstance(descendant, Mesh):
                descendant.visible = visible
    
    def set_callback(self, callback: Callable):
        if callback:
            self.callback = callback