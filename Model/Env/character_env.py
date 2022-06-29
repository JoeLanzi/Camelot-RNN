#%% Imports
import numpy as np
from gym import Env, spaces
from Model.npc import *
from reward import happiness
from visual import plot

#%% Camelot Environment
class CharacterEnv(Env):
    def __init__(self,max_training_length=10000,npc=NPC()):
        self.action_space = spaces.Discrete(9) # 9 actions
        self.observation_space = spaces.Box(np.array([0.0, 0.0, 0.0, 0.0],dtype=np.float32), np.array([100.0, 100.0, 100.0, 100.0],dtype=np.float32))

        self.NPCs = npc
        self.state = self.NPCs.return_state()
        self.market_price = self.NPCs.return_market_price()

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

        # Market price
        self.market_price = self.NPCs.return_market_price()

        # Return step information
        return self.state, reward, done, info, self.market_price
    
    def render(self):
        # Implement viz in camelot
        plot(self.NPCs.stat_record)

    def reset(self):
        self.NPCs.reset()
        self.training_length = self.max_training_length
        return self.NPCs.return_state()