import random
import twophase.solver as sv
from collections import deque

from rubik.rubiks_cube import RubiksCube
from rubik.orientation import Orientation


def generate_scramble_sequence(length=20):
    possible_moves = set("RLUDFB")
    previous_move = ""
    
    if length < 1: return []
    
    sequence = []
    
    for i in range(length):
        random_value = random.randint(0, 2)
        
        if previous_move:
            move = previous_move = random.choice(list(possible_moves - set(previous_move)))
        else:
            move = previous_move = random.choice(list(possible_moves))
            
        match random_value:
            case 1: # counter-clockwise turn
                move = move + "'"
            case 2: # double turn
                move = move + "2"
        
        sequence.append(move)
    
    print("New sequence: ", sequence)
    return sequence

def generate_orientation_reset_sequence(cube: RubiksCube):
    """
    Generate a sequence of rotation moves to orientate the cube back to its normal orientation. 
    """
    
    start = cube.get_cube_orientation()
    identity = Orientation.identity()
    
    moves = [
        ("x", Orientation.rotated_x(-90)),
        ("x'", Orientation.rotated_x(90)),
        ("y", Orientation.rotated_y(-90)),
        ("y'", Orientation.rotated_y(90)),
        ("z", Orientation.rotated_z(-90)),
        ("z'", Orientation.rotated_z(90)),
    ]
    
    queue = deque([(start, [])])
    visited = {start}
    
    # Use BFS to find the sequence
    while queue:
        orientation, path = queue.popleft()
        if orientation == identity:
            return path
        
        for move, rotation in moves:
            next_orientation: Orientation = rotation * orientation # type: ignore

            if next_orientation in visited:
                continue
            
            visited.add(next_orientation)
            queue.append((next_orientation, path + [move]))
        
    return []

def generate_solution_sequence(cube: RubiksCube):
    cubestring = cube.serialize()
    
    solution = sv.solve(cubestring).split()
    solution.pop()
    
    return solution
