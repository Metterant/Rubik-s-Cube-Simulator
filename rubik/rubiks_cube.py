from typing import cast

from .cubie_data import CubieData, PieceType
from .orientation import Orientation

class RubiksCube:
    def __init__(self) -> None:
        self.cubies: list[CubieData] = []
        self._initialize_cube()

    def _initialize_cube(self):
        """
        Generate the 26 Cubies
        """
        
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if x == 0 and y == 0 and z == 0:
                        continue
                    
                    zeros = [x, y, z].count(0)
                    
                    if zeros == 0:    p_type = PieceType.CENTER
                    elif zeros == 1:  p_type = PieceType.EDGE
                    else:             p_type = PieceType.CORNER
                    
                    new_cubie = CubieData(p_type, (x, y, z), (x, y, z), Orientation.identity())
                    self.cubies.append(new_cubie)
    
    def is_solved(self) -> bool:
        for cubie in self.cubies:
            if not cubie.is_solved():
                return False
        return True

    def _perform_layer_move(
        self,
        axis: str,
        layer: int,
        clockwise_degrees: int,
        prime: bool,
    ) -> None:
        axis_index = {"x": 0, "y": 1, "z": 2}[axis]
        rotation_factory = {
            "x": Orientation.rotated_x,
            "y": Orientation.rotated_y,
            "z": Orientation.rotated_z,
        }[axis]
        angle = -clockwise_degrees if prime else clockwise_degrees
        rotational_matrix = rotation_factory(angle)

        for cubie in self.cubies:
            if cubie.current_position[axis_index] == layer:
                cubie.current_position = rotational_matrix * cubie.current_position  # type: ignore[assignment]
                cubie.orientation = rotational_matrix * cubie.orientation  # type: ignore[assignment]
    
    def perform_r_move(self, prime: bool = False):
        self._perform_layer_move("x", 1, -90, prime)
    
    def perform_l_move(self, prime: bool = False):
        self._perform_layer_move("x", -1, 90, prime)
        
    def perform_u_move(self, prime: bool = False):
        self._perform_layer_move("y", 1, -90, prime)
            
    def perform_d_move(self, prime: bool = False):
        self._perform_layer_move("y", -1, 90, prime)
    
    def perform_f_move(self, prime: bool = False):
        self._perform_layer_move("z", 1, -90, prime)
    
    def perform_b_move(self, prime: bool = False):
        self._perform_layer_move("z", -1, 90, prime)

    def perform_m_move(self, prime: bool = False):
        self._perform_layer_move("x", 0, -90, prime)
    
    def perform_e_move(self, prime: bool = False):
        self._perform_layer_move("y", 0, -90, prime)
        
    def perform_s_move(self, prime: bool = False):
        self._perform_layer_move("z", 0, -90, prime)
    
    def perform_x_move(self, prime: bool = False):
        self.perform_r_move(prime)
        self.perform_m_move(prime)
        self.perform_l_move(not prime)
    
    def perform_y_move(self, prime: bool = False):
        self.perform_u_move(prime)
        self.perform_e_move(prime)
        self.perform_d_move(not prime)
    
    def perform_z_move(self, prime: bool = False):
        self.perform_f_move(prime)
        self.perform_s_move(prime)
        self.perform_b_move(not prime)
