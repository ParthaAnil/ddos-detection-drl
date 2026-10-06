import numpy as np
from tensorflow.keras.models import load_model

model = load_model("rl_agent/dqn_ddos_model.keras", compile=False)

def predict_action_with_confidence(state):
    state = np.array(state, dtype=np.float32).reshape(1, -1)

    q_values = model.predict(state, verbose=0)[0]

    # Stable softmax
    exp_q = np.exp(q_values - np.max(q_values))
    confidence = (exp_q / np.sum(exp_q)).tolist()

    # Guarantee exactly 3 values
    while len(confidence) < 3:
        confidence.append(0.0)

    action = int(np.argmax(q_values))
    return action, confidence
