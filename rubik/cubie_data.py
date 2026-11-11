from dataclasses import dataclass
from enum import Enum, auto

from .orientation import Orientation

class PieceType(Enum):
    CORNER = auto()
    EDGE = auto()
    CENTER = auto()

@dataclass
class CubieData:
    type: PieceType
    home_position: tuple[int, int, int] # Vector3
    current_position: tuple[int, int, int] # Vector3
    orientation: Orientation # 3D rotational matrix (with 4th column and 4th row removed)
    
    def is_solved(self) -> bool:
        return self.current_position == self.home_position and self.orientation == Orientation.identity()