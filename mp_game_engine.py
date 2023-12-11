import components
import random
from game_engine import attack, cli_coordinates_input

players = {}

red = "\033[91m"
green = "\033[92m"
reset = "\033[0m"

def random_attack_algorithm(board_size):
    x = random.randint(0, board_size - 1)
    y = random.randint(0, board_size - 1)
    return (x, y)

def generate_attack(board_size=10, algorithm="random"):
    match algorithm:
        case "random":
            return random_attack_algorithm(board_size)
        case _:
            raise ValueError(f"The algorithm '{algorithm}' is invalid")

def print_board(board, board_history, show_ships=True):
    board_length = len(board)

    for y in range(board_length):
        for x in range(board_length):

            colour = red if (x, y) in board_history else reset

            shape = "##" if (board[y][x] is not None and show_ships) or board_history.get((x, y), False) else "::"

            print(f"{colour}{shape}{reset}", end=" ")

        print()

def ai_opponent_game_loop():
    print("Welcome to Battleship")

    players["Player"] = {
        "board": components.place_battleships(components.initialise_board(), components.create_battleships(), "custom"),
        "battleships": components.create_battleships(),
        "board_history": {} # Store the coords:result as (int, int):bool to track the AI's attack attempt history
    }

    players["AI"] = {
        "board": components.place_battleships(components.initialise_board(), components.create_battleships(), "random"),
        "battleships": components.create_battleships(),
        "board_history": {} # Store the coords:result as (int, int):bool to track the Player's attack attempt history
    }

    print("-" * 29)

    while True:
        # Print Boards
        print("AI's board")
        print_board(players["AI"]["board"], players["AI"]["board_history"], show_ships=False)

        print("\nYour board")
        print_board(players["Player"]["board"], players["Player"]["board_history"], show_ships=True)

        print("-" * 29)

        # Player attacks AI
        while True:
            coordinates = cli_coordinates_input()
            if coordinates not in players["AI"]["board_history"]:
                break
            print(f"You've already attacked {coordinates}")

        print("-" * 29)

        hit_or_miss = attack(coordinates, players["AI"]["board"], players["AI"]["battleships"])
        print(f"You attacked {coordinates} - {green}Hit{reset}" if hit_or_miss else f"You attacked {coordinates} - {red}Miss{reset}")
        players["AI"]["board_history"][coordinates] = hit_or_miss

        # All AI ships are sunk
        if all(ship_length == 0 for ship_length in players["AI"]["battleships"].values()):
            print(f"{green}You Won{reset}")
            break

        # AI attacks Player
        while True:
            coordinates = generate_attack()
            if coordinates not in players["Player"]["board_history"]:
                break

        hit_or_miss = attack(coordinates, players["Player"]["board"], players["Player"]["battleships"])
        print(f"AI  attacked {coordinates} - {red}Hit{reset}" if hit_or_miss else f"AI  attacked {coordinates} - {green}Miss{reset}")
        players["Player"]["board_history"][coordinates] = hit_or_miss

        # All Player ships are sunk
        if all(ship_length == 0 for ship_length in players["Player"]["battleships"].values()):
            print(f"{red}AI Won{reset}")
            break

        print("-" * 29)

    # Game Over
    print("Game Over")

    print("-" * 29)

    print("AI's board revealed")
    print_board(players["AI"]["board"], players["AI"]["board_history"], show_ships=True)

    print("\nYour board")
    print_board(players["Player"]["board"], players["Player"]["board_history"], show_ships=True)


if __name__ == "__main__":
    ai_opponent_game_loop()