import components

# Define type aliases
Board = list[list[str | None]]
Coordinates = tuple[int, int]

def attack(coordinates: Coordinates, board: Board, battleships: dict[str, int]) -> bool:
    """Returns if attack hits a ship and updates the board and ship counters

    If the target coordinate is already `None`, the attack is a miss.
    If the attack hits, it reverts the target coordinate to `None`,
    then, the corresponding ship counter in the dictionary will decrement by 1.

    :param coordinates: Coordinates of the attack
    :type coordinates: Coordinates
    :param board: Board to target and modify
    :type board: Board
    :param battleships: Dictionary of ships and its corresponding lengths
    :type battleships: dict[str, int]
    :return: Success or failure of the attack
    :rtype: bool
    """
    ship_name = board[coordinates[1]][coordinates[0]]

    if ship_name is None: # Miss
        return False
    
    # Hit
    board[coordinates[1]][coordinates[0]] = None

    battleships[ship_name] -= 1

    return True

def cli_coordinates_input(board_size: int = 10) -> Coordinates:
    """Prompts the user for a valid coordinate input through the command-line

    :param board_size: Size of board for range validation check,
        defaults to 10
    :type board_size: int, optional
    :return: Tuple pair of int representing x and y coordinates
    :rtype: Coordinates
    """
    while True:
        val = input("Attack x-coordinate: ")
        try:
            x = int(val)

            if x not in range(board_size):
                print(f"{x} does not fit within 0 to {board_size - 1}")
                continue

            break
        except ValueError:
            print(f"{val} is not a number")

    while True:
        val = input("Attack y-coordinate: ")
        try:
            y = int(val)

            if y not in range(board_size):
                print(f"{y} does not fit within 0 to {board_size - 1}")
                continue

            break
        except ValueError:
            print(f"{val} is not a number")

    return (x, y)

def print_board(board: Board, show_acronym: bool = True) -> None:
    """Prints an ASCII representation of the board's state

    If `show_acronym` is `True`, each cell with a ship will be represented
    with the first two characters of the ship name. Mainly for debugging.
    If `show_acronym` is `False`, each cell with a ship will be represented
    as `##`
    Any unoccupied cells will be represented as `::`

    :param board: Board to display
    :type board: Board
    :param show_acronym: Represent occupied cells with 2 character
        ship name acronyms,
        defaults to True
    :type show_acronym: bool, optional
    """
    for row in board:
        for cell in row:
            if cell is None:
                print("::", end=" ")
            else:
                print(cell[:2] if show_acronym else "##", end=" ")
        print()

def simple_game_loop() -> None:
    """Simple game loop with one player, one board and ships always revealed"""
    
    print("Welcome to Battleship")

    board = components.initialise_board()
    ships = components.create_battleships()

    components.place_battleships(board, ships, "custom")

    print("-" * 29)

    while not all(ship_length == 0 for ship_length in ships.values()):

        print_board(board, show_acronym=False)

        print("-" * 29)

        hit_or_miss = attack(cli_coordinates_input(), board, ships)

        print("-" * 29)

        print("Hit" if hit_or_miss else "Miss")
        
        print("-" * 29)

    print("Game Over")

if __name__ == "__main__":
    simple_game_loop()