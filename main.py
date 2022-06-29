import os
import random
from time import sleep
import pandas as pd

from action import action
from Entities.characters import Characters
from Actions.set_positions import set_character_position, set_item_position
from Entities.items import Items
from threading import Thread
from stable_baselines3 import PPO
from Model.Env.character_env import CharacterEnv
from Model.npc import *

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class CamelotEnv:
    def __init__(self) -> None:
        self.step = 3000
        self.env_kate = CharacterEnv(self.step, Farmer(name='kate'))
        self.env_bob = CharacterEnv(self.step, Guards(wage=100, name='bob'))
        self.models = ['Guards_PPO_100k', 'Farmer_PPO_100k']
        self.PPO_Path_1 = os.path.join('Model', 'Training', 'Saved Models', self.models[1])
        self.PPO_Path_2 = os.path.join('Model', 'Training', 'Saved Models', self.models[0])
        self.model_kate = PPO.load(self.PPO_Path_1, env=self.env_kate)
        self.model_bob = PPO.load(self.PPO_Path_2, env=self.env_bob)
        self.obs_kate = self.env_kate.reset() # observation (health, hunger, energy, wealth)
        self.obs_bob = self.env_bob.reset() # observation (health, hunger, energy, wealth)
        self.actions_kate = []
        self.actions_bob = []
        self.last_location_kate = -1
        self.last_location_bob = -1
        self.action_kate = -1
        self.action_bob = -1
        
        # Market setting
        self.market = Market(inflation_rate=0.005)
        self.market_price_history = []
        self.selling_price_history = []
        self.buying_price_history = []

        self.initial_obs_action = pd.DataFrame([self.obs_kate + (self.action_kate,)], columns=["hunger", "energy", "health", "wealth", "action"])
        self.state_history_kate = []
        self.state_history_bob = []
        self.state_columns = ["hunger", "energy", "health", "wealth", "action"]

        # initial csv file
        self.initial_obs_action.to_csv('csv/kate_state.csv', index=False)
        self.initial_obs_action.to_csv('csv/bob_state.csv', index=False)

        self.setup_city()
        self.setup_house()
        self.setup_char()
        self.setup_items()
        self.setup_camera()

    def setup_city(self):
        action('CreatePlace(MainCity, City)')
        action('EnableIcon("Open_Green_House_City_Door", Open, MainCity.GreenHouseDoor, "Green House Door", true)')
        action('EnableIcon("Open_Brown_House_City_Door", Open, MainCity.BrownHouseDoor, "Brown House Door", true)')
        action('EnableIcon("Open_Red_House_City_Door", Open, MainCity.RedHouseDoor, "Red House Door", true)')
        action('EnableIcon("Open_Blue_House_City_Door", Open, MainCity.BlueHouseDoor, "Blue House Door", true)')
    
    def setup_char(self):
        self.kate = Characters('Kate', 'C', 'Long', 'Queen')        # Setup character
        self.bob = Characters('Bob', 'F', 'Mage_Full', 'HeavyArmour')        # Setup character Bob
        set_character_position('Kate', 'MainCity.Fountain')
        set_character_position('Bob', 'MainCity.NorthEnd')

        # Merchant
        self.tom = Characters('Tom', 'D', 'Short, Short_Beard, Short_Full', 'Merchant')
        self.emma = Characters('Emma', 'A', 'Ponytail', 'Merchant')
        self.isabella = Characters('Isabella', 'E', 'Straight', 'Bandit')
        set_character_position('Tom', 'MainCity.EastEnd')
        set_character_position('Emma', 'MainCity.Bench.Right')
        set_character_position('Isabella', 'MainCity.Plant')
        
    def setup_house(self):
        # Create green house
        action('CreatePlace(GreenCottage, Cottage)')
        action('EnableIcon("Open_Green_House_Door", Open, GreenCottage.Door, "Green House Door", true)')

        # Create brown house
        action('CreatePlace(BrownCottage, Cottage)')
        action('EnableIcon("Open_Brown_House_Door", Open, BrownCottage.Door, "Brown House Door", true)')

        # Create red house
        action('CreatePlace(RedCottage, Cottage)')
        action('EnableIcon("Open_Red_House_Door", Open, RedCottage.Door, "Red House Door", true)')

        # Create blue house
        action('CreatePlace(BlueCottage, Cottage)')
        action('EnableIcon("Open_Blue_House_Door", Open, BlueCottage.Door, "Blue House Door", true)')
    
    def setup_items(self):
        self.surfaces_places = [['GreenCottage.Shelf.Left', 'GreenCottage.Door', 'MainCity.GreenHouseDoor'], ['BrownCottage.Shelf.Right', 'BrownCottage.Door', 'MainCity.BrownHouseDoor'], ['RedCottage.Shelf.Left', 'RedCottage.Door', 'MainCity.RedHouseDoor'], ['BlueCottage.Shelf.Right', 'BlueCottage.Door', 'MainCity.BlueHouseDoor']]
        # random.shuffle(self.surfaces_places)
        self.item_surfaces = tuple(zip(*self.surfaces_places))[0]
        self.item_surfaces = list(self.item_surfaces)
        self.item_places = tuple(zip(*self.surfaces_places))[1]
        self.item_places = list(self.item_places)
        self.item_city_door = tuple(zip(*self.surfaces_places))[2]
        self.item_city_door = list(self.item_city_door)

        # Items :          ( name,        item_type,  effect, count,   position, hp_effect, hunger_effect)
        self.apple_list = [Items('poison_apple', 'Apple', 'Poison', 1000, self.item_surfaces.pop(0), -10, -5),
                           Items('small_medicine', 'Bottle', 'Magic', 1000, self.item_surfaces.pop(0), 10, -3),
                           Items('expensive_medicine', 'GoldCup', 'Force', 1000, self.item_surfaces.pop(0), 1, -1),
                           Items('heart_apple', 'Apple', 'Heart', 1000, self.item_surfaces.pop(0), 0, 15)]

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
                                    #   "effect": apples_effect,
                                      "count": apples_count,
                                      "position": apples_position,
                                      "hp_effect": apples_hp_effect,
                                      "hunger_effect": apples_hunger_effect})
        self.apple_df_copy = self.apple_df.copy()

        self.apple_df.to_csv('csv/items.csv', index=False)

        for apple in self.apple_list:
            set_item_position(apple.name, apple.item_type, apple.position, effect=apple.effect)

    def setup_camera(self):
        # self.bob.focus()
        self.kate.focus()
        action('SetCameraMode(track)')
        action('ShowMenu()')
        action('HideMenu()')
        action('EnableInput()')

    @threaded
    def kate_main(self):
        for i in range(self.step):
            # predict action
            if self.action_kate == 0 or self.action_kate == 1 or self.action_kate == 2 or self.action_kate == 3 :
                self.last_location_kate = self.action_kate
            self.action_kate,_ = self.model_kate.predict(self.obs_kate) #using model

            # get new observation
            self.obs_kate, self.reward_kate, self.done_kate, self.info_kate, self.market_price = self.env_kate.step(self.action_kate)
            # store market price
            if self.action_kate == 6 or self.action_kate==7:
                self.market_price_history.append(['kate', self.market_price])
                # print('self.market_price_history',self.market_price_history)

             # update csv file
            self.state_history_kate.append(self.obs_kate + (self.action_kate,))
            self.state_history_kate_df = pd.DataFrame(self.state_history_kate, columns=self.state_columns)
            self.state_history_kate_df.to_csv('csv/kate_state.csv', index=False)

            # If eat apple
            if self.action_kate == 0 or self.action_kate == 1 or self.action_kate == 2 or self.action_kate == 3:
                
                # items state update
                self.apple_df_copy.loc[self.action_kate, 'count'] -= 1
                self.apple_df_copy.to_csv('csv/items.csv', index=False)

                if self.last_location_kate != self.action_kate and self.last_location_kate != -1:
                    if self.kate.exit(self.item_places[self.last_location_kate]) is True:
                        self.kate.enter(self.item_city_door[self.last_location_kate])

                if self.kate.exit(self.item_city_door[self.action_kate]) is True:
                    self.kate.enter(self.item_places[self.action_kate])

                apple = self.apple_list[self.action_kate]
                self.kate.take(apple.name, apple.position)
                self.kate.drink()

            if self.action_kate == 4:
                if self.last_location_kate == 0 or self.last_location_kate == 1 or self.last_location_kate == 2 or self.last_location_kate == 3:
                    self.kate.exit(self.item_places[self.last_location_kate])
                    self.kate.enter(self.item_city_door[self.last_location_kate])

                self.kate.sleep('MainCity.Bench')
            if self.action_kate == 5:
                self.kate.wave()

            if self.action_kate == 6:           # Sell
                if self.last_location_kate == 0 or self.last_location_kate == 1 or self.last_location_kate == 2 or self.last_location_kate == 3:
                    self.kate.exit(self.item_places[self.last_location_kate])
                    self.kate.enter(self.item_city_door[self.last_location_kate])

                self.kate.give('heart_apple', 'Emma')
                self.emma.pocket('heart_apple')
                
            
            if self.action_kate == 7:           # Buy
                if self.last_location_kate == 0 or self.last_location_kate == 1 or self.last_location_kate == 2 or self.last_location_kate == 3:
                    self.kate.exit(self.item_places[self.last_location_kate])
                    self.kate.enter(self.item_city_door[self.last_location_kate])
                    
                self.kate.take('heart_apple', 'Emma')
                self.kate.pocket('heart_apple')

            if self.action_kate == 8:
                self.kate.wave()

    @threaded
    def bob_main(self):
        for i in range(self.step):
            # predict action
            if self.action_bob == 0 or self.action_bob == 1 or self.action_bob == 2 or self.action_bob == 3 :
                self.last_location_bob = self.action_bob
            self.action_bob,_ = self.model_bob.predict(self.obs_bob) #using model

            # get new observation
            self.obs_bob, self.reward_bob, self.done_bob, self.info_bob, self.market_price = self.env_bob.step(self.action_bob)
            # store market price
            if self.action_bob == 6 or self.action_bob==7:
                self.market_price_history.append(['bob', self.market_price])
                # print('self.market_price_history',self.market_price_history)

             # update csv file
            self.state_history_bob.append(self.obs_bob + (self.action_bob,))
            self.state_history_bob_df = pd.DataFrame(self.state_history_bob, columns=self.state_columns)
            self.state_history_bob_df.to_csv('csv/bob_state.csv', index=False)

            # If eat apple
            if self.action_bob == 0 or self.action_bob == 1 or self.action_bob == 2 or self.action_bob == 3:
                
                # items state update
                self.apple_df_copy.loc[self.action_bob, 'count'] -= 1
                self.apple_df_copy.to_csv('csv/items.csv', index=False)

                if self.last_location_bob != self.action_bob and self.last_location_bob != -1:
                    if self.bob.exit(self.item_places[self.last_location_bob]) is True:
                        self.bob.enter(self.item_city_door[self.last_location_bob])

                if self.bob.exit(self.item_city_door[self.action_bob]) is True:
                    self.bob.enter(self.item_places[self.action_bob])

                apple = self.apple_list[self.action_bob]
                self.bob.take(apple.name, apple.position)
                self.bob.drink()

            if self.action_bob == 4:
                if self.last_location_bob == 0 or self.last_location_bob == 1 or self.last_location_bob == 2 or self.last_location_bob == 3:
                    self.bob.exit(self.item_places[self.last_location_bob])
                    self.bob.enter(self.item_city_door[self.last_location_bob])

                self.bob.sleep('MainCity.Bench')
            if self.action_bob == 5:
                self.bob.wave()

            if self.action_bob == 6:           # Sell
                if self.last_location_bob == 0 or self.last_location_bob == 1 or self.last_location_bob == 2 or self.last_location_bob == 3:
                    self.bob.exit(self.item_places[self.last_location_bob])
                    self.bob.enter(self.item_city_door[self.last_location_bob])

                self.bob.give('heart_apple', 'Emma')
                self.emma.pocket('heart_apple')
                
            
            if self.action_bob == 7:           # Buy
                if self.last_location_bob == 0 or self.last_location_bob == 1 or self.last_location_bob == 2 or self.last_location_bob == 3:
                    self.bob.exit(self.item_places[self.last_location_bob])
                    self.bob.enter(self.item_city_door[self.last_location_bob])
                    
                self.bob.take('heart_apple', 'Emma')
                self.bob.pocket('heart_apple')

            if self.action_bob == 8:
                self.bob.wave()

        while True:
            pass

    @threaded
    def camera_setting(self):
        last_character = 'Kate'
        while True:
            file = open('csv/camera.txt','r')
            character_focus = file.read()
            if last_character != character_focus:
                if character_focus == 'Kate':
                    self.kate.focus()
                if character_focus == 'Bob':
                    self.bob.focus()
                last_character = character_focus
            file.close()
            sleep(2)


if __name__ == "__main__":
    # CamelotEnv()
    cam_env = CamelotEnv()
    handle = cam_env.kate_main()
    handle2 = cam_env.bob_main()
    handle_camera = cam_env.camera_setting()

    handle_camera.join()
    handle2.join()
    handle.join()