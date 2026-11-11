from typing import cast

from cubie_data import CubieData, PieceType
from orientation import Orientation

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
    
    def perform_r_move(self, prime: bool = False):
        # Select cubies with current X = 1
        active_cubies = [c for c in self.cubies if c.current_position[0] == 1]
        
        for cubie in active_cubies:
            rotational_matrix = Orientation.rotated_x(-90) if prime else Orientation.rotated_x(+90)
            cubie.current_position = rotational_matrix * cubie.current_position # type: ignore
            cubie.orientation *= rotational_matrix # type: ignore
    
    def perform_l_move(self, prime: bool = False):
        # Select cubies with current X = -1
        active_cubies = [c for c in self.cubies if c.current_position[0] == -1]
        
        for cubie in active_cubies:
            rotational_matrix = Orientation.rotated_x(-90) if prime else Orientation.rotated_x(+90)
            cubie.current_position = rotational_matrix * cubie.current_position # type: ignore
            cubie.orientation *= rotational_matrix # type: ignore
        
    def perform_u_move(self, prime: bool = False):
        # Select cubies with current Y = 1
        active_cubies = [c for c in self.cubies if c.current_position[1] == 1]
        
        for cubie in active_cubies:
            rotational_matrix = Orientation.rotated_y(-90) if prime else Orientation.rotated_y(+90)
            cubie.current_position = rotational_matrix * cubie.current_position # type: ignore
            cubie.orientation *= rotational_matrix # type: ignore
            
    def perform_d_move(self, prime: bool = False):
        # Select cubies with current Y = -1
        active_cubies = [c for c in self.cubies if c.current_position[1] == -1]
        
        for cubie in active_cubies:
            rotational_matrix = Orientation.rotated_y(-90) if prime else Orientation.rotated_y(+90)
            cubie.current_position = rotational_matrix * cubie.current_position # type: ignore
            cubie.orientation *= rotational_matrix # type: ignore
    
            
    def perform_f_move(self, prime: bool = False):
        # Select cubies with current Z = 1
        active_cubies = [c for c in self.cubies if c.current_position[2] == 1]
        
        for cubie in active_cubies:
            rotational_matrix = Orientation.rotated_z(-90) if prime else Orientation.rotated_z(+90)
            cubie.current_position = rotational_matrix * cubie.current_position # type: ignore
            cubie.orientation *= rotational_matrix # type: ignore
    
    def perform_b_move(self, prime: bool = False):
        # Select cubies with current Z = -1
        active_cubies = [c for c in self.cubies if c.current_position[2] == -1]
        
        for cubie in active_cubies:
            rotational_matrix = Orientation.rotated_z(-90) if prime else Orientation.rotated_z(+90)
            cubie.current_position = rotational_matrix * cubie.current_position # type: ignore
            cubie.orientation *= rotational_matrix # type: ignore


rubiks_cube = RubiksCube()
for i in range(6):
    rubiks_cube.perform_r_move(prime=False)
    rubiks_cube.perform_u_move(prime=False)
    rubiks_cube.perform_r_move(prime=True)
    rubiks_cube.perform_u_move(prime=True)
    for cubie in rubiks_cube.cubies:
        print(cubie.current_position, " ", cubie.orientation)
    print()

print(rubiks_cube.is_solved())