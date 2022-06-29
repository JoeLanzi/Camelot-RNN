class CreateMap():
    pass

#%% Randomly Creating Map
W,S,G,F = 0,1,2,3 #water,stone,grass,forest
C = 5
biom = [W,S,G,F]
biom_shape = (6,6)

import numpy as np
water_area = np.random.choice(biom, size=biom_shape, replace=True, p=[0.5, 0, 0.5, 0])
grass_area_1 = np.random.choice(biom, size=biom_shape, replace=True, p=[0, 0, 1.0, 0])
grass_area_2 = np.random.choice(biom, size=biom_shape, replace=True, p=[0, 0.05, 0.9, 0.05])  
forest_area =  np.random.choice(biom, size=biom_shape,replace=True, p=[0, 0, 0.8, 0.2])             

top = np.concatenate((water_area,grass_area_1), axis=1 )
bottom = np.concatenate((forest_area,grass_area_2), axis=1 )
map1 = np.concatenate((top,bottom), axis=0 )
map1


#%% Saved map
map1 = [[0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
        [0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 0, 2, 2, C, 2, 2],
        [0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
        [0, 0, 2, 0, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 3, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 3, 2, 2, 3, 2, 2, 2, 1],
        [3, 2, 2, 2, 3, 2, 2, 1, 2, 2]]

#%%
map1 = [[0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2],
       [0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2],
       [2, 0, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2],
       [2, 2, 0, 0, 0, 0, 2, 2, C, 2, 2, 2],
       [0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2],
       [2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2],
       [2, 3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2],
       [3, 3, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2],
       [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2],
       [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2],
       [2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2],
       [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]


#%% Display Map 

import pygame, sys

"""Link Tile to Colour"""
TileColour = {W : (0,0,255),        # blue
              S : (145, 142, 133),  # stonegray
              G : (124,252,0),      # grassy green
              F : (0,100,0),        # forest green
              C : (0,0,0)
              }


"""CREATING MAP-SIZE"""
TILESIZE = 60
MAPWIDTH = len(map1[0])
MAPHEIGHT = len(map1[1])

"""Create Display"""
pygame.init()
DISPLAY = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))


"""Basic User Interface"""
while True:
    
    for event in pygame.event.get():
        
        """Quit (when "x" in top-right corner is pressed)"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    """Draw Map to Display"""
     #ROWS
    for row in range(MAPHEIGHT):
          #COLUMNS
           for col in range(MAPWIDTH):
             #DRAW TILE
             """pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)"""
             pygame.draw.rect(DISPLAY,TileColour[map1[row][col]],(col*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))
             
    """Update Display"""
    pygame.display.update()



# %% Euclidean Distance
from scipy.spatial import distance
point_1 = (1, 2)
point_2 = (4, 5)
# computing the euclidean distance
euclidean_distance = distance.euclidean(point_1, point_2)
print('Euclidean Distance between', point_1, 'and', point_2, 'is: ', euclidean_distance)
# %% Getting Water, Tree, or Stone coordinates
result = np.where(np.array(map1) == W)
item_coordinates = list(zip(result[0], result[1]))

result = np.where(np.array(map1) == C)
char_coordinates = list(zip(result[0], result[1]))
# %% Finding distance between char and the 2 stone
dist = []
for i in range(len(item_coordinates)):
    dist.append(distance.euclidean(char_coordinates[0], item_coordinates[i]) )
dist
# %% coordinate of item closes to char
item_coordinates[np.where(dist==min(dist))[0][0]]

# %%
