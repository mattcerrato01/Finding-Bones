import pygame as p
import math as m


def loadify(imgname): #Returns loaded Image
    return p.image.load(imgname).convert_alpha()

class Tile: #One 800x800 tile, contains the collision sprites contained within that tile

    def __init__(self, name, collision_group, x, y):
        self.image = loadify(name)
        self.image = p.transform.scale(self.image, (800, 800))
        self.collision_group = collision_group
        self.x = x*800
        self.y = y*800


    def add_to_group(self, *object):
        self.collision_group.add(object)

    def remove_from_goup(self, *object):
        self.collision_group.remove(object)

    def draw(self, screen, offset_x, offset_y): #draws the tile and all the sprites within it
        screen.blit(self.image, (self.x-offset_x+374, self.y-offset_y+228))
        for object in self.collision_group:
            object.draw(screen, offset_x, offset_y)

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
                    if collidable.x >= x*800 and collidable.x < (x+1)*800 and collidable.y >= y*800 and collidable.y < (y+1)*800:
                        new_group.add(collidable)



                self.tile_array[x].append(Tile(name, new_group, x, y))
                y+=1
            x+=1

    def draw(self, screen, offset_x, offset_y): #called in the main while loop, determines what tiles are visible and calls their draw functions
#tile player is in

        return_group = p.sprite.Group()


        if int(offset_x // 800) >= 0 and int(offset_x // 800) < len(self.tile_array) and int(offset_y // 800) >= 0 and int(offset_y // 800) < len(self.tile_array[0]):
            self.tile_array[int(offset_x // 800)][int(offset_y // 800)].draw(screen, offset_x-25, offset_y)
            return_group.add(self.tile_array[int(offset_x // 800)][int(offset_y // 800)].collision_group.sprites())
        one = False
        two = False

#tile to the right / left of player
        if int(offset_x // 800 + offset_x // 400 % 2 * 2 - 1) >= 0 and int(offset_x // 800 + offset_x // 400 % 2 * 2 - 1) < len(self.tile_array) and int(offset_y // 800) >= 0 and int(offset_y // 800) < len(self.tile_array[0]) :
            self.tile_array[int(offset_x // 800 + offset_x // 400 % 2 * 2 - 1)][int(offset_y // 800)].draw(screen, offset_x-25, offset_y)
            return_group.add(self.tile_array[int(offset_x // 800 + offset_x // 400 % 2 * 2 - 1)][int(offset_y // 800)].collision_group.sprites())
            one = True

        #print(str(int(offset_x // 800 + offset_x // 400 % 2 * 2 - 1) >= 0) + " : " + str(int(offset_x // 800 + offset_x // 400 % 2 * 2 - 1) < len(self.tile_array)) + " : " + str(int(offset_y // 800) >= 0) + " : " + str(int(offset_y // 800) < len(self.tile_array[0])))
        #print(str(offset_x) + ", " + str(offset_y))

#tile above / below the player
        if int(offset_y // 800 + (offset_y // 400 % 2 * 2 - 1)) >= 0 and int(offset_y // 800 + (offset_y // 400 % 2 * 2 - 1)) < len(self.tile_array[0]) and int(offset_x // 800) >= 0 and int(offset_x // 800) < len(self.tile_array):
            self.tile_array[int(offset_x // 800)][int(offset_y // 800 + (offset_y // 400 % 2 * 2 - 1))].draw(screen, offset_x-25, offset_y)
            return_group.add(self.tile_array[int(offset_x // 800)][int(offset_y // 800 + (offset_y // 400 % 2 * 2 - 1))].collision_group.sprites())
            two = True

#tile in (left OR right) and (top OR bottom) of screen
        if one and two:
            self.tile_array[int(offset_x // 800 + offset_x // 400 % 2 * 2 - 1)][int(offset_y // 800 + (offset_y // 400 % 2 * 2 - 1))].draw(screen, offset_x-25, offset_y)
            return_group.add(self.tile_array[int(offset_x // 800 + offset_x // 400 % 2 * 2 - 1)][int(offset_y // 800 + (offset_y // 400 % 2 * 2 - 1))].collision_group.sprites())

        return return_group