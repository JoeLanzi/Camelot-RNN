#%% 1. Imports 
# open gym ai
from gym import Env,spaces

# helper
import numpy as np
import os
from statistics import mean

# baselines
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

#%% 2. Environment Class 
""" 
    This is simulated environment that will be integrated with Camelot
    Consists of actions,states,rewards
    Also logic for actions and NPC stats
"""
class CamelotEnv(Env):
    def __init__(self,max_training_length=10000):
        self.action_space = spaces.Discrete(5) #5 actions
        self.observation_space = spaces.Box(np.array([0,0,0,0]),np.array([100,100,100,1]))

        self.health = 100
        self.hunger = 100
        self.energy = 100
        self.location = 0     # 0 at camp, 1 at plant
        self.state = (self.health, self.hunger, self.energy,self.location) # initial state

        self.max_training_length = max_training_length
        self.training_length = max_training_length


    def get_action_meanings(self):
        return {0: "Go to food", 1: "Eat food", 2: "Go to camp", 3: "Sleep", 4: "Do Nothing"}

    def step(self, action):
        
        '''actions'''
        if action == 0:      # go to plant & get food        
            self.location = 1 
        elif action == 1:    # eat food
            if self.location == 1:
                self.hunger += 35
        elif action == 2:    # go to bed
            self.location = 0 
        elif action == 3:    # sleep
            if self.location == 0:
                self.energy +=35
        elif action == 4:    # do nothing
            pass
            
        self.state = (self.health, self.hunger, self.energy,self.location)
        
        '''stat logic'''
        # reduce health, hunger, and energy
        self.hunger -= 5 if self.hunger > 0 else self.hunger
        self.energy -= 3 if self.energy > 0 else self.energy
        if self.hunger <= 0 or self.energy <= 0:
            self.health -= 10

        '''step conditions'''
        # Reduce training step by 1 per step
        self.training_length -= 1 
        
        # Reward for executing a step.
        reward = 1
        
        # Check if training_length is done or if NPC health is done
        done = True if self.training_length <= 0 or self.health <= 0 else False 
        
        # Set placeholder for info
        info = {}
        
        # Return step information
        return self.state, reward, done, info
    
    def render(self):
        # Implement viz in camelot
        pass

    def reset(self):
        # Reset NPC State
        self.health = 100
        self.hunger = 100
        self.energy = 100
        self.location = 0
        # Reset training step
        self.training_length = self.max_training_length
        return self.state
# %% testing the environment
env = CamelotEnv(1000000)
mean_score = []

episodes = 10
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0 
    
    while not done:
        env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score+=reward
    print('Episode:{} Score:{}'.format(episode, score))
    mean_score.append(score)
env.close()

#print('Total Episodes:{} Average Score:{}'.format(episode, mean(mean_score))) #get mean scores


#env.observation_space.sample()
#env.action_space.sample()

# %% Train Model using agent/ppo model
"""
    Agent using PPO - multilayer perceptron policy model
"""
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold

save_path = os.path.join('Training','Saved Models')

stop_callback = StopTrainingOnRewardThreshold(reward_threshold=10000,verbose=1)
eval_callback = EvalCallback(env,
                            callback_on_new_best=stop_callback,
                            eval_freq=10000,
                            best_model_save_path=save_path, 
                            verbose=1)

log_path = os.path.join('Training', 'Logs')
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_path)
model.learn(total_timesteps=100000)


# %% Evaluate
#model = PPO.load(os.path.join(save_path,'best_model'),env=env) # load model at path
#PPO_Path = os.path.join('Training','Saved Models','CamelotModel_3')
#model.save(PPO_Path) # save model at path

env = CamelotEnv()
evaluate_policy(model,env,n_eval_episodes=10,render=False)
# %% Deploy Model in the environment
"""
    Simulation Phase
    Uses trained models in the environment 
"""
from tqdm import tqdm
#del model # delete model
PPO_Path = os.path.join('Training','Saved Models','CamelotModel_3')

env = CamelotEnv(1000000)
model = PPO.load(PPO_Path,env=env) # load model at path

mean_score = []
episodes = 1
pbar = tqdm(total=1000000) # progress bar

for episode in range(1,episodes+1):
    obs = env.reset() # observation
    done = False
    score = 0
    
    while not done:
        env.render() 
        action,_ = model.predict(obs) #using model
        obs,reward,done,info = env.step(action)
        score += reward
        pbar.update(1)
    #print(f'Episode:{episode} Score:{score}')
    mean_score.append(score)
env.close()
pbar.close()

print('Total Episodes:{} Average Score:{}'.format(episode, mean(mean_score)))
# %% Plot Mean Scores
import matplotlib.pyplot as plt
plt.hist(mean_score)