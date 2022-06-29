#%% Imports
import numpy as np
from gym import Env, spaces

#%% Camelot Environment
class CharacterEnv(Env):
    def __init__(self,max_training_length=10000):
        self.action_space = spaces.Discrete(6) # 6 actions
        self.observation_space = spaces.Box(np.array([0.0, 0.0, 0.0],dtype=np.float32), np.array([100.0, 100.0, 100.0],dtype=np.float32))

        self.hunger = 0
        self.energy = 100
        self.health = 100
        # self.location = 0     # 0 at camp, 1 at plant
        # self.state = (self.health, self.hunger, self.energy,self.location) # initial state
        self.state = (self.hunger, self.energy, self.health) # initial state

        self.max_training_length = max_training_length
        self.training_length = max_training_length


    def get_action_meanings(self):
        return {0: "Eat poison apple",
                1: "Eat magic apple",
                2: "Eat force apple",
                3: "Eat heart apple",
                4: "Sleep",
                5: "Wave"}

    def step(self, action):
        '''stat logic'''
        # reduce health, hunger, and energy
        if self.hunger < 100:
            self.hunger += 5
        
        if self.energy > 0:
            self.energy -= 3
        
        if self.hunger >= 100 or self.energy <= 0:
            self.health -= 10
        
        '''actions'''
        if action == 0: # poison
            self.health -= 10
            self.hunger += 5
        if action == 1: # magic
            self.health += 10
            self.hunger -= 3
        if action == 2: # force
            self.health += 3
            self.hunger -= 15
        if action == 3: # heart
            self.health += 15
            self.hunger -= 2
        if action == 4: # sleep
            self.health += 0
            self.energy += 25
        if action == 5: # wave
            pass
        
        if self.hunger >= 100:
            self.hunger = 100
        if self.hunger <= 0:
            self.hunger = 0
        if self.energy >= 100:
            self.energy = 100
        if self.energy <= 0:
            self.energy = 0
        if self.health >= 100:
            self.health = 100
        if self.health <= 0:
            self.health = 0

        # self.state = (self.health, self.hunger, self.energy,self.location)
        self.state = (self.hunger, self.energy, self.health)

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
        self.hunger = 0
        self.energy = 100
        self.health = 100
        # self.location = 0
        # Reset training step
        self.training_length = self.max_training_length
        return self.state