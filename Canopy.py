import pygame as p
import GameStates as gs
coord = gs.CoordConverter()


def loadify(imgname):
    return p.image.load("images/" + imgname)

class Canopy:

    def __init__(self, x, y, w, h):

        self.dimension = 100

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.leaf = Leaf(self.dimension)


    def draw(self, screen):

        for i in range(self.w // self.dimension):
            for j in range(self.h // self.dimension):

                temp_x = self.x + i * self.dimension
                temp_y = self.y + j * self.dimension

                self.leaf.draw(screen, temp_x, temp_y)



class Secret_Canopy(Canopy):

    def __init__(self, x, y, w, h):
        Canopy.__init__(self, x, y, w, h)
        self.discovered = False

    def draw(self, screen):

        if self.x <= coord.real_x(400) <= self.x+self.w and self.y <= coord.real_y(300) <= self.y+self.h:
            self.discovered = True

        if not self.discovered:
            Canopy.draw(self, screen)




class Leaf:

    def __init__(self, dimension):

        self.image = p.transform.scale(loadify("leaf.png"), (dimension, dimension))

    def draw(self, screen, x, y):

        screen.blit(self.image, (coord.screen_x(x), coord.screen_y(y)))