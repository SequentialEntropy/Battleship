import components

# Define type aliases
Board = list[list[str | None]]
Coordinates = tuple[int, int]

def attack(coordinates: Coordinates, board: Board, battleships: dict[str, int]) -> bool:

    ship_name = board[coordinates[1]][coordinates[0]]

    if ship_name is None: # Miss
        return False
    
    # Hit
    board[coordinates[1]][coordinates[0]] = None

    battleships[ship_name] -= 1

    return True

def cli_coordinates_input(board_size: int = 10) -> Coordinates:
    
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
    for row in board:
        for cell in row:
            if cell is None:
                print("::", end=" ")
            else:
                print(cell[:2] if show_acronym else "##", end=" ")
        print()

def simple_game_loop() -> None:
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