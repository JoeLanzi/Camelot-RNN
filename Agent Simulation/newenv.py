#%% 1. Imports 
# open gym ai
from concurrent.futures import thread
from gym import Env,spaces

# helper
import numpy as np
import os
from statistics import mean
from reward import happiness
from visual import plot
import time
from threading import Thread, Timer

# baselines
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv

# market class
from supply import Market

# npc classes
from npc import *
#%% 2. Environment Class 
""" 
    This is simulated environment that will be integrated with Camelot
    Consists of actions,states,rewards
    Also logic for actions and NPC stats
"""

class CamelotEnv(Env):
    def __init__(self,max_training_length=10000,npc=NPC()):
        self.action_space = spaces.Discrete(9) #9 actions
        self.observation_space = spaces.Box(np.array([0,0,0,0]),np.array([100,100,100,100]))

        self.NPCs = npc
        self.state = npc.return_state()

        self.max_training_length = max_training_length
        self.training_length = max_training_length


    def step(self, action):
        
        npc = self.NPCs
        npc.actions(action)

        '''environment logic'''
        # reduce health, hunger, and energy
        npc.hunger -= 2 if npc.hunger > 0 else npc.hunger
        npc.energy -= 1 if npc.energy > 0 else npc.energy
        if npc.hunger <= 0 or npc.energy <= 0:
            npc.health -= 5

        if npc.hunger >= 100:
            npc.hunger = 100
        if npc.hunger <= 0:
            npc.hunger = 0
        if npc.energy >= 100:
            npc.energy = 100
        if npc.energy <= 0:
            npc.energy = 0
        if npc.health >= 100:
            npc.health = 100
        if npc.health <= 0:
            npc.health = 0

        ''''Record History'''
        self.state = npc.return_state()
        for i in range(len(npc.stat_record)):
            npc.stat_record[i].append(npc.return_state()[i])


        '''step conditions'''
        # Reduce training step by 1 per step
        self.training_length -= 1 
        
        # Reward per step.
        reward = 0.5 + happiness(list(npc.return_state()))
        
        # Check if training_length is done or if NPC health is done
        done = True if self.training_length <= 0 or npc.health <= 0 else False 
        
        # Set placeholder for info
        info = {}

        # Return step information
        return self.state, reward, done, info
    
    def render(self):
        # Implement viz in camelot
        plot(self.NPCs.stat_record)
        #pass

    def reset(self):
        self.NPCs.reset()
        self.training_length = self.max_training_length
        return self.NPCs.return_state()
# %% testing the environment
env = CamelotEnv(1000,Guards())
mean_score = []

episodes = 1
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0 
    
    while not done:
        #env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    env.render()
    print('Episode:{} Score:{:.2f}'.format(episode, score))
    mean_score.append(score)
#env.close()

print('Total Episodes:{} Average Score:{:.2f}'.format(episode, mean(mean_score))) #get mean scores


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
                            eval_freq=1000,
                            best_model_save_path=save_path, 
                            verbose=1)

#make multi env 
#from stable_baselines3.common.vec_env import VecFrameStack
env = DummyVecEnv([lambda:CamelotEnv(1000,Guards(wage=500))])
#env = VecFrameStack(env,4)


log_path = os.path.join('Training', 'Logs')
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_path)
model.learn(total_timesteps=100000,callback=eval_callback) #callback=eval_callback


"""
PPO overfits in a single environment
requires multiple parallel environments to prevent overfitting
As PPO is an on-policy algorithm it requires multiple parallel environments in 
order to break the correlation between the samples = prevent over fitting.
"""

# %% Save or Load
"""load best model model at path"""
model = PPO.load(os.path.join(save_path,'best_model'),env=env) 

"""save model at path"""
PPO_Path = os.path.join('Training','Saved Models','Guards_PPO_100k')
model.save(PPO_Path) 

#%% Evaluate
evaluate_policy(model,env,n_eval_episodes=5,render=False)
# tensorboard --logdir Training/Logs

# %%%%% Deploy Model in the environment %%%%% #
###############################################
"""
    Simulation Phase
    Uses trained models in the environment 
"""
n = 1000
env = CamelotEnv(n,Guards(wage=2000))
#env = VecFrameStack(env,4)

from tqdm import tqdm
#del model # delete model
PPO_Path = os.path.join('Training','Saved Models','Guards_PPO_100k')
model = PPO.load(PPO_Path,env=env) # load model at path



mean_score = []
episodes = 1000
pbar = tqdm(total=n) if episodes == 1 else None # progress bar

for episode in range(1,episodes+1):
    obs = env.reset() # observation
    done = False
    score = 0
    
    while not done:
        #env.render() #render live
        action,_ = model.predict(obs) #using model
        obs,reward,done,info = env.step(action)
        score += reward
        pbar.update(1) if episodes == 1 else None
    print(f'Episode:{episode} Score:{score}')
    mean_score.append(score)
    #env.render() #render per episode
#env.close()
pbar.close() if episodes == 1 else None

print('Total Episodes:{} Average Score:{}'.format(episode, mean(mean_score))) if episode > 1 else None
# %% Plot Mean Scores
import matplotlib.pyplot as plt
plt.hist(mean_score,bins=30,facecolor='#2ab0ff', edgecolor='#169acf', linewidth=1)
plt.title('Guard Scores') 
plt.xlabel('Score') 
plt.ylabel('Count') 
plt.show()

# %%
