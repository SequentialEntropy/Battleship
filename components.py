import json
from algorithms import simple_placement_algorithm, random_placement_algorithm, custom_placement_algorithm

def initialise_board(size: int = 10) -> list[list[int]]:
    return [[None for _ in range(size)] for _ in range(size)]

def create_battleships(filename: str = "battleships.txt") -> dict[str, int]:
    ships = {}
    with open(filename) as file:

        for line in file:
            data = line.strip().split(":")
            try:
                ship_name, ship_length = data
                ships[ship_name] = int(ship_length)
            except ValueError as e:
                raise ValueError(f"'{line}' in {filename} does not follow the 'ship_name:ship_length' format") from e

        return ships

def dict_from_json_file(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as file:
        return json.loads(file.read())

# Fourth parameter is only used to supply the custom_placement_algorithm with the placement JSON containing ship coordinates
def place_battleships(board: list[list[str | None]], ships: dict[str, int], algorithm: str = "simple", placement: dict[str, list[str]] = dict_from_json_file("placement.json")) -> list[list[str | None]]:
    match algorithm:
        case "simple":
            return simple_placement_algorithm(board, ships)
        case "random":
            return random_placement_algorithm(board, ships)
        case "custom":
            return custom_placement_algorithm(board, ships, placement)
        case _: # Raise an error if the algorithm argument is neither of the above
            raise ValueError(f"The algorithm '{algorithm}' is invalid")