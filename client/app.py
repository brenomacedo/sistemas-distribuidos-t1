from flask import Flask, request, jsonify, redirect
from threading import Thread
from flask_cors import CORS
from models import message_pb2
import socket

GATEWAY_PORT = 5008
GATEWAY_IP = "localhost"
TCP_LISTEN_IP = "0.0.0.0"
TCP_LISTEN_PORT = 5001

app = Flask(__name__)

CORS(app)

DEVICES_MAP = {
  "AIR_CONDITIONING",
  "ABAJOUR",
  "ARTIFICIAL_LIGHT",
  "ABAJUR",
  "SOUND_BOX",
  "TELEVISION",
  "DOOR",
}

ac_status = {"isOn": False, "temperature": 25, "error": False}
music_status = {"isOn": False, "musicPath": "public/music/lofi.mp3", "error": False}
sensor_temperature_status = {"temperature": 25}

devices = []


def send_message(message: bytes):
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((GATEWAY_IP, GATEWAY_PORT))

  client_socket.sendall(message)
  client_socket.close()


def listen_messages():
  server_socket = socket.socket(
    socket.AF_INET,  # familia de ips ipv4
    socket.SOCK_STREAM,  # socket orientado a conexão (TCP)
  )
  server_socket.bind((TCP_LISTEN_IP, TCP_LISTEN_PORT))
  server_socket.listen(10)

  try:
    while True:
      client_socket, _ = server_socket.accept()

      data = client_socket.recv(1024)
      if data:
        message = message_pb2.Message()
        message.ParseFromString(data)
        if message.type == message_pb2.REGISTER_DEVICE:
          new_device = {"id": message.params[0], "type": DEVICES_MAP[message.params[1]]}
          devices.append(new_device)
          print(f"Novo dispositivo do tipo {new_device['type']} conectado")
        elif message.type == message_pb2.TEMPERATURE_INFO:
          sensor_temperature_status["temperature"] = message.params[0]
          print(
            f"Nova temperatura detectada pelo sensor: {sensor_temperature_status['temperature']}"
          )
  except Exception:
    pass


Thread(target=listen_messages).start()


@app.route("/api/ac-status", methods=["GET"])
def get_ac_status():
  return jsonify(ac_status)


@app.route("/api/ac-increase", methods=["GET"])
def increase_temperature():
  if ac_status["isOn"]:
    ac_status["temperature"] += 1
  return jsonify(ac_status)


@app.route("/api/ac-decrease", methods=["GET"])
def decrease_temperature():
  if ac_status["isOn"]:
    ac_status["temperature"] -= 1
  return jsonify(ac_status)


@app.route("/api/ac-toggle", methods=["GET"])
def toggle():
  ac_status["isOn"] = not ac_status["isOn"]
  return jsonify(ac_status)


@app.route("/api/sensor-temperature", methods=["GET"])
def sensor_temperature():
  return jsonify(
    {"temperature": sensor_temperature_status["temperature"], "error": False}
  )


@app.route("/api/change-color", methods=["POST"])
def change_color():
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
    color = data.get("color")

    if not color:
      return jsonify({"error": "No color parameter provided"}), 400

    return jsonify({"color": colors[color]}), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route("/api/music-status", methods=["GET"])
def get_music_status():
  return jsonify(music_status)


@app.route("/api/toggle-music", methods=["GET"])
def toggle_music():
  music_status["isOn"] = not music_status["isOn"]
  return jsonify(music_status)


@app.route("/api/select-music", methods=["POST"])
def change_music():
  music_status["isOn"] = True
  musics = {
    "jazz": "public/music/jazz.mp3",
    "lofi": "public/music/lofi.mp3",
    "mozart": "public/music/mozart.mp3",
  }
  try:
    data = request.get_json()
    music = data.get("music")

    if not music:
      return jsonify({"error": "No music parameter provided"}), 400

    return jsonify({"music": musics[music]}), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route("/")
def front_end():
  return redirect("/static/index.html", code=302)


if __name__ == "__main__":
  app.run(debug=True)
