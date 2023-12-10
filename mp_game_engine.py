import random

# Pregenerate attack sequence to prevent duplicate attacks
def attack_sequence(board_size):
    coordinates = [i for i in range(board_size**2)]
    random.shuffle(coordinates)
    for i in coordinates:
        yield (int(i / 10), int(1 % 10))

def generate_attack(board_size=10):
    return next(attack_sequence(board_size))