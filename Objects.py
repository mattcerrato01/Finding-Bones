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
    return p.image.load("images/" + imgname).convert_alpha()


class Object(p.sprite.Sprite):

    def __init__(self, overworld_image_name, x=0, y=0, width=50, height=50, action = """has(berry) {print "I'm a big berry man"} AND do(2) {to inv "berry", print "Take your berry you bastard"} AND do(2:3) {print "go away now"}  """):  # NOTE: come back and clean up initialization and such here
        p.sprite.Sprite.__init__(self)
        self.soul_reaped = False
        self.action = action
        self.overworld_image_name = overworld_image_name

        try:
            self.underworld_image_name = overworld_image_name[:-4] + "_underworld" + overworld_image_name[-4:]
            self.underworld_image = p.transform.scale(loadify(self.underworld_image_name), (self.width, self.height))
        except:
            aldkfj = 0

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = loadify(overworld_image_name)

        # self.underworld_image = p.transform.scale(self.image, (self.width, self.height))
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.update()

    def perform_action(self, mouse_click): # returns true if villager has been reaped
        if self.rect.collidepoint(mouse_click) and world.state():

            self.action = actions.perform_action(self.action)

        elif self.rect.collidepoint(mouse_click) and type(self) == Villagers and not world.state():
            self.soul_reaped = False
            return True
        return False
    def update_action(self):
        return self.action
    def changeMouse(self, mouse):
        if self.rect.collidepoint(mouse) and world.state():
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

    def __init__(self, overworld_image_name, fated, x, y, male = True):
        self.male = male
        if male:
            Object.__init__(self, overworld_image_name + "_front_m.png", 46, 110)
        else:
            Object.__init__(self, overworld_image_name + "_front_f.png", 46, 110)
        self.width = 46
        self.height = 110

        self.setX(x)
        self.setY(y)

        self.fated = fated
        if fated:
            self.underworld_image = loadify("fated_soul.png")
        else:
            self.underworld_image = loadify("unfated_soul.png")

        if male:
            self.front_image = (p.transform.scale(loadify(overworld_image_name+"_front_m.png"), (self.width, self.height)))
            self.idle = (p.transform.scale(loadify(overworld_image_name+"_idle_m.png"), (self.width, self.height)))
            self.left_image = p.transform.scale(loadify(overworld_image_name+"_left_m.png"), (self.width, self.height))
            self.right_image = p.transform.scale(loadify(overworld_image_name+"_right_m.png"), (self.width, self.height))
            self.back_image = p.transform.scale(loadify(overworld_image_name+"_back_m.png"), (self.width, self.height))
        else:
            self.front_image = (p.transform.scale(loadify(overworld_image_name + "_front_f.png"), (self.width, self.height)))
            self.idle = (p.transform.scale(loadify(overworld_image_name + "_idle_f.png"), (self.width, self.height)))
            self.left_image = p.transform.scale(loadify(overworld_image_name + "_left_f.png"), (self.width, self.height))
            self.right_image = p.transform.scale(loadify(overworld_image_name + "_right_f.png"), (self.width, self.height))
            self.back_image = p.transform.scale(loadify(overworld_image_name + "_back_f.png"), (self.width, self.height))
        self.forward_image = self.front_image
        self.current_image = self.back_image


        self.name = names.generate(male)



        self.underworld_image = p.transform.scale(self.underworld_image, (self.width, self.height))
        self.walking_time = 0



        self.dialogues = ["""print “Weird stuff goin on today, amirite?” """,
                          """print “Ya ever try berries and fish?  It tastes great, except for how bad it is.” """,
                          """print "I"m about to try some isometric exercise, care to join me?" """,
                          """print "The wife"s makin" stew for supper tonight." """,
                          """print "What kind of diet you doing? You look so skinny." """,
                          """print "Wonderful weather we"re having." """,
                          """print "Monarchy? More like Monanarcy, when we overthrowing the government?" """,
                          """print "That king is just, yowza, more like King Thicc" """,
                          """print "I heard the chicken served near the well is fantastic" """,
                          """print "Weather looks terrible today, I hate the sun." """,
                          """print "I want to eat more berries, but I think 700 is enough" """,
                          """print "Loud belch" """,
                          """print "I want to own a cow farm, but all I have is a chicken farm" """,
                          """print "Wonder if we will ever see a dragon?" """,
                          """print "I heard that some guy has started to follow the way of the vampire" """,
                          """print "I wonder where Brad went, I haven"t seen him in weeks" """,
                          """print "Can"t wait to eat some boiled turnip tonight" """,
                          """print "I heard the carnival is coming here, within a decade" """,
                          """print "I hope Death is doing okay today" """,
                          """print "Hello friend! Need some berries" """,
                          """print "One day, I will eat something other than fish" """,
                          """print "I wish I wish I was a fish """,
                          """print "Best way to ward off demons? Call them demoffs" """] #List of dialogue options for normal villager
        idx = r.randint(0,len(self.dialogues)-1)
        self.action = self.dialogues[idx]
        font = p.font.SysFont('Times New Romans', 16)
        self.nameplate = font.render(self.name, False, (0, 0, 0), (255,255,255))
    #   self.fated

    def update_action(self):
        idx = r.randint(0,len(self.dialogues)-1)
        self.action = self.dialogues[idx]


    def draw(self, screen, player):
        walk_gap = 100
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
                                self.forward_image = self.front_image
                        self.current_image = self.forward_image
            else:
                if self.walking_time % walk_gap == 0:
                    if r.randint(0, 6) == 1:
                        self.forward_image = self.idle
                    else:
                        self.forward_image = self.front_image
                self.current_image = self.forward_image
            self.walking_time +=1

            self.draw_image(screen, self.current_image)
        else:
            self.draw_image(screen, self.underworld_image)

    def draw_image(self, screen, image):
        screen.blit(image, (coord.screen_x(self.x), coord.screen_y(self.y)))
        rect = self.nameplate.get_rect()
        screen.blit(self.nameplate, (coord.screen_x(self.x) + self.width / 2 - rect.width / 2, coord.screen_y(self.y) + self.height))
    def changeMouse(self, mouse):
        if self.rect.collidepoint(mouse):
            return True
        else:
            return False


    def get_soul_reaped(self):
        return self.soul_reaped

