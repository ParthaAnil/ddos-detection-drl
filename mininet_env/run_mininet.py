import subprocess

print("Starting Mininet topology...")

# Use DEFAULT Mininet controller (NO remote controller)
subprocess.run(
    ["sudo", "mn", "--topo", "single,2", "--test", "pingall"]
)

print("Mininet execution finished")

# ---- RL + Defence integration ----
from controller.defence_controller import apply_defence

def get_network_state():
    """
    Simulated network state
    """
    packet_rate = 250     # simulated attack traffic
    drop_rate = 0.35
    latency = 120
    return [packet_rate, drop_rate, latency]

state = get_network_state()
apply_defence(state)
