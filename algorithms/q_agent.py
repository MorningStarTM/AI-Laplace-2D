import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import math
import random
import numpy as np
from collections import deque
import os

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
        self.target_model = DQN(state_dim, action_dim).to(device)  # Target network
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.target_model.load_state_dict(self.model.state_dict())  # Initialize target network
        self.target_update_freq = 1000  # Frequency of updating target network
        self.steps_done = 0

    def act(self, state):
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)  # Add batch dimension
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_dim)
        with torch.no_grad():
            q_values = self.model(state)
        return torch.argmax(q_values).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*minibatch)
        states = torch.tensor(states, dtype=torch.float32).to(device)
        actions = torch.tensor(actions, dtype=torch.long).to(device)
        rewards = torch.tensor(rewards, dtype=torch.float32).to(device)
        next_states = torch.tensor(next_states, dtype=torch.float32).to(device)
        dones = torch.tensor(dones, dtype=torch.float32).to(device)

        q_values = self.model(states)
        next_q_values = self.target_model(next_states).detach()
        q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
        target = rewards + self.gamma * next_q_values.max(1)[0] * (1 - dones)

        loss = nn.MSELoss()(q_value, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.steps_done % self.target_update_freq == 0:
            self.target_model.load_state_dict(self.model.state_dict())  # Update target network

        if self.epsilon > 0.01:
            self.epsilon *= self.epsilon_decay

        self.steps_done += 1


    def save_model(self, path:str):
        torch.save(self.model.state_dict(), os.path.join("models", path))

    def load_model(self, path:str):
        self.model.load_state_dict(torch.load(os.path.join("models", path)))