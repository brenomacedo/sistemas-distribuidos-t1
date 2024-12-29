from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

ac_status = {
    'isOn': True,
    'temperature': 25
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

if __name__ == '__main__':
    app.run(debug=True)
