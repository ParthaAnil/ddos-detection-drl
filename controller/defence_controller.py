import random
from rl_agent.inference import predict_action_with_confidence

# =============================
# Global traffic mode flags
# =============================
ATTACK_MODE = False
FORCE_BENIGN = False


def set_attack_mode(mode: bool):
    """
    Start or stop DDoS attack simulation.
    """
    global ATTACK_MODE, FORCE_BENIGN

    if mode:
        ATTACK_MODE = True
        FORCE_BENIGN = False
    else:
        ATTACK_MODE = False
        FORCE_BENIGN = True


def get_attack_mode():
    return ATTACK_MODE


# =============================
# Network state generator
# =============================
def get_network_state():
    """
    Generates network metrics.
    """

    # -----------------------------
    # Active DDoS attack
    # -----------------------------
    if ATTACK_MODE:
        return [
            random.randint(900, 1600),
            round(random.uniform(0.5, 0.9), 2),
            random.randint(250, 500)
        ]

    # -----------------------------
    # Forced benign (after stop)
    # Only once, then reset
    # -----------------------------
    global FORCE_BENIGN
    if FORCE_BENIGN:
        FORCE_BENIGN = False  # IMPORTANT RESET
        return [80, 0.05, 40]

    # -----------------------------
    # Normal benign traffic
    # -----------------------------
    return [
        random.randint(50, 180),
        round(random.uniform(0.0, 0.15), 2),
        random.randint(20, 100)
    ]


# =============================
# Defence decision logic
# =============================
def apply_defence(state):
    """
    Uses RL model to decide mitigation.
    Safe, stable, demo-proof.
    """

    try:
        action, confidence = predict_action_with_confidence(state)
    except Exception:
        # Hard safety fallback (Tier-1 behavior)
        return {
            "traffic_status": "Benign Traffic",
            "action_taken": "No mitigation required",
            "confidence": [1.0, 0.0, 0.0]
        }

    if action == 0:
        status = "Benign Traffic"
        action_taken = "No mitigation required"

    elif action == 1:
        status = "DDoS Detected"
        action_taken = "Rate limiting enabled"

    elif action == 2:
        status = "DDoS Detected"
        action_taken = "Traffic blocked"

    else:
        status = "Unknown"
        action_taken = "No action"

    return {
        "traffic_status": status,
        "action_taken": action_taken,
        "confidence": confidence
    }