class Quest_Villager(Villagers):

    def __init__(self, overworld_image_name, fated, quest_end, x, y, male = True, grey = False):
        Villagers.__init__(self, overworld_image_name, fated, x, y, male)
        # print(str(self.essential) + str(quest_end))
        self.grey = grey
        self.quest_end = quest_end

        self.question_mark = p.transform.scale(loadify("question_mark.png"), (16, 24))
        if grey:
            self.grey_soul = p.transform.scale(loadify("grey_soul.png"), (self.width, self.height))
        self.essential_soul = p.transform.scale(loadify("essential_soul.png"), (self.width, self.height))
        self.fated_soul = p.transform.scale(loadify("fated_soul.png"), (self.width, self.height))
        self.unfated_soul = p.transform.scale(loadify("unfated_soul.png"), (self.width, self.height))

    def draw(self, screen, player):

        if world.state():
            Villagers.draw(self, screen, player)
            screen.blit(self.question_mark, (coord.screen_x(self.x)+self.width/2-8, coord.screen_y(self.y)-30))
        elif qm.quests[self.quest_end[0]] < self.quest_end[1]:
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

        coord.set_offset_x(300)
        coord.set_offset_y(600)

        self.x = coord.real_x(374-225)
        self.y = coord.real_y(228)
        self.width = 40
        self.height = 127  # check this, should be collision height
        self.rect = p.Rect(380, 244 + 3*self.height/4, self.width, self.height/4)
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

    def __init__(self):
        self.box_1 = p.transform.scale(loadify("dialoguebox-1.png"), (300, 100))
        self.box_2 = p.transform.scale(loadify("dialoguebox-2.png"), (300, 100))
        self.dialogue = actions.dialogue_list
        self.dialogue_box_font = p.font.SysFont("papyrus", 20)

    def draw(self, screen):
        if actions.update_dialogue_box():


            screen.blit(self.box_1, (100,25))
            screen.blit(self.box_2,(400,25))

            while len(self.dialogue) > 4:
                self.dialogue.pop(0)

            for i in range(len(self.dialogue)):
                dialogue_box = self.dialogue_box_font.render(self.dialogue[i][0], True, (255, 255, 255))
                screen.blit(dialogue_box,(120,35 + 20*i))

