def attack(coordinates, board, battleships):
    if board[coordinates[1]][coordinates[0]] is None: # Miss
        return False
    
    # Hit
    ship_name = board[coordinates[1]][coordinates[0]]

    board[coordinates[1]][coordinates[0]] = None

    battleships[ship_name] -= 1

    return True