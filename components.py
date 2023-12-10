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

def dict_from_json_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.loads(file.read())

# Fourth parameter is only used to supply the custom_placement_algorithm with the placement JSON containing ship coordinates
def place_battleships(board, ships, algorithm="simple", placement=dict_from_json_file("placement.json")):
    match algorithm:
        case "simple":
            return simple_placement_algorithm(board, ships)
        case "random":
            return random_placement_algorithm(board, ships)
        case "custom":
            return custom_placement_algorithm(board, ships, placement)
        case _: # Raise an error if the algorithm argument is neither of the above
            raise ValueError(f"The algorithm '{algorithm}' is invalid")