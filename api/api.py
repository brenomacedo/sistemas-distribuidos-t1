from flask import Flask, request, jsonify
from flask_cors import CORS

import random

app = Flask(__name__)

CORS(app)

ac_status = {
    'isOn': False,
    'temperature': 25,
    'error': False
}

music_status = {
    'isOn': False,
    'musicPath': 'public/music/lofi.mp3',
    'error': False
}

@app.route('/api/ac-status', methods=['GET'])
def get_ac_status():
    return jsonify(ac_status)

@app.route('/api/ac-increase', methods=['GET'])
def increase_temperature():
    if ac_status['isOn']:
        ac_status['temperature'] += 1
    return jsonify(ac_status)

@app.route('/api/ac-decrease', methods=['GET'])
def decrease_temperature():
    if ac_status['isOn']:
        ac_status['temperature'] -= 1
    return jsonify(ac_status)

@app.route('/api/ac-toggle', methods=['GET'])
def toggle():
    ac_status['isOn'] = not ac_status['isOn']
    return jsonify(ac_status)

@app.route('/api/sensor-temperature', methods=['GET'])
def sensor_temperature():
    return jsonify({
        "temperature": random.randint(20, 30),
        "error": False
    })

@app.route('/api/change-color', methods=['POST'])
def change_color():
    # FAZER ISSO AQUI NO GATEWAY/DISPOSITIVO
    colors = {
        "light-purple": "0x7d3ac1",
        "light-blue": "0x1e90ff",
        "light-pink": "0xff69b4",
        "light-green": "0x39ff14",
        "light-red": "0xff4500",
        "light-yellow": "0xffd700",
    }
    try:
        data = request.get_json()  
        color = data.get('color')  

        if not color:
            return jsonify({"error": "No color parameter provided"}), 400
        
        return jsonify({
            "color": colors[color] 
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/music-status', methods=['GET'])
def get_music_status():
    return jsonify(music_status)

@app.route('/api/toggle-music', methods=['GET'])
def toggle_music():
    music_status['isOn'] = not music_status['isOn']
    return jsonify(music_status)

@app.route('/api/select-music', methods=['POST'])
def change_music():
    music_status['isOn'] = True

    # FAZER ISSO AQUI NO GATEWAY/DISPOSITIVO
    musics = {
        "jazz": "public/music/jazz.mp3",
        "lofi": "public/music/lofi.mp3",
        "mozart": "public/music/mozart.mp3",
    }
    try:
        data = request.get_json()  
        music = data.get('music')  

        if not music:
            return jsonify({"error": "No music parameter provided"}), 400
        
        return jsonify({
            "music": musics[music] 
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
