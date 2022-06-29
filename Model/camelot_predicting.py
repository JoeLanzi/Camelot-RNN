import os
import sys 
sys.path.append("./Model") 
from Env.character_env import CharacterEnv
from stable_baselines3 import PPO

def load_model(step=1000):
    char_env = CharacterEnv(step)
    PPO_Path = os.path.join('Model', 'Training', 'Saved Models', 'CharacterModel')
    char_model = PPO.load(PPO_Path, env=char_env)

    return char_env, char_model

def predict_action(obs):
    step = 10
    env = CharacterEnv(step)
    PPO_Path = os.path.join('Model', 'Training', 'Saved Models', 'CharacterModel')
    model = PPO.load(PPO_Path, env=env)
    action,_ = model.predict(obs) #using model
    obs,reward,done,info = env.step(action)

    return action, obs, reward, done, info 

if __name__ == "__main__":
    predict_action()