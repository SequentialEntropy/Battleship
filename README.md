# Battleship

## Introduction

This is a Python project recreating the classic board game, *Battleship*, implementing a web interface through Flask (For ECM1400).

[Sphinx Documentation](https://htmlpreview.github.io/?https://github.com/SequentialEntropy/Battleship/blob/master/docs/_build/html/modules.html)

## Design Choices (200 word Self-Assessment)

Each game is represented through data in the `players` dictionary in `mp_game_engine.py`. This is imported in `main.py` to *prevent* defining player and board data with the `global` keyword. The **players** and **AI** are both represented in the *same format* within this `players` dictionary to make **players** and **AI** *functionally equivalent*. The AI is essentially another instance of `player` with the *inputted vs generated* attack coordinates being the sole difference. This allows functions such as `attack` (`game_engine.py`) and `place_battleships` (`components.py`). Future developments are thus, made easier for player vs player games, implemented by making *both instances* of `player` use *inputted coordinates*. This would be an idea for further development beyond the original specifications. Custom error messages were implemented by providing verbose messages on why errors occurred in the *specific* context of the Battleship game (`algorithm_helpers.py`). To make it easier to create new placement and attack algorithms, both are defined using a *match case* statement. This means a developer can add new algorithms just by importing the function and adding a new `case`. Custom battleships can be defined as well, by editing `battleships.txt`.

## Further Expansions beyond the Specifications
One expansion featured in this project is using a more sophisticated AI to perform the `generate_attack` function (`mp_game_engine.py`). This new algorithm initially randomly targets coordinates, similar to the original coursework specifications. However, when the algorithm detects a successful hit, it then narrows down to targeting the adjacent tiles and exhausting all possible directions a ship could be, before reverting to random attacks. When playing against this AI, it felt significantly challenging, which allowed users to change the difficulty of the game.

## Prerequisites

This project was developed on the Python 3.10.5 environment.

Check to see if your Python version matches
```
python3 --version
```

Dependencies are separated for general users and for developers.

## How to Use (General Users)
To install the core dependencies required to run the code, use `requirements.txt`.
1. Open the command-line
2. Ensure the correct directory is opened, change the directory if needed.
```
cd Battleship-master
```
3. List the files in the directory
```
ls
```
4. Check if this `README.md` file is shown
5. Install the core dependencies
```
python3 -m pip install -r requirements.txt
```
6. Before running the code, move into the `Battleship` directory
```
cd Battleship
```
7. Run the Flask server
```
python3.10 main.py
```
8. Open the web interface through the browser
```
http://0.0.0.0:4000/placement
```

## How to Use (For Devolopers and Contributors)
To install additional dependencies such as `pytest`, use `requirements-dev.txt`.

1. Open the command-line
2. Ensure the correct directory is opened, change the directory if needed.
```
cd Battleship-master
```
3. List the files in the directory
```
ls
```
4. Check if this `README.md` file is shown
5. Install the developer dependencies
```
python3 -m pip install -r requirements-dev.txt
```

## Details

Published as a [GitHub Repository](https://github.com/SequentialEntropy/Battleship).

Project licensed with the [MIT License](LICENSE)

Documentation generated with [Sphinx](https://htmlpreview.github.io/?https://github.com/SequentialEntropy/Battleship/blob/master/docs/_build/html/modules.html)

Author - Candidate 123166
