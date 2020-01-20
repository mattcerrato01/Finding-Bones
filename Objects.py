# Test
import pygame as p
import math as m
import GameStates as gs
import random as r

coord = gs.CoordConverter()
world = gs.WorldState()
names = gs.NameGenerator()
inventory = gs.Inventory()
actions = gs.Actions()
qm = gs.QuestManager()


def loadify(imgname):
    return p.image.load(imgname).convert_alpha()


class Object(p.sprite.Sprite):

    def __init__(self, overworld_image_name, width=50, height=50, villager = False):  # NOTE: come back and clean up initialization and such here
        p.sprite.Sprite.__init__(self)
        self.soul_reaped = False
        self.action = """do(2) {print 'Hello there!'} AND do(2:3) {print 'go away now'} AND has(berry) {print 'Im a big berry man'}"""
        self.overworld_image_name = overworld_image_name
        if not villager:
            self.underworld_image_name = overworld_image_name[:-4] + "_underworld" + overworld_image_name[-4:]
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.image = loadify(overworld_image_name)
        #		self.underworld_image = loadify(self.underworld_image_name)
        # self.underworld_image = p.transform.scale(self.image, (self.width, self.height))
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.update()

    def perform_action(self, mouse_click): # returns true if villager has been reaped
        if self.rect.collidepoint(mouse_click):

            self.action = actions.perform_action(self.action)

            if type(self) == Villagers and not world.state():
                self.soul_reaped = False
                return True
        return False
    def update_action(self):
        return self.action
    def changeMouse(self, mouse):
        if self.rect.collidepoint(mouse):
            return True
        else:
            return False
    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x
        self.update()

    def setY(self, y):
        self.y = y
        self.update()

    def draw(self, screen, player = None):
        if world.state():
            screen.blit(self.image, (coord.screen_x(self.x), coord.screen_y(self.y)))
        else:
            screen.blit(self.image, (coord.screen_x(self.x), coord.screen_y(self.y)))

    def update(self):
        self.rect = p.Rect(coord.screen_x(self.x), coord.screen_y(self.y), self.width, self.height)

    def collide(self, sprite):
        return p.sprite.collide_rect(self, sprite)


class Villagers(Object):

    def __init__(self, overworld_image_name, fated, essential=False, male = True):
        Object.__init__(self, overworld_image_name[3], 46, 110, villager=True)
        self.fated = fated
        self.underworld_image_name = "VillagerMaleFront_underworld.png"
        self.image = (p.transform.scale(loadify(overworld_image_name[0][0]), (self.width, self.height)))
        self.idle = (p.transform.scale(loadify(overworld_image_name[0][1]), (self.width, self.height)))

        self.left_image = p.transform.scale(loadify(overworld_image_name[1]), (self.width, self.height))
        self.right_image = p.transform.scale(loadify(overworld_image_name[2]), (self.width, self.height))
        self.back_image = p.transform.scale(loadify(overworld_image_name[3]), (self.width, self.height))
        self.current_image = self.back_image
        self.current_image = p.transform.scale(self.current_image, (self.width,self.height))

        self.forward_image = self.image

        name = names.generate(male)


        self.underworld_image = loadify(self.underworld_image_name)
        self.underworld_image = p.transform.scale(self.underworld_image, (self.width, self.height))
        self.essential = essential
        self.walking_time = 0
        self.dialogues = ["""print 'Woah nice costume'""", """print 'its a little early for halloween though isnt it'"""
            , """print 'Hello There'""", """print 'Im not sure about this scotty'""", """print 'Dewit'"""] #List of dialogue options for normal villagers
        idx = r.randint(0,len(self.dialogues)-1)
        self.action = self.dialogues[idx]
        font = p.font.SysFont('Times New Romans', 16)
        self.nameplate = font.render(name, False, (0, 0, 0), (255,255,255))
    #   self.fated

    def update_action(self):
        idx = r.randint(0,len(self.dialogues)-1)
        self.action = self.dialogues[idx]
    def get_essential(self):
        return self.essential

    def draw(self, screen, player):
        walk_gap = 100 #aklsdjf
        distx = (400 - coord.screen_x(self.x+self.width/2))
        disty = (300-coord.screen_y(self.y+self.height/2))
        if world.state():
            dist = m.sqrt(distx**2 + disty**2)
            if dist < 200:
                if abs(distx) > abs(disty):
                    if distx>=0:
                        self.current_image = self.right_image
                    elif distx<0:
                        self.current_image = self.left_image
                elif abs(distx) < abs(disty):
                    if disty<=0:
                        self.current_image = self.back_image
                    elif disty>0:
                        if self.walking_time % walk_gap == 0:
                            if r.randint(0,6) == 1:
                                self.forward_image = self.idle
                            else:
                                self.forward_image = self.image
                        self.current_image = self.forward_image
            else:
                if self.walking_time % walk_gap == 0:
                    if r.randint(0, 6) == 1:
                        self.forward_image = self.idle
                    else:
                        self.forward_image = self.image
                self.current_image = self.forward_image
            self.walking_time +=1

            self.draw_image(screen, self.current_image)
        else:
            self.draw_image(screen, self.underworld_image)

    def draw_image(self, screen, image):
        screen.blit(image, (coord.screen_x(self.x), coord.screen_y(self.y)))
        rect = self.nameplate.get_rect()
        screen.blit(self.nameplate, (coord.screen_x(self.x) + self.width / 2 - rect.width / 2, coord.screen_y(self.y) + self.height))



    def get_soul_reaped(self):
        return self.soul_reaped

