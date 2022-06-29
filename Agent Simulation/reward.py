#%%
import numpy as np
import math

def sigmoid(x):
    z = np.exp(-0.09*(x - 50))
    sig = 1 / (1 + z)
    return sig if z != 1 else 0

def log(x):
    return 0.1*np.log(x) if x >= 1 else 0

def gauss(x):
    return math.erf(3*x/100)-1

def happiness(state):
    return gauss(state[0]) + gauss(state[1]) + gauss(state[2]) + log(state[3]) 

'''
# %%
import matplotlib.pyplot as plt
import random
import numpy as np
x = random.sample(range(0, 100000), 100)
x.sort()

plt.plot(x,0.1*np.log(x))
# %%
x = random.sample(range(0, 100), 100)
x.sort()

plt.plot(x,[sigmoid(x[i]) for i in x])

# %%
x = random.sample(range(0, 100), 100)
x.sort()

plt.plot(x,[2*math.erf(3*i/100)-1 for i in x])

'''