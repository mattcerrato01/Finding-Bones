# TESTING PUSH
import pygame as p
import math as m
import GameStates as gs

coord = gs.CoordConverter()
world = gs.WorldState()

def loadify(imgname): #Returns loaded Image
    return p.image.load(imgname).convert_alpha()

class Tile: #One 800x800 tile, contains the collision sprites contained within that tile

    def __init__(self, name, collision_group, x, y):
        self.image = loadify(name)
        self.image = p.transform.scale(self.image, (800, 600))
        self.underworld_image = p.transform.scale(loadify(name[:-4] + "_underworld" + name[-4:]), (800, 600))
        self.collision_group = collision_group
        self.x = x*800
        self.y = y*600


    def add_to_group(self, *object):
        self.collision_group.add(object)

    def remove_from_goup(self, *object):
        self.collision_group.remove(object)

    def draw(self, screen): #draws the tile and all the sprites within it
        if world.state():
            screen.blit(self.image, (coord.screen_x(self.x), coord.screen_y(self.y)))
        else:
            screen.blit(self.underworld_image, (coord.screen_x(self.x), coord.screen_y(self.y)))
        for object in self.collision_group:
            object.draw(screen)



class Map: #Contains a 2D array of all the tiles, and a function that draws only visible tiles

    def __init__(self, image_name_array, collidable_group): #takes a 2D array of image names and a list of collidable sprites. Instantiates tiles with images as backgrounds and containing all collidable sprites within their area into the 2D array "tile array"
        self.tile_array = []
        x = 0
        for name_array in image_name_array:
            y = 0
            self.tile_array.append([])
            for name in name_array:
                new_group = p.sprite.Group()
                for collidable in collidable_group:
                    if collidable.x >= x*800 and collidable.x < (x+1)*800 and collidable.y >= y*600 and collidable.y < (y+1)*600:
                        new_group.add(collidable)



                self.tile_array[x].append(Tile(name, new_group, x, y))
                y+=1
            x+=1

    def draw(self, screen): #called in the main while loop, determines what tiles are visible and calls their draw functions
#tile player is in

        return_group = p.sprite.Group()

        variable_1 = int(coord.real_x(400)//800)
        variable_2 = int(variable_1 + coord.real_x(400)//400%2*2-1)
        variable_a = int(coord.real_y(300)//600)
        variable_b = int(variable_a + coord.real_y(300)//300%2*2-1)
        variable_5 = len(self.tile_array)

        boolean_1 = variable_1 >= 0 and variable_1 < variable_5
        boolean_2 = variable_2 >= 0 and variable_2 < variable_5
        boolean_a = variable_a >= 0 and variable_a < variable_5
        boolean_b = variable_b >= 0 and variable_b < variable_5

        if boolean_1 and boolean_a:
            self.tile_array[variable_1][variable_a].draw(screen)
            return_group.add(self.tile_array[variable_1][variable_a].collision_group.sprites())
        if boolean_1 and boolean_b:
            self.tile_array[variable_1][variable_b].draw(screen)
            return_group.add(self.tile_array[variable_1][variable_b].collision_group.sprites())
        if boolean_2 and boolean_a:
            self.tile_array[variable_2][variable_a].draw(screen)
            return_group.add(self.tile_array[variable_2][variable_a].collision_group.sprites())
        if boolean_2 and boolean_b:
            self.tile_array[variable_2][variable_b].draw(screen)
            return_group.add(self.tile_array[variable_2][variable_b].collision_group.sprites())

        #p.draw.rect(screen,(0,0,0),(0,299,800,2))
        #p.draw.rect(screen,(0,0,0),(399,0,2,600))

        return return_group