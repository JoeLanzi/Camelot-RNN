#%% Imports
import os
import pandas as pd
import os
import sys
import time
sys.path.append("..") 
# from Helper.csv_handler import store_action_csv, clear_observation_csv
from Env.character_env import CharacterEnv
from stable_baselines3 import PPO

#%% load model
step = 5
env = CharacterEnv(step)
PPO_Path = os.path.join('Model', 'Training', 'Saved Models', 'CharacterModel')
model = PPO.load(PPO_Path, env=env)

obs = env.reset() # observation (health, hunger, energy)
done = False
score = 0
start_predict = True

# initialize state.csv
state_history = pd.DataFrame([[0, 100, 100, -1]], columns = ["hunger", "energy", "health", "action"])
#%%
try:
    while not done:
        predict_flag = pd.read_csv('csv/predict_flag.csv').iloc[0][0]
        if predict_flag == True:
            obs = tuple(pd.read_csv('csv/state.csv').iloc[-1])[0:3]
            action,_ = model.predict(obs) #using model
            obs,reward,done,info = env.step(action)

            # update observation.csv
            obs_series = pd.DataFrame([obs+ (action,)], columns=["hunger", "energy", "health", "action"])
            obs_series.to_csv('csv/observation.csv', index=False)

            # update state.csv
            obs_action_series = pd.DataFrame([obs + tuple([action])], columns = ["hunger", "energy", "health", "action"])
            state_history = pd.concat([state_history, obs_action_series])
            state_history.reset_index(inplace=True, drop=True)
            state_history.to_csv('csv/state.csv', index=False)

            # update predict_flag.csv
            predict_flag = pd.DataFrame({'Flag':[False]})
            predict_flag.to_csv('csv/predict_flag.csv', index=False)
        
        time.sleep(0.5) # for avoiding csv i/o error
except KeyboardInterrupt:
    print('interrupted!')

env.close()

# %%
