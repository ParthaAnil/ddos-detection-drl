import random
import numpy as np
from agent import DQNAgent
from environment import DDoSEnvironment

# -----------------------------
# Initialize environment & agent
# -----------------------------
env = DDoSEnvironment()
agent = DQNAgent(env.state_size, env.action_size)

EPISODES = 500          # Adjusted for CPU training
BATCH_SIZE = 32

print("🚀 Training started...")

for episode in range(EPISODES):

    # -----------------------------
    # Generate traffic (balanced)
    # -----------------------------
    if random.random() < 0.5:
        # Simulated DDoS attack traffic
        packet_rate = random.randint(900, 1500)
        drop_rate = random.uniform(0.5, 0.9)
        latency = random.randint(250, 500)
    else:
        # Normal traffic
        packet_rate = random.randint(50, 250)
        drop_rate = random.uniform(0.0, 0.3)
        latency = random.randint(20, 150)

    # -----------------------------
    # Environment state
    # -----------------------------
    state = env.get_state(packet_rate, drop_rate, latency)

    # Agent chooses action
    action = agent.act(state)

    # Reward from environment
    reward = env.get_reward(state, action)

    # Single-step environment
    next_state = state
    done = True

    # Store experience
    agent.remember(state, action, reward, next_state, done)

    # Train only if memory is sufficient
    if len(agent.memory) > BATCH_SIZE:
        agent.replay(BATCH_SIZE)

    # -----------------------------
    # Logging
    # -----------------------------
    if episode % 100 == 0:
        print(
            f"Episode {episode} | "
            f"PacketRate: {packet_rate} | "
            f"DropRate: {drop_rate:.2f} | "
            f"Latency: {latency} | "
            f"Action: {action} | "
            f"Reward: {reward} | "
            f"Epsilon: {agent.epsilon:.3f}"
        )

# -----------------------------
# Save trained model
# -----------------------------
agent.model.save("rl_agent/dqn_ddos_model.keras")
print("✅ Training complete. Model saved to rl_agent/dqn_ddos_model.keras")