class Quest_Villager(Villagers):

    def __init__(self, overworld_image_name, fated, quest_end, male=True, grey = False):
        Villagers.__init__(self, overworld_image_name, fated, True, male)
        print(str(self.essential) + str(quest_end))
        self.grey = grey
        self.quest_end = quest_end
        if grey:
            self.grey_soul = p.transform.scale(loadify("grey_soul.png"), (self.width, self.height))
        self.essential_soul = p.transform.scale(loadify("essential_soul.png"), (self.width, self.height))
        self.fated_soul = p.transform.scale(loadify("fated_soul.png"), (self.width, self.height))
        self.unfated_soul = p.transform.scale(loadify("unfated_soul.png"), (self.width, self.height))

    def draw(self, screen, player):

        print( str(self.essential) + " " + str(qm.quests[self.quest_end[0]]) + " " + str(self.quest_end[1])  )

        if world.state():
            Villagers.draw(self, screen, player)
        elif self.essential and qm.quests[self.quest_end[0]] < self.quest_end[1]:
            self.draw_image(screen, self.essential_soul)
        elif self.grey and qm.quests[3]>4:
            self.draw_image(screen, self.grey_soul)
        elif self.fated:
            self.draw_image(screen, self.fated_soul)
        else:
            self.draw_image(screen, self.unfated_soul)




class Movable_Object(Object):

    def __init__(self, overworld_image_name):
        Object.__init__(self, overworld_image_name)

    def moveX(self, x, collidable_group):

        self.x += x
        coord.set_offset_x(self.x + 374)
        if world.state():
            for collidable in collidable_group:
                collidable.update()
                if collidable != self and self.collide(collidable):
                    self.x -= x
                    coord.set_offset_x(self.x + 374)
                    break
        else:
            for collidable in collidable_group:
                collidable.update()

    def moveY(self, y, collidable_group):

        self.y += y
        coord.set_offset_y(self.y + 228)

        if world.state():
            for collidable in collidable_group:
                collidable.update()
                if collidable != self and self.collide(collidable):
                    self.y -= y
                    coord.set_offset_y(self.y + 228)
                    collidable.update()
                    break
        else:
            for collidable in collidable_group:
                collidable.update()


