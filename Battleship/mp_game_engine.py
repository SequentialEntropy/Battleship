import components
import random
from game_engine import attack, cli_coordinates_input
from typing import Any

# Define type aliases
Board = list[list[str | None]]
Coordinates = tuple[int, int]

players: dict[str, dict[str, Any]] = {}

grey = "\033[90m"
red = "\033[91m"
green = "\033[92m"
aqua = "\033[96m"
reset = "\033[0m"

def random_attack_algorithm(board_size: int) -> Coordinates:
    """Generates random x and y coordinates within range of given `board_size`

    :param board_size: Range for random number generator
    :type board_size: int
    :return: Tuple of random `int` pair representing x and y coordinates
    :rtype: Coordinates
    """
    x = random.randint(0, board_size - 1)
    y = random.randint(0, board_size - 1)
    return (x, y)

def adjacent_attack_algorithm(board_size, board_history, memory):
    # First move is always random
    if board_history == {}:
        return random_attack_algorithm(board_size)
    
    # If directions_to_attack doesn't exist, initialise it
    if "directions_to_attack" not in memory:
        memory["directions_to_attack"] = []

    current_coordinates = list(board_history)[-1] # Most recent attack
    current_hit_or_miss = board_history[current_coordinates]

    # If current_coordinates were random coordinates but resulted in a hit
    if current_hit_or_miss and memory["directions_to_attack"] == []:
        # Then, initialise initial_hit_coordinates and directions_to_attack
        memory["initial_hit_coordinates"] = current_coordinates
        memory["directions_to_attack"] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # Make the AI's choice of direction less predictable in order
        random.shuffle(memory["directions_to_attack"])

    # Ensure the loop runs at least once - the current coordinates are already in board_history
    next_coordinate = current_coordinates

    while next_coordinate in board_history:

        # If current_coordinates was the first miss in this direction
        if len(memory["directions_to_attack"]) > 0 and not current_hit_or_miss:
            # Then there's nothing else to check in this direction - so pop this direction
            memory["directions_to_attack"].pop(0)
            current_coordinates = memory["initial_hit_coordinates"]
        
        # If there's no directions to check and current_coordinates was a miss
        if len(memory["directions_to_attack"]) == 0 and not current_hit_or_miss:
            # This means a random stranded attack, no previous adjacent hits have been made
            # Continue attacking randomly
            return random_attack_algorithm(board_size)

        # If this direction isn't exhausted
        if len(memory["directions_to_attack"]) > 0:
            # Continue advancing the attacks toward the same direction
            next_direction = memory["directions_to_attack"][0]

            next_coordinate = (
                current_coordinates[0] + next_direction[0],
                current_coordinates[1] + next_direction[1]
            )

            if next_coordinate[0] not in range(board_size) or next_coordinate[1] not in range(board_size):
                memory["directions_to_attack"].pop(0)
                return current_coordinates

            # If the coordinate has already been attacked
            if next_coordinate in board_history:
                current_coordinates = next_coordinate
                current_hit_or_miss = board_history[next_coordinate]
                continue # Skip to the next cell in the same direction

            return next_coordinate

def generate_attack(board_size: int = 10, algorithm: str = "random", board_history: dict[tuple[int, int], bool] = {}, memory: dict = None) -> Coordinates:
    # TODO rewrite docstring
    """Generates AI attack coordinates based on `algorithm`

    :param board_size: Size of board,
        defaults to 10
    :type board_size: int, optional
    :param algorithm: Algorithm used,
        defaults to "random"
    :type algorithm: str, optional
    :raises ValueError: When `algorithm` does not match any defined algorithms
    :return: Tuple `int` pair representing x and y coordinates of AI's turn
    :rtype: Coordinates
    """
    match algorithm:
        case "random":
            return random_attack_algorithm(board_size)
        case "adjacent":
            return adjacent_attack_algorithm(board_size, board_history, memory)
        case _:
            raise ValueError(f"The algorithm '{algorithm}' is invalid")

