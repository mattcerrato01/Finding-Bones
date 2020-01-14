import random
import pygame as p

class WorldState:

    overworld = True

    def state(self):
        return WorldState.overworld

    def toggle(self):
        WorldState.overworld = not WorldState.overworld
    def x(self):
        x = 0

class NameGenerator:

    def __init__(self):
        self.male_names = ["Kristoff","William","Jonathon","Walter","Francis","Peter","Frederick","Roger","Arthur","Cedric","Zane","Donald","Leo","Ronald","Robin","Gavin","Charles","Benjamin","Augustus"]

        self.female_names = ["Murial","Mary","Elizabeth","Maria"]

    def generate(self, male = True):
        if male:
            return self.male_names[random.randint(0, len(self.male_names)-1)]
        return self.female_names[random.randint(0, len(self.female_names)-1)]

class CoordConverter:

    offset_x = 0
    offset_y = 0

    def set_offset_x(self, offset_x):
        CoordConverter.offset_x = offset_x

    def set_offset_y(self, offset_y):
        CoordConverter.offset_y = offset_y

    def real_x(self, screen_x):
        return screen_x - CoordConverter.offset_x

    def real_y(self, screen_y):
        return screen_y - CoordConverter.offset_y

    def screen_x(self, real_x):
        return real_x + CoordConverter.offset_x

    def screen_y(self, real_y):
        return real_y + CoordConverter.offset_y

class Inventory:

    inventory = []

    def get_inventory(self):
        return Inventory.inventory[:]

    def append_to_inventory(self, object):
        Inventory.inventory.append(object)

    def remove_from_inventory(self, object):
        Inventory.inventory.remove(object)

class Actions:

    dialogue_list = []

    def dialogue_box(self, dialogue):

        Actions.dialogue_list.append((dialogue, p.time.get_ticks()))

    def update_dialogue_box(self):

        while len(Actions.dialogue_list) > 4:
            Actions.dialogue_list.pop(0)

        while len(Actions.dialogue_list) > 0:
            if Actions.dialogue_list[0][1]+3000 < p.time.get_ticks():
                Actions.dialogue_list.pop(0)
            else:
                break

        return len(Actions.dialogue_list) > 0

        """
        :param dialogue: what to print
        
        prints dialogue to dialogue box for period of time
        
        :return: 
        """