class Player(Movable_Object):

    def __init__(self, name, up_walk, down_walk, left_walk, right_walk, ):
        # check to see if we can just flip left walk for right walk
        Movable_Object.__init__(self, name)

        self.speed = 2  # Change to 20 when testing
        self.diag_speed = self.speed / m.sqrt(2)

        coord.set_offset_x(374)
        coord.set_offset_y(228)

        self.x = coord.real_x(374)
        self.y = coord.real_y(228)
        self.width = 40
        self.height = 127  # check this, should be collision height
        self.rect = p.Rect(380, 244, self.width, self.height)
        self.walking_time = 0

        self.tab_ = True

        self.up_walk = []
        self.down_walk = []
        self.left_walk = []
        self.right_walk = []

        for name in up_walk:
            self.up_walk.append(p.transform.scale(loadify(name + ".png"), (112, 144)))
        for name in down_walk:
            self.down_walk.append(p.transform.scale(loadify(name + ".png"), (112, 144)))
        for name in left_walk:
            self.left_walk.append(p.transform.scale(loadify(name + ".png"), (112, 142)))
        for name in right_walk:
            self.right_walk.append(p.transform.scale(loadify(name + ".png"), (112, 142)))

        self.current_group = self.up_walk

        self.empty_hourglass = p.transform.scale(loadify("Empty_Hourglass.png"), (50, 80))
        self.fate_hourglass_bottom = p.transform.scale(loadify("Fate_Hourglass_Bottom.png"), (50, 80))
        self.fate_hourglass_top = p.transform.scale(loadify("Fate_Hourglass_Top.png"), (50, 80))
        self.soul_hourglass_bottom = p.transform.scale(loadify("Soul_Hourglass_Bottom.png"), (50, 80))
        self.soul_hourglass_top = p.transform.scale(loadify("Soul_Hourglass_Top.png"), (50, 80))

        self.fate = 100
        self.soul = 100


    def get_fate(self):
        return self.fate

    def set_fate(self, fate):
        self.fate = fate

    def get_soul(self):
        return self.soul

    def set_soul(self, soul):
        self.soul = soul
    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def move(self, keys, collidable_group, demon_group):

        temp_speed = self.speed
        temp_diag_speed = self.diag_speed
        soul_drain = .01
        animation_speed = 1

        if keys[304]:
            temp_speed *= 2
            temp_diag_speed *= 2
            soul_drain *= 2
            animation_speed = 2

        walk_gap = 30

        if keys[100] == keys[97]:
            if keys[115] and self.y > -2250:
                self.moveY(temp_speed * -1, collidable_group)
                self.current_group = self.up_walk
                if self.walking_time % walk_gap:
                    self.image = self.up_walk[self.walking_time // walk_gap % len(self.up_walk)]
            elif keys[119] and self.y < 0:
                self.moveY(temp_speed, collidable_group)
                self.current_group = self.down_walk
                if self.walking_time % walk_gap:
                    self.image = self.down_walk[self.walking_time // walk_gap % len(self.down_walk)]
        elif keys[115] == keys[119]:
            if keys[100] and self.x > - 3150:
                self.moveX(temp_speed * -1, collidable_group)
                self.current_group = self.right_walk
                if self.walking_time % walk_gap:
                    self.image = self.right_walk[self.walking_time // walk_gap % len(self.right_walk)]
            elif keys[97] and self.x < 0:
                self.moveX(temp_speed, collidable_group)
                self.current_group = self.left_walk
                if self.walking_time % walk_gap:
                    self.image = self.left_walk[self.walking_time // walk_gap % len(self.left_walk)]
        else:
            if keys[100] and self.x > -3150:
                self.moveX(temp_diag_speed * -1, collidable_group)
                self.current_group = self.right_walk
                if self.walking_time % walk_gap:
                    self.image = self.right_walk[self.walking_time // walk_gap % len(self.right_walk)]
            elif keys[97] and self.x < 0:
                self.moveX(temp_diag_speed, collidable_group)
                self.current_group = self.left_walk
                if self.walking_time % walk_gap:
                    self.image = self.left_walk[self.walking_time // walk_gap % len(self.left_walk)]
            if keys[115] and self.y > -2250:
                self.moveY(temp_diag_speed * -1, collidable_group)
            elif keys[119] and self.y < 0:
                self.moveY(temp_diag_speed, collidable_group)

        if keys[100] == keys[97] and not keys[115] and not keys[119]:
            self.walking_time = 0
            self.image = self.current_group[1]
        else:
            self.walking_time += animation_speed
            self.soul -= soul_drain

        coord.set_offset_x(self.x + 374)
        coord.set_offset_y(self.y + 228)

        if p.key.get_pressed()[9] and self.tab_holder:
            collide = False
            for collidable in collidable_group:
                collidable.update()
                if collidable != self and self.collide(collidable):
                    collide = True
                    break
            for demon in demon_group:
                demon.update()
                if self.collide(demon):
                    demon.setX(demon.getX() + 200)
                    demon.setY(demon.getY() + 200)
                    break
            if not collide:
                world.toggle()
                self.soul -= 10
                self.tab_holder = False

        elif not p.key.get_pressed()[9]:
            self.tab_holder = True

    def draw(self, screen, player = 0):
        if self.image in self.up_walk:
            screen.blit(self.image, (374, 228))
        elif self.image in self.down_walk:
            screen.blit(self.image, (314, 228))
        elif self.image in self.left_walk:
            screen.blit(self.image, (316, 229))
        elif self.image in self.right_walk:
            screen.blit(self.image, (372, 229))

        screen.blit(self.empty_hourglass, (10, 510), (0, 0, 50, 80))
        screen.blit(self.fate_hourglass_top, (10, 544 - 30 * (self.fate / 100)),
                    (0, 34 - 30 * (self.fate / 100), 50, 34))
        screen.blit(self.fate_hourglass_bottom, (10, 556 + 30 * (self.fate / 100)),
                    (0, 46 + 30 * (self.fate / 100), 50, 76))

        screen.blit(self.empty_hourglass, (740, 510), (0, 0, 50, 80))
        screen.blit(self.soul_hourglass_top, (740, 544 - 30 * (self.soul / 100)),
                    (0, 38 - 30 * (self.soul / 100), 50, 34))
        screen.blit(self.soul_hourglass_bottom, (740, 556 + 30 * (self.soul / 100)),
                    (0, 46 + 30 * (self.soul / 100), 50, 76))


class Demons(Object):

    def __init__(self, name, x, y, up_walk, down_walk, left_walk, right_walk, player):
        Object.__init__(self, name)
        self.setX(x)
        self.setY(y)
        self.speed = 2 - player.fate / 100 * 1.5
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
        chg_x = self.x + player.x
        chg_y = self.y + player.y
        hyp = m.sqrt(chg_x ** 2 + chg_y ** 2)
        # angle = m.atan2(chg_y, chg_x)
        x_move = (chg_x * self.speed) / hyp  # m.cos(angle) * self.speed
        y_move = (chg_y * self.speed) / hyp  # m.sin(angle) * self.speed

        walk_gap = 30

        self.y -= y_move
        self.x -= x_move

        self.update()

        if x_move > 0 and abs(x_move) > abs(y_move):
            self.current_group = self.left_walk
        elif x_move < 0 and abs(x_move) > abs(y_move):
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

    def draw(self, screen, player = None):
        screen.blit(self.image, (coord.screen_x(self.x), coord.screen_y(self.y)))

class Dialogue_box():

    def draw(self, screen):
        if actions.update_dialogue_box():
            dialogue = actions.dialogue_list
            p.draw.rect(screen,(0,0,0), (100,25, 600, 100))
            dialogue_box_font = p.font.SysFont("papyrus", 20)

            while len(dialogue) > 4:
                dialogue.pop(0)

            for i in range(len(dialogue)):
                dialogue_box = dialogue_box_font.render(dialogue[i][0], True, (255, 255, 255))
                screen.blit(dialogue_box,(120,30 + 20*i))
