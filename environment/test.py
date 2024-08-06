import gym
from GymEnv import CarRaceEnv

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
            action = env.action_space.sample()
            
            # Step the environment with the sampled action
            observation, reward, done, info = env.step(action)
            print(observation)
            # Accumulate the total reward
            total_reward += reward
            
            # Render the environment
            env.render()
        
        print(f"Episode {episode + 1} finished with total reward: {total_reward}")
    
    # Close the environment
    env.close()

if __name__ == "__main__":
    main()
