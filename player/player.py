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
 
@app.route('/play/<int:player_id>', methods=['GET'])
def play(player_id):
    global min_number, max_number
    response=None    

    while(response!="won"):
        guess = random.randint(min_number, max_number)        
        game_start_response=requests.post(f"{game_master_url}/start_game/{player_id}", json={"guess": guess})
        
        if guess is None:
            return 'Bad request: Missing guess parameter', 400   
        
        if game_start_response.status_code == 200:
            game_result_response = requests.get(f'{game_master_url}/game_result/{player_id}')
            result = game_result_response.json()  
            response = result["result"]
            print(result)
            if response == 'lower':                
                max_number = guess - 1             
            elif response == "higher":                
                min_number = guess + 1        
                
            if(response!="won"):
                history.append(guess)
                guess = random.randint(min_number, max_number)              

            elif history[-1]!=result['target number']:                
                history.append(result['target number'])            
                          
            return jsonify(result, f"history:{history}"), 200        

        else:
            return 'Error communicating with Game Master server', 500
    

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)




