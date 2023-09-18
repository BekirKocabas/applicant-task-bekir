import random
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration for the range of numbers
min_number = 1
max_number = 10
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
 
@app.route('/play/<int:player_id>', methods=['GET'])
def play(player_id):
    global min_number, max_number
    guess = random.randint(min_number, max_number)            
    game_start_response=requests.post(f"{game_master_url}/start_game/{player_id}", json={"guess": guess})
    game_result_response = requests.get(f'{game_master_url}/game_result/{player_id}')
    result = game_result_response.json()
    response = result["result"]   
    history.append(guess)     
     
    if guess is None:
        return 'Bad request: Missing guess parameter', 400   
    if game_start_response.status_code == 200:
        if response == 'lower':                
            max_number = guess - 1             
        elif response == "higher":                
            min_number = guess + 1        
        elif response == "won":                
            min_number = guess
            max_number = guess            
                                
        return jsonify(result, f"history:{history}"), 200                   

    else:
        return 'Error communicating with Game Master server', 500
 
    
@app.route('/reset_play/<int:player_id>', methods=['GET'])
def reset_play(player_id):
    global history, response, max_number, min_number

    history = []  # Clear the game history
    response = None  # Reset the response
    max_number = 10  # Reset the maximum number to its initial value
    min_number = 1   # Reset the minimum number to its initial value   
    target_request = requests.get(f'{game_master_url}/reset_target/{player_id}') #Send a request to the Game Master server to request a new target
    
    if target_request.status_code == 200:
        return f'Game reset for Player {player_id}. New target requested from Game Master.', 200
    else:
        return 'Error communicating with Game Master server', 500


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)