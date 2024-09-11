from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import logging

# Initialiser Flask og SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Opprett en logger
logging.basicConfig(level=logging.INFO)

# Lagring av iSpindel-data
ispindel_data = {}

# Håndtere POST-forespørsler til /data
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    logging.info(f"Data received: {data}")
    
    # Hent iSpindel ID fra data
    ispindel_id = data.get('ID')
    if ispindel_id:
        ispindel_data[ispindel_id] = data
        logging.info(f"iSpindel ID: {ispindel_id}")
        
        # Send data til nettsiden via WebSocket
        socketio.emit('update_data', ispindel_data)
        return jsonify({"status": "success"}), 200
    else:
        logging.warning("iSpindel ID not found in the data!")
        return jsonify({"status": "error", "message": "iSpindel ID not found"}), 400

# Ny rute for /api/ispindel-data
@app.route('/api/ispindel-data', methods=['POST'])
def ispindel_data_endpoint():
    data = request.json
    logging.info(f"Data received on /api/ispindel-data: {data}")
    
    # Legg til dataene i ispindel_data og send det til nettsiden
    ispindel_id = data.get('ID')
    if ispindel_id:
        ispindel_data[ispindel_id] = data
        socketio.emit('update_data', ispindel_data)
    
    return jsonify({"status": "success"}), 200

# Ny rute for /api/post_data
@app.route('/api/post_data', methods=['POST'])
def post_data_endpoint():
    data = request.json
    logging.info(f"Data received on /api/post_data: {data}")
    
    # Legg til dataene i ispindel_data og send det til nettsiden
    ispindel_id = data.get('ID')
    if ispindel_id:
        ispindel_data[ispindel_id] = data
        socketio.emit('update_data', ispindel_data)
    
    return jsonify({"status": "success"}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)