def print_board(board: Board, board_history: dict[Coordinates, bool], show_ships: bool = True) -> None:
    """Prints an ASCII representation of the board's state with grid headings

    :param board: Board to display
    :type board: Board
    :param board_history: `Coordinates:bool` pair to track attacked cell colour
    :type board_history: dict[Coordinates, bool]
    :param show_ships: Show or hide ships not yet revealed in `board_history`,
        defaults to True
    :type show_ships: bool, optional
    """
    board_size = len(board)

    print(" ".join([" ", grey] + [" " * (2 - len(str(i))) + str(i) for i in range(board_size)] + [reset]))
    for y in range(board_size):
        print(grey + " " * (2 - len(str(y))) + str(y), end=reset + " ")
        for x in range(board_size):
            
            colour = (red if board_history[(x, y)] else aqua) if (x, y) in board_history else reset

            shape = "##" if (board[y][x] is not None and show_ships) or ((x, y) in board_history) else "::"

            print(f"{colour}{shape}{reset}", end=" ")

        print()

def ai_opponent_game_loop() -> None:
    """Fully functional player vs AI game loop on the command-line"""

    print("Welcome to Battleship")

    print("-" * 32)

    algorithms = ["random", "adjacent"]

    while True:
        print("Choose an AI algorithm:")
        for i in range(len(algorithms)):
            print(f"{i} - {algorithms[i]}")
        try:
            choice = int(input("Choice: "))
            algorithm = algorithms[choice]
            break
        except ValueError:
            continue
        except IndexError:
            continue

    players["Player"] = {
        "board": components.place_battleships(components.initialise_board(), components.create_battleships(), "custom"),
        "battleships": components.create_battleships(),
        "board_history": {} # Store the coords:result as (int, int):bool to track the AI's attack attempt history
    }

    players["AI"] = {
        "board": components.place_battleships(components.initialise_board(), components.create_battleships(), "random"),
        "battleships": components.create_battleships(),
        "board_history": {}, # Store the coords:result as (int, int):bool to track the Player's attack attempt history
        "memory": {}
    }

    print("-" * 32)

    while True:
        # Print Boards
        print("AI's board")
        print_board(players["AI"]["board"], players["AI"]["board_history"], show_ships=False)

        print("\nYour board")
        print_board(players["Player"]["board"], players["Player"]["board_history"], show_ships=True)

        print("-" * 32)

        # Player attacks AI
        while True:
            coordinates = cli_coordinates_input()
            if coordinates not in players["AI"]["board_history"]:
                break
            print(f"You've already attacked {coordinates}")

        print("-" * 32)

        hit_or_miss = attack(coordinates, players["AI"]["board"], players["AI"]["battleships"])
        print(f"You attacked {coordinates} - {green}Hit{reset}" if hit_or_miss else f"You attacked {coordinates} - {red}Miss{reset}")
        players["AI"]["board_history"][coordinates] = hit_or_miss

        # All AI ships are sunk
        if all(ship_length == 0 for ship_length in players["AI"]["battleships"].values()):
            print(f"{green}You Won{reset}")
            break

        # AI attacks Player
        while True:
            coordinates = generate_attack(len(players["Player"]["board"]), algorithm=algorithm, board_history=players["Player"]["board_history"], memory=players["AI"]["memory"])
            if coordinates not in players["Player"]["board_history"]:
                break

        hit_or_miss = attack(coordinates, players["Player"]["board"], players["Player"]["battleships"])
        print(f"AI  attacked {coordinates} - {red}Hit{reset}" if hit_or_miss else f"AI  attacked {coordinates} - {green}Miss{reset}")
        players["Player"]["board_history"][coordinates] = hit_or_miss

        # All Player ships are sunk
        if all(ship_length == 0 for ship_length in players["Player"]["battleships"].values()):
            print(f"{red}AI Won{reset}")
            break

        print("-" * 32)

    # Game Over
    print("Game Over")

    print("-" * 32)

    print("AI's board revealed")
    print_board(players["AI"]["board"], players["AI"]["board_history"], show_ships=True)

    print("\nYour board")
    print_board(players["Player"]["board"], players["Player"]["board_history"], show_ships=True)


if __name__ == "__main__":
    ai_opponent_game_loop()