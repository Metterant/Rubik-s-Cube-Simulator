from typing import cast

from .cubie_data import CubieData, PieceType
from .orientation import Orientation

class RubiksCube:
    def __init__(self) -> None:
        self.cubies: list[CubieData] = []
        self.move_dict = {
            "R": self.perform_r_move,
            "L": self.perform_l_move,
            "U": self.perform_u_move,
            "D": self.perform_d_move,
            "F": self.perform_f_move,
            "B": self.perform_b_move,
            "M": self.perform_m_move,
            "E": self.perform_e_move,
            "S": self.perform_s_move,
            "x": self.perform_x_move,
            "y": self.perform_y_move,
            "z": self.perform_z_move,
            "r": self.perform_r_move,
            "l": self.perform_l_move,
            "u": self.perform_u_move,
            "d": self.perform_d_move,
            "f": self.perform_f_move,
            "b": self.perform_b_move,
            "m": self.perform_m_move,
            "e": self.perform_e_move,
            "s": self.perform_s_move
        }
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
    
    def consume_move(self, move):
        prime = False
        number_of_repeats = 1
        
        if len(move) > 1:
            if move[1] == "'": prime = True
            else: number_of_repeats = int(move[1])
        
        for i in range(number_of_repeats): 
            self.move_dict[move[0]](prime)
    
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
