import random
import json

def initialise_board(size=10):
    return [[None for _ in range(size)] for _ in range(size)]

def create_battleships(filename="battleships.txt"):
    with open(filename) as file:
        # TODO Input validation, check for "string:int" format for each line
        lines = file.readlines()

        ships = {line.split(":")[0]: int(line.split(":")[1].replace("\n", "")) for line in lines}

        return ships





def simple_placement_algorithm(board, ships):
    row = 0
    for ship_name in ships:
        ship_length = ships[ship_name]
        board[row][:ship_length] = [ship_name for _ in range(ship_length)]
        row += 1
    return board

class ShipClashError(Exception):
    def __init__(self, x, y, rotation, ship_length, ship_name="Ship", obstructing_ship_name="Ship"):
        self.message = f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' is obstructed by existing {obstructing_ship_name}"
    def __str__(self):
        return self.message

class ShipExceedsBoardBoundsError(Exception):
    def __init__(self, x, y, rotation, ship_length, ship_name="Ship", board_size=None):
        if board_size is None:
            self.message = f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' does not fit the board"
        else:
            self.message = f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' does not fit the board of size {board_size}"
    def __str__(self):
        return self.message

class InvalidShipRotationError(Exception):
    def __init__(self, rotation):
        self.message = f"The rotation '{rotation}' is not acceptable, it must be either 'h' or 'v'"
    def __str__(self):
        return self.message

def fit_ship(board, x, y, rotation, ship_length, ship_name):
    board_size = len(board)

    match rotation:
        case "h":
            if x + ship_length > board_size: # If ship pokes out the right side of the board, raise an error
                raise ShipExceedsBoardBoundsError(x, y, rotation, ship_length, ship_name, board_size)

            ship_coords = [(i, y) for i in range(x, x + ship_length)]

        case "v":
            if y + ship_length > board_size: # If ship pokes out the bottom side of the board, raise an error
                raise ShipExceedsBoardBoundsError(x, y, rotation, ship_length, ship_name, board_size)

            ship_coords = [(x, i) for i in range(y, y + ship_length)]

        case _:
            raise InvalidShipRotationError(rotation)

    

    # Having two loops is necessary to prevent the board from having an invalid state
    # by making sure the boat is either fully placed or rejected and not in-between

    # As the board is modified in-place and not on a copy, we have to make sure
    # the function doesn't exit midway through the loop because of a clash being detected

    # First loop is a preliminary check to determine if all cells in a given ship length are occupied by another ship
    for coord in ship_coords:
        # Check if coordinates in the board is occupied (clash detection)
        if board[coord[1]][coord[0]] is not None:
            raise ShipClashError(x, y, rotation, ship_length, ship_name, board[coord[1]][coord[0]])

    # Second loop is in charge of actually placing the ship
    for coord in ship_coords:
        board[coord[1]][coord[0]] = ship_name
    
    # Ship is fitted onto the board successfully
    return True

def random_placement_algorithm(board, ships):
    board_size = len(board)

    for ship_name in ships:
        ship_length = ships[ship_name]

        while True: # Repeatedly attempt fitting a ship onto a board
            rotation = random.choice(["h", "v"])

            # Prevent ship exceeding board bounds
            if rotation == "h":
                x = random.randint(0, board_size - 1 - ship_length)
                y = random.randint(0, board_size - 1)
            elif rotation == "v":
                x = random.randint(0, board_size - 1)
                y = random.randint(0, board_size - 1 - ship_length)

            try:
                if fit_ship(board, x, y, rotation, ship_length, ship_name):
                    break # Stop attempting to place a ship
            except ShipClashError:
                pass # Catch a failed attempt at placing a ship
    
    return board

def custom_placement_algorithm(board, ships, placement):
    for ship_name in ships:
        ship_length = ships[ship_name]

        # TODO Catch ValueError when x and y are not of type "int"
        x = int(placement[ship_name][0])
        y = int(placement[ship_name][1])
        rotation = placement[ship_name][2]

        fit_ship(board, x, y, rotation, ship_length, ship_name)

    return board

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