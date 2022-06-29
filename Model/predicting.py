#%% Imports
from cProfile import label
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statistics import mean
from Env.character_env import CharacterEnv
from tqdm import tqdm
from stable_baselines3 import PPO

#%% load model
step = 5
env = CharacterEnv(step)
PPO_Path = os.path.join('Training', 'Saved Models', 'CharacterModel')
model = PPO.load(PPO_Path, env=env)
mean_score = []
episodes = 1
pbar = tqdm(total=step * episodes) # progress bar

for episode in range(1,episodes+1):
    obs = env.reset() # observation
    done = False
    score = 0
    actions = []
    hunger = []
    energy = []
    health = []
    
    while not done:
        env.render()
        action,_ = model.predict(obs) #using model
        obs,reward,done,info = env.step(action)
        score += reward
        pbar.update(1)
        hunger.append(obs[0])
        energy.append(obs[1])
        health.append(obs[2])
        actions.append(action)
    print(f'Episode:{episode} Score:{score}')
    mean_score.append(score)
env.close()
pbar.close()

plt.figure()
plt.subplot(2,2,1)
x = np.arange(0, step, 1)
plt.plot(x, hunger, label='hunger')
plt.plot(x, energy, label='energy')
plt.plot(x, health, label='health')
plt.legend()

plt.subplot(2,2,2)
ax = pd.Series(actions).value_counts().plot(kind='bar', rot=0)

plt.show()
print('Total Episodes:{} Average Score:{}'.format(episode, mean(mean_score)))
# %% Plot Mean Scores
import matplotlib.pyplot as plt
plt.hist(mean_score)
