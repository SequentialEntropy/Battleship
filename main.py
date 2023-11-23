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
    global placement
    return placement

if __name__ == "__main__":
    app.run(port=4000)