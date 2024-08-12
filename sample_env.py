from environment import CarRaceEnv
from environment import RaceEnv
import gym
import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
import torch.optim as optim
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
class DQNAgent:
    def __init__(self, state_dim, action_dim, lr, gamma, epsilon, epsilon_decay, buffer_size):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.memory = deque(maxlen=buffer_size)
        self.model = DQN(state_dim, action_dim).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)

    def act(self, state):
        state = torch.tensor(state, dtype=torch.float32).to(device)
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_dim)
        q_values = self.model(state)
        return torch.argmax(q_values).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            state = torch.tensor(state, dtype=torch.float32).to(device)
            next_state = torch.tensor(next_state, dtype=torch.float32).to(device)
            target = reward
            if not done:
                target = reward + self.gamma * torch.max(self.model(next_state)).item()
            target_f = self.model(state).detach().cpu().numpy()
            target_f[action] = target
            target_f = torch.tensor(target_f, dtype=torch.float32).to(device)
            self.optimizer.zero_grad()
            loss = nn.MSELoss()(self.model(state), target_f)
            loss.backward()
            self.optimizer.step()
        if self.epsilon > 0.01:
            self.epsilon *= self.epsilon_decay

agent = DQNAgent(15, 4, lr=0.001, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, buffer_size=10000)
agent.model.load_state_dict(torch.load("model.pth"))

def main():
    # Create the environment
    env = CarRaceEnv()
    
    # Number of episodes to run
    num_episodes = 5
    
    for episode in range(num_episodes):
        # Reset the environment to start a new episode
        observation = env.reset()
        
        done = False
        total_reward = 0
        
        while not done:
            # Sample a random action from the action space
            #action = env.action_space.sample()
            action = agent.act(observation)
            # Step the environment with the sampled action
            observation, reward, done, info,_ = env.step(action)
            
            # Accumulate the total reward
            total_reward += reward
            
            # Render the environment
            env.render()
        
        print(f"Episode {episode + 1} finished with total reward: {total_reward}")
    
    # Close the environment
    env.close()



def main2():
    # Initialize the environment
    env = RaceEnv()
    
    # Reset the environment to the initial state
    observation = env.reset()

    # Sample actions (for demonstration purposes)
    actions = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]  # Rotate left, Rotate right, Move forward
    
    try:
        for action in actions:
            # Step through the environment with the sample action
            observation, reward, done, frame_iteration = env.step(action)
            
            # Render the environment
            env.render()
            
            # Print out the current state and reward for observation
            print(f"Action: {action}, Reward: {reward}, Done: {done}")
            
            # Pause for a short period to visualize the changes
           

            if done:
                print("Episode finished.")
                break

    finally:
        # Close the environment and Pygame
        env.close()


if __name__ == "__main__":
    main2()