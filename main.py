from flask import Flask, request, render_template, jsonify, Response
from mp_game_engine import players, attack, generate_attack

import components

app = Flask(__name__)

ships = components.create_battleships()
board_size = 10

@app.route("/placement", methods=["GET", "POST"])
def placement_interface() -> str | Response:
    match request.method:
        case "GET":
            return render_template("placement.html", ships=ships, board_size=board_size)
    
        case "POST":
        
            placement = request.get_json()

            players["Player"] = {
                "board": components.place_battleships(components.initialise_board(board_size), components.create_battleships(), "custom", placement),
                "battleships": components.create_battleships(),
                "board_history": {} # Store the coords:result as (int, int):bool to track the AI's attack attempt history
            }

            players["AI"] = {
                "board": components.place_battleships(components.initialise_board(board_size), components.create_battleships(), "random"),
                "battleships": components.create_battleships(),
                "board_history": {} # Store the coords:result as (int, int):bool to track the Player's attack attempt history
            }

            return jsonify({"message": "Success!"})
        case _: # Theoretically unreachable clause, but to adhere to return type declaration
            return "Method Not Allowed"

@app.route("/")
def root() -> str:
    player_board = players["Player"]["board"]
    return render_template("main.html", player_board=player_board)

@app.route("/attack", methods=["GET"])
def process_attack() -> tuple[str, int] | Response:

    # Player attacks AI
    x = request.args.get("x", default=-1, type=int)
    y = request.args.get("y", default=-1, type=int)
    coordinates = (x, y)

    if coordinates in players["AI"]["board_history"]:
        # Prevent showing "undefined" in game log by not returning JSON, causing a 409 and a parsing error on the client
        # Although this shows as an error in the browser console, this is not visible to the user
        return f"You've already attacked {coordinates}", 409

    try:
        hit_or_miss_ai_board = attack(coordinates, players["AI"]["board"], players["AI"]["battleships"])
        players["AI"]["board_history"][coordinates] = hit_or_miss_ai_board
    except IndexError:
        return f"{coordinates} is not within board of size {board_size}", 400

    # AI attacks Player
    while True:
        coordinates = generate_attack(board_size)
        if coordinates not in players["Player"]["board_history"]:
            break

    hit_or_miss_player_board = attack(coordinates, players["Player"]["board"], players["Player"]["battleships"])
    players["Player"]["board_history"][coordinates] = hit_or_miss_player_board

    # All AI ships are sunk
    if all(ship_length == 0 for ship_length in players["AI"]["battleships"].values()):
        return jsonify({
            "hit": hit_or_miss_ai_board,
            "AI_Turn": coordinates,
            "finished": "Game Over, Player wins!"
        })

    # All Player ships are sunk
    elif all(ship_length == 0 for ship_length in players["Player"]["battleships"].values()):
        return jsonify({
            "hit": hit_or_miss_ai_board,
            "AI_Turn": coordinates,
            "finished": "Game Over, AI wins!"
        })
    
    else:
        return jsonify({
            "hit": hit_or_miss_ai_board,
            "AI_Turn": coordinates
        })

if __name__ == "__main__":
    app.run(port=4000)