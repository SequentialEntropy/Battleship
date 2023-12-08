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
        case _:
            raise InvalidAlgorithmException(algorithm)