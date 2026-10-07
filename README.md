# Real-Time DDoS Detection and Mitigation using Deep Reinforcement Learning

A Deep Q-Network (DQN) agent that watches network traffic metrics and decides, in real time, whether to **allow**, **rate-limit** or **block** traffic. It is set in a Software-Defined Networking (SDN) environment simulated with Mininet and comes with a live Flask dashboard.

## How it works

```
Network metrics ──► DQN agent ──► Defence action ──► Flask dashboard
(packet rate,        (TensorFlow/    (allow / rate-limit /   (live status +
 drop rate,           Keras)          block)                 confidence)
 latency)
```

| Part | Details |
|---|---|
| **State** | `[packet_rate, drop_rate, latency]` |
| **Actions** | `0` Allow · `1` Rate-limit · `2` Block |
| **Reward** | Rewards allowing normal traffic, rate-limiting suspicious traffic and blocking attack traffic; penalises wrong decisions (e.g. −20 for allowing an attack, −10 for blocking normal traffic) |
| **Model** | Dense 24 → 24 → 3 (ReLU, linear output), Adam (lr 0.001), MSE loss |
| **Training** | 500 episodes, experience replay (memory 2000, batch 32), γ = 0.95, ε-greedy with decay 0.995 |

## Results

| Metric | Score |
|---|---|
| Accuracy | 93% |
| Precision | 92.16% |
| Recall | 94% |
| F1-score | 93.07% |

## Project structure

```
ddos-detection-drl/
├── rl_agent/
│   ├── agent.py              # DQN agent (model, ε-greedy policy, experience replay)
│   ├── environment.py        # State definition and reward function
│   ├── train.py              # Training loop
│   ├── inference.py          # Loads the trained model, returns action + confidence
│   └── dqn_ddos_model.keras  # Trained model
├── controller/
│   └── defence_controller.py # Network state + mitigation decision logic
├── mininet_env/
│   ├── topo.py               # SDN topology: server h1, host h2, switch s1
│   └── run_mininet.py        # Starts the Mininet topology (Linux only)
├── web/
│   ├── app.py                # Flask dashboard + REST API
│   └── templates/index.html
└── requirements.txt
```

## Getting started

Run every command from the **project root** (the folder containing `rl_agent/`), because the model is loaded by a relative path.

```bash
# 1. Clone
git clone https://github.com/ParthaAnil/ddos-detection-drl.git
cd ddos-detection-drl

# 2. Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. (Optional) Retrain the agent — overwrites rl_agent/dqn_ddos_model.keras
python rl_agent/train.py

# 4. Start the dashboard
python web/app.py
```

Then open **http://127.0.0.1:5000**.

### REST API

| Endpoint | Returns |
|---|---|
| `GET /` | Dashboard page |
| `GET /status` | Current metrics, traffic status, action taken and model confidence (JSON) |
| `GET /attack/start` | Switches the simulated metrics to high-load conditions, to test the agent's response |
| `GET /attack/stop` | Returns the simulated metrics to normal |

### Mininet (optional, Linux only)

The SDN topology needs Mininet installed on Linux (it was developed in a Linux VM) and root access:

```bash
sudo python mininet_env/run_mininet.py
```

## Tech stack

Python · TensorFlow / Keras · NumPy · Flask · Mininet (SDN)

## Paper

*Real-Time DDoS Attack Detection and Mitigation Using Deep Reinforcement Learning* (IEEE conference paper draft).
