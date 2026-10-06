import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, jsonify
from controller.defence_controller import (
    get_network_state,
    apply_defence,
    set_attack_mode
)

app = Flask(__name__)


# =============================
# UI Route
# =============================
@app.route("/")
def index():
    return render_template("index.html")


# =============================
# Status API (used by dashboard)
# =============================
@app.route("/status")
def status():
    state = get_network_state()
    decision = apply_defence(state)

    print("CONFIDENCE:", decision["confidence"])  # DEBUG LINE

    return jsonify({
        "packet_rate": state[0],
        "drop_rate": state[1],
        "latency": state[2],
        "traffic_status": decision["traffic_status"],
        "action_taken": decision["action_taken"],
        "confidence": decision["confidence"]
    })



# =============================
# Attack control endpoints
# =============================
@app.route("/attack/start")
def start_attack():
    set_attack_mode(True)
    return jsonify({"attack_mode": "on"})


@app.route("/attack/stop")
def stop_attack():
    set_attack_mode(False)
    return jsonify({"attack_mode": "off"})


# =============================
# App runner
# =============================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
