import random

from algorithm_helpers import MaxAttemptsReached, ShipClashError, fit_ship

# Define type aliases
Board = list[list[str | None]]

def simple_placement_algorithm(board: Board, ships: dict[str, int]) -> Board:
    row = 0
    for ship_name in ships:
        ship_length = ships[ship_name]
        board[row][:ship_length] = [ship_name for _ in range(ship_length)]
        row += 1

    return board



def random_placement_algorithm(board: Board, ships: dict[str, int], max_attempts: int = 100) -> Board:
    board_size = len(board)

    for ship_name in ships:
        ship_length = ships[ship_name]

        error = None
        for _ in range(max_attempts): # Repeatedly attempt fitting a ship onto a board
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
            except ShipClashError as e:
                error = e
                continue # Move onto the next attempt

        else: # If loop exits without breaking
            raise MaxAttemptsReached(max_attempts) from error
    
    return board



def custom_placement_algorithm(board: Board, ships: dict[str, int], placement: dict[str, list[str]]) -> Board:
    for ship_name in ships:
        ship_length = ships[ship_name]

        # TODO Catch ValueError when x and y are not of type "int"
        x = int(placement[ship_name][0])
        y = int(placement[ship_name][1])
        rotation = placement[ship_name][2]

        fit_ship(board, x, y, rotation, ship_length, ship_name)

    return board