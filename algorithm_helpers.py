# Define type aliases
Board = list[list[str | None]]

class ShipClashError(Exception):
    """Custom exception for ship placement attempted in an occupied cell"""

    def __init__(self, x: int, y: int, rotation: str, ship_length: int, ship_name: str = "Ship", obstructing_ship_name: str = "Ship") -> None:
        """Constructs an error message

        :param x: x-coordinate of target ship
        :type x: int
        :param y: y-coordinate of target ship
        :type y: int
        :param rotation: Rotation of target ship
        :type rotation: str
        :param ship_length: Length of target ship
        :type ship_length: int
        :param ship_name: Name of target ship,
            defaults to "Ship"
        :type ship_name: str, optional
        :param obstructing_ship_name: Name of ship obstructing target ship,
            defaults to "Ship"
        :type obstructing_ship_name: str, optional
        """
        super().__init__(
            f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' is obstructed by existing {obstructing_ship_name}"
        )

class ShipExceedsBoardBoundsError(Exception):
    """Custom exception for when ship would extend outside the board bounds"""

    def __init__(self, x: int, y: int, rotation: str, ship_length: int, ship_name: str = "Ship", board_size: int | None = None) -> None:
        """Constructs an error message

        :param x: x-coordinate of target ship
        :type x: int
        :param y: y-coordinate of target ship
        :type y: int
        :param rotation: Rotation of target ship
        :type rotation: str
        :param ship_length: Length of target ship
        :type ship_length: int
        :param ship_name: Name of target ship,
            defaults to "Ship"
        :type ship_name: str, optional
        :param board_size: Size of board,
            defaults to None
        :type board_size: int | None, optional
        """
        if board_size is None:
            super().__init__(
                f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' does not fit the board"
            )

        else:
            super().__init__(
                f"{ship_name} of length {ship_length} positioned at ({x}, {y}) with rotation '{rotation}' does not fit the board of size {board_size}"
            )

class MaxAttemptsReached(Exception):
    """Custom exception for when ship placement attempts exceed a threshold"""
    
    def __init__(self, attempts: int) -> None:
        """Constructs an error message

        :param attempts: Number of attempts made - same as max attempts
        :type attempts: int
        """
        super().__init__(
            f"Max attempts ({attempts}) reached"
        )
    


def fit_ship(board: Board, x: int, y: int, rotation: str, ship_length: int, ship_name: str) -> bool:
    """Modifies board in-place updating the coordinates the ship would occupy

    Changes the value stored in each coordinate in the board
    from `None` to the `ship_name`

    :param board: Board to modify
    :type board: Board
    :param x: x-coordinate of target ship
    :type x: int
    :param y: y-coordinate of target ship
    :type y: int
    :param rotation: Rotation of target ship
    :type rotation: str
    :param ship_length: Length of target ship
    :type ship_length: int
    :param ship_name: Name of target ship
    :type ship_name: str
    :raises ShipExceedsBoardBoundsError: When ship would overflow board bounds
    :raises ValueError: When the rotation is neither 'h' nor 'v'
    :raises ShipClashError: When any space the ship would occupy already has an
        existing ship placed there
    :return: Success or fail
    :rtype: bool
    """    
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

    

    """
    Having two loops is necessary to prevent the board from having an invalid state
    by making sure the boat is either fully placed or rejected and not in-between

    As the board is modified *in-place* and *not on a copy*, we have to make sure
    the function doesn't exit midway through the loop because of a clash being detected
    '''
    """

    # First loop is a preliminary check to determine if all cells in a given ship length are occupied by another ship
    for coord in ship_coords:
        # Check if coordinates in the board is occupied (clash detection)
        obstructing_ship_name = board[coord[1]][coord[0]]
        if obstructing_ship_name is not None:
            raise ShipClashError(x, y, rotation, ship_length, ship_name, obstructing_ship_name)

    # Second loop is in charge of actually placing the ship (modifying board)
    for coord in ship_coords:
        board[coord[1]][coord[0]] = ship_name
    
    # Ship is fitted onto the board successfully
    return True