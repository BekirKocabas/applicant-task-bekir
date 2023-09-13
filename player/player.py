# import random
# from flask import Flask, jsonify

# app = Flask(__name__)

# # Configuration
# MIN_NUMBER = 1
# MAX_NUMBER = 1000

# # Generate a random target number for the game
# target_number = random.randint(MIN_NUMBER, MAX_NUMBER)

# @app.route('/health')
# def health():
#     return 'healthy player server', 200

# @app.route('/hostname')
# def hostname():
#     import socket
#     return socket.gethostname(), 200

# @app.route('/play')
# def play():
#     global MIN_NUMBER, MAX_NUMBER
#     guess = random.randint(MIN_NUMBER, MAX_NUMBER)
#     history = []

#     while guess != target_number:
#         if guess < target_number:
#             MIN_NUMBER = guess + 1
#         else:
#             MAX_NUMBER = guess - 1
#         history.append(guess)
#         guess = random.randint(MIN_NUMBER, MAX_NUMBER)

#     history.append(guess)

    

#     return jsonify({"result": f"true number is {history[-1]}: won", "history": history})


# if __name__ == '__main__':
#     #app.run(debug=True)
#     app.run(host='0.0.0.0', port=5001)
#     #app.run(host='0.0.0.0', port=80)


import random
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration for the range of numbers
min_number = 1
max_number = 1000
#player_id = 0

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
    response=None
    history = []  
    guess = random.randint(min_number, max_number)
    history.append(guess)
    while(response!="won"):        
        game_start_response=requests.post(f"{game_master_url}/start_game/{player_id}", json={"guess": guess})
        
        if guess is None:
            return 'Bad request: Missing guess parameter', 400   
        
        if game_start_response.status_code == 200:
            game_result_response = requests.get(f'{game_master_url}/game_result/{player_id}')
            result = game_result_response.json()
            response = result["result"]
            if response == 'lower':
                #global max_number
                max_number = history[-1]
            elif response == "higher":
                #global min_number
                min_number = history[-1]
            guess = random.randint(min_number, max_number)
            history.append(guess)
            return jsonify(history[-1], result), 200
        else:
            return 'Error communicating with Game Master server', 500
    result = game_result_response.json()
    return jsonify(history[-1], result), 200

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
    #app.run(host='0.0.0.0', port=80)

