import json
from algorithms import simple_placement_algorithm, random_placement_algorithm, custom_placement_algorithm

def initialise_board(size=10):
    return [[None for _ in range(size)] for _ in range(size)]

def create_battleships(filename="battleships.txt"):
    with open(filename) as file:
        # TODO Input validation, check for "string:int" format for each line
        lines = file.readlines()

        ships = {line.split(":")[0]: int(line.split(":")[1].replace("\n", "")) for line in lines}

        return ships

def placement_from_file(filename="placement.json"):
    with open(filename) as file:
        placement_json = file.read()
        placement_dict = json.loads(placement_json)
        return placement_dict

# Fourth parameter is only used to supply the custom_placement_algorithm with the placement JSON containing ship coordinates
def place_battleships(board, ships, algorithm="simple", placement=placement_from_file("placement.json")):
    match algorithm:
        case "simple":
            return simple_placement_algorithm(board, ships)
        case "random":
            return random_placement_algorithm(board, ships)
        case "custom":
            return custom_placement_algorithm(board, ships, placement)
        case _: # Raise an error if the algorithm argument is neither of the above
            raise ValueError(f"The algorithm '{algorithm}' is invalid")