class Tombstone(Object):
    def __init__(self, overworld_image_name = "graveyard-tombstone.png", name = ""):
        Object.__init__(self, overworld_image_name, width=103,height=110)
        self.name = name

    def set_name(self, name):
        self.name = name

    def draw(self, screen, player = None):
        screen.blit(self.image, (coord.screen_x(self.x), coord.screen_y(self.y)))
        grave_font = p.font.SysFont("papyrus", 20)
        grave_name = grave_font.render(self.name, True, (0,0,0))
        grave_rect = grave_name.get_rect()
        screen.blit(grave_name, (coord.screen_x(self.x) + self.width/2 - grave_rect.width/2, coord.screen_y(self.y) + self.height/2))

class Graveyard(Object):

    def __init__(self, x = 200, y= 0):
        Object.__init__(self,   overworld_image_name="graveyard-tombstone.png", x= x,y= y)
        self.dead_people = []
        self.tombstones = []
        self.visible_tombstones = []
        y_of_grave = self.y
        x_of_grave = self.x
        for i in range(9):
            tombstone = Tombstone()
            if i % 3 == 0 and i>0:
                x_of_grave = self.x
                y_of_grave += 175

            tombstone.setX(x_of_grave)
            tombstone.setY(y_of_grave)
            self.tombstones.append(tombstone)
            x_of_grave += 125

    def add_grave(self, villager):

        self.dead_people.append(villager)
        if len(self.dead_people) > 9:
            self.dead_people.pop(0)
            self.visible_tombstones.pop(0)
        for i in range(len(self.dead_people)):
            self.tombstones[i].set_name(self.dead_people[i].name)

        self.visible_tombstones.append(self.tombstones[len(self.dead_people)-1])

    def get_tombstones(self):
        return self.visible_tombstones[:]

class Hitbox(p.sprite.Sprite):
    def __init__(self, x, y, width, height, action = ""):
        p.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.drawn = False
        self.rect = p.Rect(coord.screen_x(self.x), coord.screen_y(self.y), self.width, self.height)

    def draw(self, screen, player):
        p.draw.rect(screen, (0,0,0), (coord.screen_x(self.x), coord.screen_y(self.y), self.width, self.height), 2 )
        self.drawn = True

    def changeMouse(self, mouse):
        return self.rect.collidepoint(mouse) and self.action != "" and world.state()

    def perform_action(self, mouse_click):
        if self.rect.collidepoint(mouse_click) and world.state():
            self.action = actions.perform_action(self.action)
        return False

    def update_action(self):
        return self.action
    def update(self):
        self.rect = p.Rect(coord.screen_x(self.x), coord.screen_y(self.y), self.width, self.height)

class Object_chgs_image(Object):
    def __init__(self, start_image_name, end_image_name, x, y, width, height, action, conditional):
        Object.__init__(self, start_image_name, x, y, width, height, action)
        self.start_image = p.transform.scale(loadify(start_image_name), (self.width, self.height))
        self.end_image = p.transform.scale(loadify(end_image_name), (self.width, self.height))
        self.conditional = conditional
        self.image = self.start_image

    def chg_image(self):

        if self.image == self.start_image:
            print("chged image")
            self.image = self.end_image
        elif self.image == self.end_image:
            print("chged image")
            self.image = self.start_image

    def perform_action(self, mouse_click):
        if self.rect.collidepoint(mouse_click) and world.state():
            if inventory.has(self.conditional) > 0 or self.conditional == "":
                print("will change image")
                self.chg_image()

            self.action = actions.perform_action(self.action)
            if self.conditional == "" or self.conditional == "bucket":
                self.chg_action()
            print(inventory.inventory)
    def chg_action(self):
        if self.image == self.end_image:
            self.action = """has(bucket){ "bucket" from inv"""
            self.conditional = "bucket"
        elif self.image == self.start_image:
            self.action = """hasnt(bucket){"bucket" to inv}"""
            self.conditional = ""
        return False


#         Well's width is 108, height is 168






