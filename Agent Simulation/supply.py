#%%
# supply and demand
# sell just food for now
# buy from gatherer
# buyer going for best deal
import numpy as np

class Traders:
    def __init__(self, name, minval=10, inflation_rate=0.001):  
        self.name = name 
        self.min = minval # min value accepted        # change later for inflation
        self.prices = {"apple":round(np.random.randint(10,15),2)} #market price
        self.inflation_rate = inflation_rate
        
    # merchants
    # lower price if does not sell
    # increase price if they sell
    def sell(self,sale=False):
        increment = round(np.random.random(),2)
        for i in self.prices:
            if self.prices[i] < self.min and sale:
                self.prices[i] == self.min
                self.prices[i] += increment 
            elif self.prices[i] > self.min:
                self.prices[i] += increment if sale else -increment
            elif self.prices[i] == self.min and sale:
                self.prices[i] += increment 
            
        if sale:
            # increase due to market inflation
            self.min += self.min*self.inflation_rate
        return self.prices

    def buy(self,item="apple"):
        #30% profit margin based on market price
        return round(self.prices[item]*0.7 ,2)

class Market:
    def __init__(self, inflation_rate=0.001):
        self.traders = [Traders("trader"+str(i),round(np.random.randint(7,10),2),inflation_rate) for i in range(3)]
        
    def market_prices(self):
        return [round(self.traders[i].prices["apple"],2) for i in range(len(self.traders))]

    def lowest_sellprice(self):
        return min(self.market_prices())

    def buy_from_lowest(self):
        index = { #-------make universal next time
            0:[True,False,False],
            1:[False,True,False],
            2:[False,False,True]
        }
        ind = index[self.market_prices().index(self.lowest_sellprice())]
        selling_price = self.lowest_sellprice()

        #change suppy market cost
        for i in range(3):
            self.traders[i].sell(ind[i])

        return selling_price

    def sell_best_price(self):
        return max([i.buy() for i in self.traders])


# %%%%%%%%%%%%%%%% Test %%%%%%%%%%%%%%%%% #
'''
market = Market()

for i in range(200):
    print([market.traders[i].min for i in range(len(market.traders))])
    print("current market prices",market.market_prices())
    print("buying cheapest",market.buy_from_lowest())
    print("selling for best offer",market.sell_best_price(),"\n")


# %% plot inflation
market = Market(inflation_rate=0.005)
selling_price = []
buying_price = []
for i in range(1000):
    selling_price.append(market.buy_from_lowest())
    buying_price.append(market.sell_best_price())

import matplotlib.pyplot as plt

plt.plot(range(len(selling_price)),selling_price,label="selling price")
plt.plot(range(len(buying_price)),buying_price,label="buying price")
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Market Prices over Time w/ inflation')
plt.legend()
plt.show()
'''

# %% plot market
'''
market = Market(inflation_rate=0.005)
market_price=[[],[],[]]
buying_price = []
for i in range(500):
    market.buy_from_lowest()
    for j in range(len(market.traders)):
        market_price[j].append(market.market_prices()[j])
    buying_price.append(market.sell_best_price())

import matplotlib.pyplot as plt

plt.figure(figsize=(20,10))
plt.plot(range(len(market_price[0])),market_price[0],label="trader 1")
plt.plot(range(len(market_price[1])),market_price[1],label="trader 2")
plt.plot(range(len(market_price[2])),market_price[2],label="trader 3")
plt.plot(range(len(buying_price)),buying_price,label="buying price")
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Apple Market Prices over Time w/ inflation')
plt.legend()
plt.show()
'''