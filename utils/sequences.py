import math
import random

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