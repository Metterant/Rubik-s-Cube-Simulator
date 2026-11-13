from typing import Callable

from py3d.core_ext.mesh import Mesh
from py3d.core_ext.object3d import Object3D
from py3d.material.surface import SurfaceMaterial
from py3d.core_ext.mesh import Mesh
from py3d.geometry.rectangle import RectangleGeometry

from .label import Label

class Button(Object3D):
    def __init__(self, x, y, width, height, callback: Callable, text="Button", font_size=28):
        super().__init__()
        self.bound = (x, y, width, height)
        self.text = text
        self.callback = callback
        
        material = SurfaceMaterial(property_dict={"baseColor": [1, 1, 1]})
    
        geometry = RectangleGeometry(
            width=width,
            height=height,
            position=(0, 0),
            alignment=(0, 0),
        )
        
        self.label = Label(text=text, font_size=font_size)
        self.background = Mesh(geometry, material)
        
        self.add(self.label)
        self.add(self.background)
        self.set_position([x, y, 0])
    
    def set_label_position(self, x, y):
        self.label.set_position([x, y, 0])