import pygame as p
import math as m

def loadify(imgname):
    return p.image.load(imgname).convert_alpha()

class Object(p.sprite.Sprite):

    def __init__(self, name, width=50, height=50):
        p.sprite.Sprite.__init__(self)
        self.name = name
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.image = loadify(name)
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = p.Rect(self.x, self.y, self.width, self.height)

    def setX(self, x):
        self.x = x
        self.rect = p.Rect(self.x, self.y, self.width, self.height)

    def setY(self, y):
        self.y = y
        self.rect = p.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, ((self.x-offset_x)+374, (self.y-offset_y)+228))

    def collide(self, sprite):
        #IDEA: multiple collidable groups for map regions
        return p.sprite.collide_rect(self, sprite)


class Movable_Object(Object):

    def __init__(self, name):
        Object.__init__(self, name)

    def moveX(self, x, collidable_group):

        collision = False
        self.x += x
        self.rect = p.Rect(self.x, self.y-30, self.width, self.height)

        for collidable in collidable_group:
            if  collidable != self and self.collide(collidable):
                collision = True
                break

        if collision:
            self.x -= x
            self.rect = p.Rect(self.x, self.y-30, self.width, self.height)

    def moveY(self, y, collidable_group):

        self.y += y
        self.rect = p.Rect(self.x, self.y-30, self.width, self.height)
        collision = False

        for collidable in collidable_group:
            if collidable != self and self.collide(collidable):
                collision = True
                break

        if collision:
            self.y -= y
            self.rect = p.Rect(self.x, self.y-30, self.width, self.height)




class Player(Movable_Object):

    def __init__(self, name, up_walk, down_walk, left_walk, right_walk):
        #check to see if I can just flip left walk for right walk
        Movable_Object.__init__(self, name)
        self.speed = 20
        self.diag_speed = self.speed/m.sqrt(2)
        self.x = 1600
        self.y = 1600
        self.width = 56
        self.height = 127
        self.rect = p.Rect(1600, 1600, 56, 142)
        self.walking_time = 0

        self.up_walk = []
        self.down_walk = []
        self.left_walk = []
        self.right_walk = []

        for name in up_walk:
            self.up_walk.append(p.transform.scale(loadify(name+".png"), (112, 144)))
        for name in down_walk:
            self.down_walk.append(p.transform.scale(loadify(name+".png"), (112, 144)))
        for name in left_walk:
            self.left_walk.append(p.transform.scale(loadify(name+".png"), (112, 142)))
        for name in right_walk:
            self.right_walk.append(p.transform.scale(loadify(name+".png"), (112, 142)))

        self.current_group = self.up_walk


        #doing walking -- specifically i am looking at animating different walking in each if statement by changing self.image. May need to send

    def move(self, keys, collidable_group):

        walk_gap = 30

        if p.key.get_pressed()[100] == keys[97]:
            if keys[115]:
                self.moveY(self.speed,collidable_group)
                self.current_group = self.up_walk
                if self.walking_time % walk_gap:
                    self.image = self.up_walk[self.walking_time//walk_gap % len(self.up_walk)]
            elif keys[119]:
                self.moveY(self.speed*-1,collidable_group)
                self.current_group = self.down_walk
                if self.walking_time % walk_gap:
                    self.image = self.down_walk[self.walking_time//walk_gap % len(self.down_walk)]
        elif keys[115] == keys[119]:
            if keys[100]:
                self.moveX(self.speed,collidable_group)
                self.current_group = self.right_walk
                if self.walking_time % walk_gap:
                    self.image = self.right_walk[self.walking_time//walk_gap % len(self.right_walk)]
            elif keys[97]:
                self.moveX(self.speed*-1,collidable_group)
                self.current_group = self.left_walk
                if self.walking_time % walk_gap:
                    self.image = self.left_walk[self.walking_time//walk_gap % len(self.left_walk)]
        else:
            if keys[100]:
                self.moveX(self.diag_speed,collidable_group)
                self.current_group = self.right_walk
                if self.walking_time % walk_gap:
                    self.image = self.right_walk[self.walking_time//walk_gap % len(self.right_walk)]
            elif keys[97]:
                self.moveX(self.diag_speed*-1,collidable_group)
                self.current_group = self.left_walk
                if self.walking_time % walk_gap:
                    self.image = self.left_walk[self.walking_time//walk_gap % len(self.left_walk)]
            if keys[115]:
                self.moveY(self.diag_speed,collidable_group)
            elif keys[119]:
                self.moveY(self.diag_speed*-1,collidable_group)

        if p.key.get_pressed()[100] == p.key.get_pressed()[97] and not keys[115] and not keys[119]:
            self.walking_time = 0
            self.image = self.current_group[1]
        else:
            self.walking_time += 1

    def draw(self, screen):
        if self.image in self.up_walk:
            screen.blit(self.image, (374, 228))
        elif self.image in self.down_walk:
            screen.blit(self.image, (314, 228))
        elif self.image in self.left_walk:
            screen.blit(self.image, (316, 229))
        elif self.image in self.right_walk:
            screen.blit(self.image, (372, 229))

class Demons(Object):
    def __init__(self, name, x, y, up_walk, down_walk, left_walk, right_walk):
        Object.__init__(self, name)
        self.setX(x)
        self.setY(y)
        self.speed = 5
        self.hit = False
        self.walking_time = 0

        self.up_walk = []
        self.down_walk = []
        self.left_walk = []
        self.right_walk = []

        for name in up_walk:
            self.up_walk.append(p.transform.scale(loadify(name + ".png"), (48, 54)))
        for name in down_walk:
            self.down_walk.append(p.transform.scale(loadify(name + ".png"), (48, 54)))
        for name in left_walk:
            self.left_walk.append(p.transform.scale(loadify(name + ".png"), (48, 54)))
        for name in right_walk:
            self.right_walk.append(p.transform.scale(loadify(name + ".png"), (48, 54)))

        self.current_group = self.up_walk

    def move(self, player):
        chg_x = self.x - player.x
        chg_y = self.y - player.y
        angle = m.atan2(chg_y,chg_x)
        x_move = m.cos(angle) * self.speed
        y_move = m.sin(angle) * self.speed

        walk_gap = 30

        self.y -= y_move
        self.x -= x_move

        self.rect = p.Rect(self.x, self.y - 30, self.width, self.height)

        if x_move > 0 and abs(x_move)> abs(y_move):
            self.current_group = self.left_walk
        elif x_move < 0 and abs(x_move)> abs(y_move):
            self.current_group = self.right_walk
        elif y_move > 0 and abs(y_move) > abs(x_move):
            self.current_group = self.down_walk
        elif y_move < 0 and abs(y_move) > abs(x_move):
            self.current_group = self.up_walk



        if self.walking_time % walk_gap:
            self.image = self.current_group[self.walking_time // walk_gap % len(self.current_group)]

        self.walking_time += 5


        if self.collide(player):
            self.hit = True

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, ((self.x - offset_x) + 374, (self.y - offset_y) + 228))

        #screen.blit(loadify("download.jpg"), (700, 10), (0,0,50,80 ))



