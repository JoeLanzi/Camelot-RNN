#%%
# market
from supply import Market

market = Market()
class NPC():
    def __init__(self,skill=0):
        self.health = 100
        self.hunger = 100
        self.energy = 100
        self.wealth = 100
        self.skill = skill
        self.stat_record = [[self.health],
                            [self.hunger],
                            [self.energy],
                            [self.wealth]]

        global market # market supply and demand
        self.market = market 
        
    def return_state(self):
        return (self.health, self.hunger, self.energy,round(self.wealth,2))

    def get_action_meanings(self):
        return {0: "Eat poison apple",
                1: "Eat magic apple",
                2: "Eat force apple",
                3: "Eat heart apple",
                4: "Sleep",
                5: "Do nothing",
                6: "Sell Item",
                7: "Buy Item" 
                }

    def actions(self,action):
        if action == 0:           # "Eat bad apple"
            self.health -= 10
            self.hunger -= 5
        elif action == 1:         # "Eat Apple"
            self.hunger += 15
        elif action == 2:         # "Drink small medicine"
            self.health += 10
            self.hunger += 3
        elif action == 3:         # "Use expensive medicine"
            self.health += 15
            self.hunger += 3
        elif action == 4:         # "Sleep"
            self.health += 5
            self.energy += 25
        elif action == 5:         # "Do Nothing"
            pass

        elif action == 6:         # "Sell Item for best price"
            self.wealth += round(self.market.sell_best_price(),2)
        elif action == 7 and self.wealth > self.market.buy_from_lowest():         # "Buy cheapest item"
            self.wealth -= round(self.market.buy_from_lowest(),2)
            self.hunger += 15
    
    def reset(self) -> None:
        # Reset NPC State
        self.health = 100
        self.hunger = 100
        self.energy = 100
        self.wealth = 100
        # Reset training step
        self.stat_record = [[self.health],
                            [self.hunger],
                            [self.energy],
                            [self.wealth]]


class Farmer(NPC):
    def __init__(self):
        super().__init__(skill=1)

    def actions(self,action):
        if action in range(7):
            NPC.actions(self,action)
        elif action == 8:       # "Gather Food" 
                self.wealth += round(1.25*self.market.sell_best_price() ,2)
            

class Merchant(NPC):
    def __init__(self):
        super().__init__(skill=2)

    def actions(self,action):
        if action in range(5):
            NPC.actions(self,action)
        elif action == 6:       # "earn extra from selling"
            self.wealth += round(1.1*self.market.sell_best_price() ,2)
        elif action == 7 and self.wealth > self.market.buy_from_lowest():     # "earn extra from buying"  
            self.wealth -= round(0.7*self.market.buy_from_lowest() ,2)


class Guards(NPC):
    def __init__(self,wage=100):
        super().__init__(skill=3)
        self.wage = wage

    def actions(self,action):
        if action in range(7):
            NPC.actions(self,action)
        else:
            if action == 8:       # "Patrol" 
                self.wealth += self.wage
                self.energy -= 5
            else:
                pass

class Apothecary(NPC):
    def __init__(self):
        super().__init__(skill=4)

    def actions(self,action):
        if action in range(7):
            NPC.actions(self,action)
        else:
            if action == 8:       # "Sell Potion" 
                self.wealth += round(1.25*self.market.sell_best_price() ,2)
            else:
                pass
#%% Test 
'''
market = Market()
peasant = NPC()
farmer = Farmer()
merchant = Merchant()
guard = Guards()

NPCs = [peasant,farmer,merchant,guard]

#%%
for i in NPCs:
    if i.skill not in [1,2]:
        i.health -= 10
    print(i.return_state())

for i in range(len(peasant.stat_record)):
    peasant.stat_record[i].append(peasant.return_state()[i])
peasant.stat_record
#%%
# Compare Farmer to Merchant selling
farmer.actions(6)
print(farmer.return_state())

merchant.actions(6)
print(merchant.return_state())

# Guards
guard.actions(6)
print(guard.return_state())

guard.actions(8)
print(guard.return_state())

# %%
merchant.health = 100
[i.health <=0 for i in NPCs].count(True) == len(NPCs)
'''