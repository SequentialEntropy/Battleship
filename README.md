# Battleship

  

The README file should include a list of all features that you consider are complete followed by a typical README file structure. The self-assessment must be less than 200 words and understandable within 1 minute. The subsequent README must make it clear how to execute the project, the license and any other relevant details.

  

## Introduction

This is a Python project recreating the classic board game, *Battleship*, implementing a web interface through Flask (For ECM1400).

## Design Choices (200 word Self-Assessment)

Each game is represented through data in the `players` dictionary in `mp_game_engine.py`. This is imported in `main.py` to *prevent* defining player and board data with the `global` keyword. The **players** and **AI** are both represented in the *same format* within this `players` dictionary to make **players** and **AI** *functionally equivalent*. The AI is essentially another instance of `player` with the *inputted vs generated* attack coordinates being the sole difference. This allows for easier future developments for player vs player games, implemented by making *both instances* of `player` use *inputted coordinates*. Multiple games can happen at the same time without interference on the same server, as each `player` (including AI) are given unique IDs stored in the `players` dictionary. To make it easier to create new placement and attack algorithms, both are defined using a *match case* statement. This means a developer can add new algorithms just by importing the function and adding a new `case`. Custom battleships can be defined as well, by editing `battleships.txt`. Custom error messages were implemented by providing verbose messages on why errors occurred in the *specific* context of the Battleship game (`algorithm_helpers.py`).

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

Author - Candidate 123166