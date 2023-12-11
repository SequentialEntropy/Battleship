class ShipClashError(Exception):
    def __init__(self, x, y, rotation, ship_length, ship_name="Ship", obstructing_ship_name="Ship"):
        super().__init__(
            f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' is obstructed by existing {obstructing_ship_name}"
        )

class ShipExceedsBoardBoundsError(Exception):
    def __init__(self, x, y, rotation, ship_length, ship_name="Ship", board_size=None):
        if board_size is None:
            super().__init__(
                f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' does not fit the board"
            )

        else:
            super().__init__(
                f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' does not fit the board of size {board_size}"
            )

class MaxAttemptsReached(Exception):
    def __init__(self, attempts):
        super().__init__(
            f"Max attempts ({attempts}) reached"
        )
    


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
            raise ValueError(f"The rotation '{rotation}' is invalid, it must be either 'h' or 'v'")

    

    '''
    Having two loops is necessary to prevent the board from having an invalid state
    by making sure the boat is either fully placed or rejected and not in-between

    As the board is modified *in-place* and *not on a copy*, we have to make sure
    the function doesn't exit midway through the loop because of a clash being detected
    '''

    # First loop is a preliminary check to determine if all cells in a given ship length are occupied by another ship
    for coord in ship_coords:
        # Check if coordinates in the board is occupied (clash detection)
        if board[coord[1]][coord[0]] is not None:
            raise ShipClashError(x, y, rotation, ship_length, ship_name, board[coord[1]][coord[0]])

    # Second loop is in charge of actually placing the ship (modifying board)
    for coord in ship_coords:
        board[coord[1]][coord[0]] = ship_name
    
    # Ship is fitted onto the board successfully
    return True