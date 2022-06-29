# %% Import models
import os
from Env.character_env import CharacterEnv
from npc import *
from stable_baselines3 import PPO
from statistics import mean

# %%%%% Deploy Model in the environment %%%%% #
###############################################
"""
    Simulation Phase
    Uses trained models in the environment 
"""
n = 10
env = CharacterEnv(n,Guards(wage=100))
env2 = CharacterEnv(n,Farmer())
models = ['Guards_PPO_100k', 'Farmer_PPO_100k']
#env = VecFrameStack(env,4)

from tqdm import tqdm

def testing(model_select = models[0]):
    PPO_Path = os.path.join('Training','Saved Models',models[0])
    PPO_Path2 = os.path.join('Training','Saved Models',models[1])
    model = PPO.load(PPO_Path,env=env) # load model at path
    model2 = PPO.load(PPO_Path2,env=env2) # load model at path

    mean_score = []
    actions = []
    episodes = 1
    pbar = tqdm(total=n) if episodes == 1 else None # progress bar

    for episode in range(1,episodes+1):
        obs = env.reset() # observation
        obs2 = env2.reset() # observation
        done = False
        done2 = False
        score = 0
        score2 = 0
        
        while not done:
            action,_ = model.predict(obs) #using model
            actions.append(action)
            print('action', action)
            print('obs', obs)
            obs,reward,done,info, market_price = env.step(action) # obs = (health, hunger, energy, wealth)

            if action == 6:
                # print('return_sell_best_price 1', return_sell_best_price)
                print('obs after', obs)
            if action == 7:
                # print('return_buy_from_lowest 1', return_buy_from_lowest)
                print('obs after', obs)
            score += reward
            pbar.update(1) if episodes == 1 else None
            #####
            action2,_ = model.predict(obs2) #using model
            print('action2', action2)
            print('obs2', obs2)
            obs2,reward2,done2,info2, market_price2 = env2.step(action2) # obs = (health, hunger, energy, wealth)

            if action2 == 6:
                # print('return_sell_best_price 2', return_sell_best_price2)
                print('obs2 after', obs2)
            if action2 == 7:
                # print('return_buy_from_lowest 2', return_buy_from_lowest2)
                print('obs2 after', obs2)
            score += reward

            print('Market price', market_price)
            print('Market price 2', market_price2)
            
            print('')
            
        print(f'Episode:{episode} Score:{score}')
        mean_score.append(score)
        # env.render() #render per episode
    #env.close()
    pbar.close() if episodes == 1 else None

    print('Total Episodes:{} Average Score:{}'.format(episode, mean(mean_score))) if episode > 1 else None

    return mean_score, actions

mean_score, actions = testing(models[1])
# %% Plot Mean Scores
import matplotlib.pyplot as plt
plt.hist(mean_score,bins=30,facecolor='#2ab0ff', edgecolor='#169acf', linewidth=1)
plt.title('Guard Scores') 
plt.xlabel('Score') 
plt.ylabel('Count')
plt.show()
# %%
plt.hist(actions,bins=30,facecolor='#2ab0ff', edgecolor='#169acf', linewidth=1)
plt.title('Actions count') 
plt.xlabel('Action') 
plt.ylabel('Count')
plt.show()

# %%