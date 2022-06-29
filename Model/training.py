#%% Imports
import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from stable_baselines3.common.evaluation import evaluate_policy
from Env.character_env import CharacterEnv

#%% Train Model using agent/ppo model
env = CharacterEnv(1000000)

save_path = os.path.join('Model', 'Training', 'Saved Models')
stop_callback = StopTrainingOnRewardThreshold(reward_threshold=10000,verbose=1)
eval_callback = EvalCallback(env,
                            callback_on_new_best=stop_callback,
                            eval_freq=10000,
                            best_model_save_path=save_path, 
                            verbose=1)

log_path = os.path.join('Training', 'Logs')
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_path)
model.learn(total_timesteps=100000)

#%% Evaluate
env = CharacterEnv()
evaluate_policy(model, env, n_eval_episodes=10, render=False)

#%% Save Model
PPO_Path = os.path.join('Training','Saved Models','CharacterModel')
model.save(PPO_Path)
