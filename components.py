import json
from algorithms import simple_placement_algorithm, random_placement_algorithm, custom_placement_algorithm

Board = list[list[str | None]]

def initialise_board(size: int = 10) -> Board:
    """Returns a square board initialised with `None`

    :param size: Width of the board,
        defaults to 10
    :type size: int, optional
    :return: 2D list of length `size` in both dimensions
    :rtype: list[list[None]]
    """
    return [[None for _ in range(size)] for _ in range(size)]

def create_battleships(filename: str = "battleships.txt") -> dict[str, int]:
    """Loads ship lengths from a config file

    :param filename: Name of config file,
        defaults to "battleships.txt"
    :type filename: str, optional
    :raises ValueError: If any line fails to match the `string:int` format
    :return: Dictionary with the key as the ship name
        and the value as the ship length
    :rtype: dict[str, int]
    """
    ships: dict[str, int] = {}
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
    """Returns a dict from the contents of a JSON file

    :param filename: Name of JSON file
    :type filename: str
    :return: Dictionary derived from parsed JSON
    :rtype: dict
    """    
    with open(filename, "r", encoding="utf-8") as file:
        return json.loads(file.read())

# Fourth parameter is only used to supply the custom_placement_algorithm with the placement JSON containing ship coordinates
def place_battleships(board: Board, ships: dict[str, int], algorithm: str = "simple", placement: dict[str, list[str]] = dict_from_json_file("placement.json")) -> Board:
    """Modifies board in-place, replacing `None` with the name of each ship

    :param board: Board to modify
    :type board: Board
    :param ships: Dictionary of all ship types and its length,
        does not contain any coordinates or rotation data
    :type ships: dict[str, int]
    :param algorithm: Type of placement algorithm to use,
        defaults to "simple"
    :type algorithm: str, optional
    :param placement: Dictionary of ship coordinates and corresponding
        rotations, only used for algorithms that benefit from user-specified
        configurations, such as `custom_placement_algorithm`,
        defaults to dict_from_json_file("placement.json")
    :type placement: dict[str, list[str]], optional
    :raises ValueError: If the `algorithm` argument does not match any
        algorithms defined in the match statement
    :return: A reference to the same instance as the original board passed in
        the `board` argument
    :rtype: Board
    """    
    match algorithm:
        case "simple":
            return simple_placement_algorithm(board, ships)
        case "random":
            return random_placement_algorithm(board, ships)
        case "custom":
            return custom_placement_algorithm(board, ships, placement)
        case _: # Raise an error if the algorithm argument is neither of the above
            raise ValueError(f"The algorithm '{algorithm}' is invalid")