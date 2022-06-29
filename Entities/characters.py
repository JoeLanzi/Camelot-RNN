'''
Authors: Camelot Developers (Edited and Commented by Chien-Chou Wu)
Purpose: Class for characters

0. Set Camera focus on character
1. Give item to left hand
2. Give item to right hand
3. Puts the item they're holding in their left hand into their pocket
4. Character takes an item out of their pocket and hold it in their left hand.
5. Walk To
6. Take
7. Give
8. Drink
9. Sleep
10. Sit
11. Wave
12. Exit
13. Enter
14. Dance
. Die
'''

from action import action
# from action_queue import action_queue
from Actions.set_positions import set_item_position

class Characters:
    def __init__(self, name, body_type, hair_style, outfit):
        self.name = name
        self.body_type = body_type
        self.hair_style = hair_style
        self.outfit = outfit

        action('CreateCharacter(' + self.name + ',' + self.body_type + ')')
        action('SetHairStyle(' + self.name + ',' + self.hair_style + ')')
        action('SetClothing(' + self.name + ',' + self.outfit + ')')

    # 0. Set Camera focus on character
    def focus(self):
        action('SetCameraFocus(' + self.name + ')')

    # 1. Give item to left hand
    def give_item_left(self, item_name, item_type):
        set_item_position(item_name, item_type, self.name)
    
    # 2. Give item to right hand
    def give_item_right(self, item_name, item_type):
        set_item_position(item_name, item_type, self.name)
        action('Draw(' + self.name + ',' + item_name + ')')

    # 3. Puts the item they're holding in their left hand into their pocket
    def pocket(self, item_name):
        action('Pocket(' + self.name + ',' + item_name + ')')

    # 4. Character takes an item out of their pocket and hold it in their left hand.
    def unpocket(self, item_name):
        action('Unpocket(' + self.name + ',' + item_name + ')')

    # 5. Walk To
    def walk_to(self, target):
        action('WalkTo(' + self.name + ',' + target + ')')

    # 6. Take
    def take(self, item_name, target):
        action('Take(' + self.name + ',' + item_name + ',' + target + ')')

    # 7. Give
    def give(self, item_name, target):
        action('Give(' + self.name + ',' + item_name + ',' + target + ')')

    # 8. Drink
    def drink(self):
        action('Drink(' + self.name + ')')

    # 9. Sleep
    def sleep(self, place):
        action('Sleep(' + self.name + ',' + place + ')')
    
    # 10. Sit
    def sit(self, place):
        action('Sit(' + self.name + ',' + place + ')')
    
    # 11. Wave
    def wave(self):
        action('Wave(' + self.name + ')')

    # 12. Exit
    def exit(self, target):
        return action('Exit(' + self.name + ', ' + target + ', false)')

    # 13. Enter
    def enter(self, target):
        action('Enter(' + self.name + ', ' + target + ', false)')

    # 14. Dance
    def dance(self):
        action('Dance(' + self.name + ')')

    # 15. Clap
    def clap(self):
        action('Clap(' + self.name + ')')

    # 15. Laugh
    def laugh(self):
        action('Laugh(' + self.name + ')')

    # 15. Kneel
    def kneel(self):
        action('Kneel(' + self.name + ')')

    # 16. Set position
    def set_position(self, target):
        action('SetPosition(' + self.name + ', ' +  target + ')')


    # . Die
    def die(self):
        action('Die(' + self.name + ')')