#%% Imports
import os
import time
import pandas as pd
import random
import sys
import threading
import signal

from action import action
from Actions.set_positions import set_character_position, set_item_position
from Entities.characters import Characters
from Entities.items import Items
from Model.Env.character_env import CharacterEnv
from stable_baselines3 import PPO

class CamelotEnv:
    def __init__(self, dev='') -> None:
        self.dev = dev
        self.threads = []
        self.predict_flag = False
        self.step = 5
        self.env = CharacterEnv(self.step)
        self.PPO_Path = os.path.join('Model', 'Training', 'Saved Models', 'CharacterModel')
        self.model = PPO.load(self.PPO_Path, env=self.env)
        self.obs = self.env.reset() # observation (health, hunger, energy)
        self.action = -1
        self.initial_obs_action = pd.DataFrame([self.obs + (self.action,)], columns=["hunger", "energy", "health", "action"])
        self.state_history = []
        self.state_columns = ["hunger", "energy", "health", "action"]
        self.exit_event = threading.Event()

        # initial csv file
        self.initial_obs_action.to_csv('csv/state.csv', index=False)

        # Camelot mode
        if self.dev != 'dev':
            self.setup_env()
            self.setup_items()
            self.setup_camera()

        # Develop mode
        else:
            print('Testing environment')
            self.setup_items()

        signal.signal(signal.SIGINT, self.signal_handler)
        t = threading.Thread(target=self.main)
        self.threads.append(t)
        t.start()
        
        for t in self.threads:
            t.join()


    def signal_handler(self, signum, frame):
        self.exit_event.set()


    def setup_env(self):
        action('CreatePlace(Tavern, Tavern)')                       # Setup place
        self.kate = Characters('Kate', 'C', 'Long', 'Queen')        # Setup character
        set_character_position('Kate', 'Tavern.Door')               # Setup character position

    def setup_items(self):
        self.surfaces = ['Tavern.Table.Left', 'Tavern.Shelf.Right', 'Tavern.Bar.Center', 'Tavern.Table.Right']
        random.shuffle(self.surfaces)

        # Items :          ( name,        item_type,  effect, count,   position, hp_effect, hunger_effect)
        self.apple_list = [Items('poison_apple', 'Apple', 'Poison', 10, self.surfaces.pop(), -10, -5),
                           Items('magic_apple', 'Apple', 'Magic', 10, self.surfaces.pop(), 10, -3),
                           Items('force_apple', 'Apple', 'Force', 10, self.surfaces.pop(), 1, -1),
                           Items('heart_apple', 'Apple', 'Heart', 10, self.surfaces.pop(), 15, -2)]

        apples_name = []
        apples_effect = []
        apples_count = []
        apples_position = []
        apples_hp_effect = []
        apples_hunger_effect = []

        for apple in self.apple_list:
            apples_name.append(apple.name)
            apples_effect.append(apple.effect)
            apples_count.append(apple.count)
            apples_position.append(apple.position)
            apples_hp_effect.append(apple.hp_effect)
            apples_hunger_effect.append(apple.hunger_effect)


        self.apple_df = pd.DataFrame({"name": apples_name,
                                      "effect": apples_effect,
                                      "count": apples_count,
                                      "position": apples_position,
                                      "hp_effect": apples_hp_effect,
                                      "hunger_effect": apples_hunger_effect})
        self.apple_df_copy = self.apple_df.copy()

        self.apple_df.to_csv('csv/items.csv', index=False)

        if self.dev != 'dev':
            for apple in self.apple_list:
                set_item_position(apple.name, apple.item_type, apple.position, effect=apple.effect)

    def setup_camera(self):
        action('SetCameraFocus(Kate)')
        action('ShowMenu()')
        action('SetTitle(Camelot World)')
        action('HideMenu()')
        action('EnableInput()')

    def main(self):
        for i in range(self.step):

            # if control C then break (dev mode)
            if self.exit_event.is_set():
                break

            # predict action
            self.action,_ = self.model.predict(self.obs) #using model
            # get new observation
            self.obs, self.reward, self.done, self.info = self.env.step(self.action)

            # update csv file
            self.state_history.append(self.obs + (self.action,))
            self.state_history_df = pd.DataFrame(self.state_history, columns=self.state_columns)
            self.state_history_df.to_csv('csv/state.csv', index=False)
    
            # actions in Camelot
            if self.dev != 'dev':
                if self.action == 0 or self.action == 1 or self.action == 2 or self.action == 3:
                    apple = self.apple_list[self.action]
                    self.kate.take(apple.name, apple.position)
                    self.kate.drink()
                if self.action == 4:
                    self.kate.sleep('Tavern.BackLeftStool')
                if self.action == 5:
                    self.kate.wave()

            time.sleep(1)

            # itmes control
            if self.action == 0 or self.action == 1 or self.action == 2 or self.action == 3:
                self.apple_df_copy.loc[self.action, 'count'] -= 1

                self.apple_df_copy.to_csv('csv/items.csv', index=False)

        # initial csv file
        self.initial_obs_action.to_csv('csv/state.csv', index=False)
        self.apple_df.to_csv('csv/items.csv', index=False)
        print('\x1b[6;30;42m' + 'End main' + '\x1b[0m')
        

if __name__ == "__main__":
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    try:    # develop mode
        dev = args[0]
        camelot_env = CamelotEnv(dev = dev)
    except: # Camelot
        camelot_env = CamelotEnv()
        
