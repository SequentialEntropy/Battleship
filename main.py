from flask import Flask, request, render_template, jsonify
from mp_game_engine import players

import components

app = Flask(__name__)

ships = components.create_battleships()
board_size = 10

@app.route("/placement", methods=["GET", "POST"])
def placement_interface():
    if request.method == "GET":
        return render_template("placement.html", ships=ships, board_size=board_size)
    
    elif request.method == "POST":
        
        placement = request.json

        players["Player"] = {
            "board": components.place_battleships(components.initialise_board(), components.create_battleships(), "custom", placement),
            "battleships": components.create_battleships(),
            "board_history": {} # Store the coords:result as (int, int):bool to track the AI's attack attempt history
        }

        players["AI"] = {
            "board": components.place_battleships(components.initialise_board(), components.create_battleships(), "random"),
            "battleships": components.create_battleships(),
            "board_history": {} # Store the coords:result as (int, int):bool to track the Player's attack attempt history
        }

        return jsonify({"message": "Success!"})

@app.route("/")
def root():
    player_board = players["Player"]["board"]
    return render_template("main.html", player_board=player_board)

@app.route("/attack", methods=["GET"])
def process_attack():
    x = request.args.get("x")
    y = request.args.get("y")
    
    game_finished = False
    if game_finished:
        return jsonify({
            "hit": True,
            "AI_turn": (1, 2),
            "finished": "Game Over, player wins!"
        })
    else:
        return jsonify({
            "hit": False,
            "AI_Turn": (1, 2)
        })

if __name__ == "__main__":
    app.run(port=4000)