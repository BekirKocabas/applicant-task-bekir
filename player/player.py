import random
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration for the range of numbers
min_number = 1
max_number = 1000
history = [] 

# Game Master server URL
game_master_url = "http://master:5001"

@app.route('/health', methods=['GET'])
def health_check():
    return 'healthy', 200

@app.route('/hostname', methods=['GET'])
def hostname():
    import socket
    return socket.gethostname(), 200

# Endpoint for playing the number guessing game
@app.route('/play/<int:player_id>', methods=['GET'])
def play(player_id):
    global min_number, max_number
    guess = random.randint(min_number, max_number) # # Generate a random guess within the range
    # Start a new game by sending a POST request to a Game Master server with the player's guess            
    game_start_response=requests.post(f"{game_master_url}/start_game/{player_id}", json={"guess": guess})
    # Retrieve the game result by sending a GET request to the Game Master server
    game_result_response = requests.get(f'{game_master_url}/game_result/{player_id}')
    result = game_result_response.json() 
    response = result["result"]    # Extract the game result from the response JSON
    history.append(guess)     # Add the guess to a history list
    
    # Check for missing guess parameter and handle bad requests 
    if guess is None:
        return 'Bad request: Missing guess parameter', 400
    # If the game was successfully started, update the range based on the response  
    if game_start_response.status_code == 200:
        if response == 'lower':                
            max_number = guess - 1   # Adjust the maximum number down          
        elif response == "higher":                
            min_number = guess + 1   # Adjust the minimum number up     
        elif response == "won":                
            min_number = guess
            max_number = guess            
                                
        return jsonify(result, f"history:{history}"), 200   # Return the game result and history as JSON response                

    else:
        return 'Error communicating with Game Master server', 500 # Handle server communication error
 
# Endpoint to reset the game for a player   
@app.route('/reset_play/<int:player_id>', methods=['GET'])
def reset_play(player_id):
    global history, response, max_number, min_number

    history = []  # Clear the game history
    response = None  # Reset the response
    max_number = 10  # Reset the maximum number to its initial value
    min_number = 1   # Reset the minimum number to its initial value   
    target_request = requests.get(f'{game_master_url}/reset_target/{player_id}') #Send a request to the Game Master server to request a new target
    
    if target_request.status_code == 200:
        return f'Reset game. New target requested from Game Master.', 200
    else:
        return 'Error communicating with Game Master server', 500


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)