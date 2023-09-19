import random
import threading
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Configuration for the range of numbers
min_number = 1
max_number = 1000
game_sessions = {} # Dictionary to store game sessions for each player
player_locks = {}  # Dictionary to store locks for each player
  
target_number = random.randint(min_number, max_number)

# Define a function to play the game
def play_game(player_id, player_guess):  
    result = ""
    response = {}

    if player_guess < target_number:
        result = 'higher'        # The player needs to guess a higher number
    elif player_guess > target_number:
        result = 'lower'    # The player needs to guess a lower number
    else:
        result = 'won'     # The player guessed the correct number  

    response = {
            'result': result,
            'target number' : target_number
        }

    # Store the game session result for the player
    game_sessions[player_id] = response 

    # Release the lock when the game session is complete
    player_locks[player_id].release()

# Define an endpoint to start a new game session for a player
@app.route('/start_game/<int:player_id>', methods=['POST'])
def start_game(player_id):
    if player_id in game_sessions:
        # Wait for the previous game session to finish
        player_locks[player_id].acquire()

    # Start a new game session for the player
    data = request.get_json()
    guess = data.get('guess')
    game_thread = threading.Thread(target=play_game, args=(player_id, guess))
    game_thread.start()

    return f'Started game session for Player {player_id}', 200

# Define an endpoint to get the game result for a player
@app.route('/game_result/<int:player_id>', methods=['GET'])
def get_game_result(player_id):
    if player_id not in game_sessions:
        return 'Player does not have an active game session', 404

    result = game_sessions[player_id]
    return jsonify(result), 200

# Define an endpoint to reset the target number for a player
@app.route('/reset_target/<int:player_id>', methods=['GET'])
def reset_target(player_id):
    global target_number
    
    # Setting a new target    
    target_number = random.randint(min_number, max_number)

    return f'New target set for Player {player_id}', 200

if __name__ == '__main__':
    # Initialize locks for players
    for player_id in range(1, 1001):
        player_locks[player_id] = threading.Lock()
        
    # Start the Flask web application
    app.run(host='0.0.0.0', port=5001)