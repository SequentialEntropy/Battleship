import random

def initialise_board(size=10):
    return [[None for _ in range(10)] for _ in range(10)]

def create_battleships(filename="battleships.txt"):
    with open(filename) as file:
        # TODO Input validation, check for "string:int" format for each line
        lines = file.readlines()

        ships = {line.split(":")[0]: int(line.split(":")[1].replace("\n", "")) for line in lines}

        return ships





def simple_placement_algorithm(board, ships):
    row = 0
    for ship in ships:
        ship_length = ships[ship]
        board[row][:ship_length] = [ship for _ in range(ship_length)]
        row += 1
    return board

class ShipObstructedException(Exception):
    def __init__(self, x, y, rotation, ship_length, ship_name="Ship", obstructing_ship_name="Ship"):
        self.message = f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' is obstructed by existing {obstructing_ship_name}"
    def __str__(self):
        return self.message

class ShipExceedsBoardBoundsException(Exception):
    def __init__(self, x, y, rotation, ship_length, ship_name="Ship", board_size=None):
        if board_size is None:
            self.message = f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' does not fit the board"
        else:
            self.message = f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' does not fit the board of size {board_size}"
    def __str__(self):
        return self.message

class InvalidShipRotationException(Exception):
    def __init__(self, rotation):
        self.message = f"The rotation '{rotation}' is not acceptable, it must be either 'h' or 'v'"
    def __str__(self):
        return self.message

def fit_ship(board, x, y, rotation, ship_length, ship_name):
    board_size = len(board)

    match rotation:
        case "h":
            if x + ship_length > board_size: # If ship pokes out the right side of the board, throw an error
                raise ShipExceedsBoardBoundsException(x, y, rotation, ship_length, ship_name, board_size)
                return False
            ship_coords = [(i, y) for i in range(x, x + ship_length)]
        case "v":
            if y + ship_length > board_size: # If ship pokes out the bottom side of the board, throw an error
                raise ShipExceedsBoardBoundsException(x, y, rotation, ship_length, ship_name, board_size)
                return False
            ship_coords = [(x, i) for i in range(y, y + ship_length)]
        case _:
            raise InvalidShipRotationException(rotation)
            return False

    # Preliminary check to determine if there is clearance to place the ship, since the board is modified in-place
    for coord in ship_coords:
        # Check if coordinates in the board is occupied
        if board[coord[1]][coord[0]] is not None:
            raise ShipObstructedException(x, y, rotation, ship_length, ship_name, board[coord[1]][coord[0]])
            return False

    for coord in ship_coords:
        board[coord[1]][coord[0]] = ship_name
    
    # Ship is fitted onto the board successfully
    return True

def random_placement_algorithm(board, ships):
    board_size = len(board)

    for ship in ships:
        ship_length = ships[ship]

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
                if fit_ship(board, x, y, rotation, ship_length, ship):
                    break # Stop attempting to place a ship
            except ShipObstructedException:
                pass # Catch a failed attempt at placing a ship
    
    return board

# Custom exception for an invalid algorithm, where the algorithm is not defined as an option in place_battleships
class InvalidAlgorithmException(Exception):
    def __init__(self, algorithm):
        self.message = f"The algorithm '{algorithm}' is not defined"
    def __str__(self):
        return self.message

def place_battleships(board, ships, algorithm="simple"):
    match algorithm:
        case "simple":
            return simple_placement_algorithm(board, ships)
        case "random":
            return random_placement_algorithm(board, ships)
        case _:
            raise InvalidAlgorithmException(algorithm)