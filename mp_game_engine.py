import components
import random
from game_engine import attack, cli_coordinates_input, print_board

players = {}

# Pregenerate attack sequence to prevent duplicate attacks
def attack_sequence(board_size):
    coordinates = [i for i in range(board_size**2)]
    random.shuffle(coordinates)
    for i in coordinates:
        yield (int(i / 10), int(1 % 10))

def generate_attack(board_size=10):
    return next(attack_sequence(board_size))

def ai_opponent_game_loop():
    print("Welcome to Battleship")

    players["Player"] = {
        "board": components.place_battleships(components.initialise_board(), components.create_battleships(), "custom"),
        "battleships": components.create_battleships(),
    }

    players["AI"] = {
        "board": components.place_battleships(components.initialise_board(), components.create_battleships(), "random"),
        "battleships": components.create_battleships()
    }

    print("-" * 29)

    red = "\033[91m"
    green = "\033[92m"
    reset = "\033[0m"

    while True:
        # Print Boards
        print("AI's board")
        print_board(players["AI"]["board"])

        print("\nYour board")
        print_board(players["Player"]["board"])

        print("-" * 29)

        # Player attacks AI
        coordinates = cli_coordinates_input()

        print("-" * 29)

        hit_or_miss = attack(coordinates, players["AI"]["board"], players["AI"]["battleships"])
        print(f"You attacked {coordinates} - {green}Hit{reset}" if hit_or_miss else f"You attacked {coordinates} - {red}Miss{reset}")

        # All AI ships are sunk
        if all(ship_length == 0 for ship_length in players["AI"]["battleships"].values()):
            print(f"{green}You Won{reset}")
            break

        # AI attacks Player
        coordinates = generate_attack()

        hit_or_miss = attack(coordinates, players["Player"]["board"], players["Player"]["battleships"])
        print(f"AI  attacked {coordinates} - {red}Hit{reset}" if hit_or_miss else f"AI  attacked {coordinates} - {green}Miss{reset}")

        # All Player ships are sunk
        if all(ship_length == 0 for ship_length in players["Player"]["battleships"].values()):
            print(f"{red}AI Won{reset}")
            break

        print("-" * 29)

    # Game Over
    print("Game Over")

if __name__ == "__main__":
    ai_opponent_game_loop()