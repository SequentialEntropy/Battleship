def attack(coordinates, board, battleships):
    if board[coordinates[1]][coordinates[0]] is None: # Miss
        return False
    
    # Hit
    ship_name = board[coordinates[1]][coordinates[0]]

    board[coordinates[1]][coordinates[0]] = None

    battleships[ship_name] -= 1

    return True

def cli_coordinates_input():
    
    while True:
        val = input("Enter the x-coordinate to attack: ")
        try:
            x = int(val)
            break
        except ValueError:
            print(f"{val} is not a number")

    while True:
        val = input("Enter the y-coordinate to attack: ")
        try:
            y = int(val)
            break
        except ValueError:
            print(f"{val} is not a number")

    return (x, y)