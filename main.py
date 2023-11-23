from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

ships = {
    "Aircraft_Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2,
}
board_size = 10
placement = {}
player_board = [[None for _ in range(10)] for _ in range(10)]

@app.route("/placement", methods=["GET", "POST"])
def placement_interface():
    global placement

    if request.method == "GET":
        return render_template("placement.html", ships=ships, board_size=board_size)
    
    elif request.method == "POST":
        
        placement = request.json
        return jsonify({"message": "Success!"})

@app.route("/")
def root():
    # global placement
    # return placement
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