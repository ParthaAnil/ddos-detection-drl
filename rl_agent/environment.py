import numpy as np


class DDoSEnvironment:
    def __init__(self):
        # State = [packet_rate, drop_rate, latency]
        self.state_size = 3

        # Actions:
        # 0 -> Allow Traffic
        # 1 -> Rate Limit
        # 2 -> Block Traffic
        self.action_size = 3

    def get_state(self, packet_rate, drop_rate, latency):
        """
        Returns current network state as numpy array
        """
        return np.array([packet_rate, drop_rate, latency])

    def get_reward(self, state, action):
        """
        Reward function for RL training
        """
        packet_rate, drop_rate, latency = state

        # ----------------------------
        # Normal / Benign Traffic
        # ----------------------------
        if packet_rate < 300 and drop_rate < 0.3:
            if action == 0:      # Allow
                return +10
            elif action == 1:    # Rate limit
                return -2
            else:                # Block
                return -10

        # ----------------------------
        # Suspicious Traffic
        # ----------------------------
        elif packet_rate < 800:
            if action == 1:      # Rate limit
                return +8
            elif action == 0:    # Allow
                return -5
            else:                # Block
                return -2

        # ----------------------------
        # DDoS Attack Traffic
        # ----------------------------
        else:
            if action == 2:      # Block
                return +15
            elif action == 1:    # Rate limit
                return +5
            else:                # Allow
                return -20
