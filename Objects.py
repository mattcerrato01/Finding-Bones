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

def play_sound(name):
	  sound = p.mixer.Sound("effects/" + name + ".wav")
	  sound.play()

class Object(p.sprite.Sprite):

    def __init__(self, overworld_image_name, x=0, y=0, width=50, height=50, action = """do(1) {to inv "berry"} AND do(1) {print "~You found a berry!~"}  """):  # NOTE: come back and clean up initialization and such here
        p.sprite.Sprite.__init__(self)
        self.fated = False
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

    def isFated(self):
        return self.fated

    def set_action(self, action):
        self.action = action
    def perform_action(self, mouse_click): # returns true if villager has been reaped
        if self.rect.collidepoint(mouse_click):
            self.action = actions.perform_action(self.action)

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

    def __init__(self, overworld_image_name, fated, x, y, male, side_width = 32):
        self.male = male
        if male == "m":
            self.male = "_m"
        elif male == "f":
            self.male = "_f"
        else:
            self.male = ""
        Object.__init__(self, overworld_image_name + "_front" + self.male+".png", 46, 110)

        self.width = 46
        self.height = 110
        self.side_width = side_width


        self.essential = False

        self.setX(x)
        self.setY(y)

        self.fated = fated
        if fated:
            self.underworld_image = loadify("fated_soul.png")
        else:
            self.underworld_image = loadify("unfated_soul.png")


        self.front_image = (p.transform.scale(loadify(overworld_image_name+"_front" + self.male+".png"), (self.width, self.height)))
        self.idle = (p.transform.scale(loadify(overworld_image_name+"_idle" + self.male+".png"), (self.width, self.height)))
        self.left_image = p.transform.scale(loadify(overworld_image_name+"_left" + self.male+".png"), (self.side_width, self.height))
        self.right_image = p.transform.scale(loadify(overworld_image_name+"_right" + self.male+".png"), (self.side_width, self.height))
        self.back_image = p.transform.scale(loadify(overworld_image_name+"_back" + self.male+".png"), (self.width, self.height))
        self.forward_image = self.front_image
        self.current_image = self.back_image


        self.name = names.generate(male)



        self.underworld_image = p.transform.scale(self.underworld_image, (self.width, self.height))
        self.walking_time = 0



        self.dialogues = ["""print “Weird stuff goin on today, amirite?” """,
                          """print “Ya ever try berries and fish?  It tastes great, except for how bad it is.” """,
                          """print "I'm about to try some isometric exercise, care to join me?" """,
                          """print "The wife's makin' stew for supper tonight." """,
                          """print "What kind of diet you doing? You look so skinny." """,
                          """print "Wonderful weather we're having." """,
                          """print "Monarchy? More like Monanarcy, when we overthrowing the government?" """,
                          """print "That king is just, yowza, more like King Thicc" """,
                          """print "I heard the chicken served near the well is fantastic" """,
                          """print "Weather looks terrible today, I hate the sun." """,
                          """print "I want to eat more berries, but I think 700 is enough" """,
                          """print "Loud belch" """,
                          """print "I want to own a cow farm, but all I have is a chicken farm" """,
                          """print "Wonder if we will ever see a dragon?" """,
                          """print "I heard that some guy has started to follow the way of the vampire" """,
                          """print "I wonder where Brad went, I haven't seen him in weeks" """,
                          """print "Can't wait to eat some boiled turnip tonight" """,
                          """print "I heard the carnival is coming here, within a decade" """,
                          """print "I hope Death is doing okay today" """,
                          """print "Hello friend! Need some berries" """,
                          """print "One day, I will eat something other than fish" """,
                          """print "I wish I wish I was a fish """,
                          """print "Best way to ward off demons? Call them demoffs" """,
                          """print "I have heard a rumor about a tree, surrounded by a false wall, that will grant those who touch it something that they truly desire." AND set quest(4,0)""",
                          """has(Iron Key) {print "I like the look of you."} AND hasnt(Iron Key) {print "Well aren’t you the model of what a deity of death should act like! I have a key I pickpocketed off some vampire this morning, I’ll give to you!" ,, to inv "Iron Key"}"""
                          ] #List of dialogue options for normal villager
        idx = r.randint(0,len(self.dialogues)-3)
        self.action = self.dialogues[idx]
        self.font = p.font.SysFont('Papyrus', 20)
        self.nameplate_text = self.font.render(self.name, False, (0, 0, 0))

        temp_x = self.font.size(str(self.name))[0]
        temp_y = self.font.size(str(self.name))[1]

        self.nameplate_image_left = p.transform.scale(loadify("NametagLeft.png"), (6, temp_y))
        self.nameplate_image_right = p.transform.scale(loadify("NametagRight.png"), (6, temp_y))
        self.nameplate_image_mid = p.transform.scale(loadify("NametagMid.png"), (temp_x+4, temp_y))

    #	self.fated

    def perform_action(self, mouse_click):

        if type(self) == Villagers:
            self.update_action()

        if self.rect.collidepoint(mouse_click):

            self.action = actions.perform_action(self.action)

        if self.rect.collidepoint(mouse_click) and (not self.essential or self.grey_right_now) and not world.state():
            self.soul_reaped = True
            return True
        return False

    def update_action(self):

        fate_factor = 3

        if self.fate >= 100:
            fate_factor = 1
        elif self.fate >= 65:
            fate_factor = 2

        idx = r.randint(0,len(self.dialogues)-fate_factor)
        self.action = self.dialogues[idx]


    def draw(self, screen, player):

        self.fate = player.fate

        walk_gap = 100
        distx = (400 - coord.screen_x(self.x+self.width/2))
        disty = (300-coord.screen_y(self.y+self.height/2))
        x_chg = 0
        if world.state():
            dist = m.sqrt(distx**2 + disty**2)
            if dist < 200:
                if abs(distx) > abs(disty):
                    x_chg = (self.width - self.side_width)/2
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

            self.draw_image(screen, self.current_image, x_chg)
        else:
            self.draw_image(screen, self.underworld_image)

    def draw_image(self, screen, image, x_chg = 0):
        screen.blit(image, (coord.screen_x(self.x + x_chg), coord.screen_y(self.y)))
        rect = self.nameplate_text.get_rect()



        screen.blit(self.nameplate_image_left, (coord.screen_x(self.x) + self.width / 2 - self.font.size(self.name)[0] / 2 - 8, coord.screen_y(self.y) + self.height))
        screen.blit(self.nameplate_image_right, (coord.screen_x(self.x) + self.width / 2 + self.font.size(self.name)[0] / 2 + 2, coord.screen_y(self.y) + self.height))
        screen.blit(self.nameplate_image_mid, (coord.screen_x(self.x) + self.width / 2 - self.font.size(self.name)[0] / 2 - 2, coord.screen_y(self.y) + self.height))
        screen.blit(self.nameplate_text, (coord.screen_x(self.x) + self.width / 2 - self.font.size(self.name)[0] / 2 - 2, coord.screen_y(self.y) + self.height))

    def changeMouse(self, mouse):
        if self.rect.collidepoint(mouse):
            return True
        else:
            return False


    def get_soul_reaped(self):
        return self.soul_reaped

class Quest_Villager(Villagers):

    def __init__(self, name, overworld_image_name, fated, quest_array, action, x, y, male, grey = False, secret = False):
        Villagers.__init__(self, overworld_image_name, fated, x, y, male)
        self.name = name

        temp_x = self.font.size(str(self.name))[0]
        temp_y = self.font.size(str(self.name))[1]
        self.secret = secret

        self.nameplate_text = self.font.render(self.name, False, (0, 0, 0))
        self.nameplate_image_left = p.transform.scale(loadify("NametagLeft.png"), (6, temp_y))
        self.nameplate_image_right = p.transform.scale(loadify("NametagRight.png"), (6, temp_y))
        self.nameplate_image_mid = p.transform.scale(loadify("NametagMid.png"), (temp_x + 4, temp_y))

        self.essential = True
        self.action = action
        self.quest_action = action
        self.grey = grey
        self.grey_right_now = False
        self.quest = quest_array[0]
        self.quest_end = int( quest_array[len(quest_array)-1] )
        self.quest_array = quest_array[1:]

        self.question_mark = p.transform.scale(loadify("question_mark.png"), (16, 24))
        if grey:
            self.grey_soul = p.transform.scale(loadify("grey_soul.png"), (self.width, self.height))
        self.essential_soul = p.transform.scale(loadify("essential_soul.png"), (self.width, self.height))
        self.fated_soul = p.transform.scale(loadify("fated_soul.png"), (self.width, self.height))
        self.unfated_soul = p.transform.scale(loadify("unfated_soul.png"), (self.width, self.height))
    def update_action(self):
        if qm.quest_stage(self.quest) not in self.quest_array:
            idx = r.randint(0,len(self.dialogues)-1)
            self.action = self.dialogues[idx]
        elif qm.quest_stage(self.quest) in self.quest_array:
            self.action = self.quest_action
            if self.grey:
                self.grey_right_now = True
    def set_essential(self,essential):
        self.essential = essential
    def draw(self, screen, player):
        self.update_action()

        try:
            stage = qm.quests[self.quest]
        except:
            stage = -1

        if stage > self.quest_end:
            self.essential = False

        if world.state():
            Villagers.draw(self, screen, player)


            if qm.quest_stage(self.quest) in self.quest_array and not self.secret:
                screen.blit(self.question_mark, (coord.screen_x(self.x)+self.width/2-8, coord.screen_y(self.y)-30))
        elif "Tutorial" in self.name and qm.quest_stage(0) == 4:
            self.draw_image(screen, self.unfated_soul)

        elif self.grey and qm.quest_stage(self.quest) in self.quest_array:
            self.draw_image(screen, self.grey_soul)
        elif stage <= self.quest_end and not self.secret:
            self.draw_image(screen, self.essential_soul)
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
        coord.set_offset_y(self.y +228)

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

        self.speed = 2	# Change to 20 when testing
        self.diag_speed = self.speed / m.sqrt(2)
        coord.set_offset_x(374)
        coord.set_offset_y(228)


        self.x = coord.real_x(250)
        self.y = coord.real_y(0)

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
        self.image = self.current_group[1]

        self.empty_hourglass = p.transform.scale(loadify("Empty_Hourglass.png"), (50, 80))
        self.fate_hourglass_bottom = p.transform.scale(loadify("Fate_Hourglass_Bottom.png"), (50, 80))
        self.fate_hourglass_top = p.transform.scale(loadify("Fate_Hourglass_Top.png"), (50, 80))
        self.soul_hourglass_bottom = p.transform.scale(loadify("Soul_Hourglass_Bottom.png"), (50, 80))
        self.soul_hourglass_top = p.transform.scale(loadify("Soul_Hourglass_Top.png"), (50, 80))
        self.exclamation = p.transform.scale(loadify("exclamation.png"), (20, 56))

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
            play_sound("Footsteps")



        if p.key.get_pressed()[9] and self.tab_holder:
            collide = False
            play_sound("Teleport")
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
                if world.state():
                    gs.change_track(1)
                else:
                    gs.change_track(2)
                self.soul -= 4
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
        else:
            screen.blit(self.image, (374, 228))

        screen.blit(self.empty_hourglass, (10, 510), (0, 0, 50, 80))
        screen.blit(self.fate_hourglass_top, (10, 544 - 30 * (self.fate / 100)),
                    (0, 34 - 30 * (self.fate / 100), 50, 34))
        screen.blit(self.fate_hourglass_bottom, (10, 556 + 30 * (self.fate / 100)),
                    (0, 46 + 30 * (self.fate / 100), 50, 76))

        screen.blit(self.empty_hourglass, (740, 510), (0, 0, 50, 80))
        screen.blit(self.soul_hourglass_top, (740, 548 - 30 * (self.soul / 100)),
                    (0, 38 - 30 * (self.soul / 100), 50, 34))
        screen.blit(self.soul_hourglass_bottom, (740, 556 + 30 * (self.soul / 100)),
                    (0, 46 + 30 * (self.soul / 100), 50, 76))

        if self.soul <= 50:
            screen.blit(self.exclamation, (755, 450))
        if self.fate <= 50:
            screen.blit(self.exclamation, (25, 450))



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
        chg_y = self.y - (abs(player.y) + 3*player.height/4)
        hyp = m.sqrt(chg_x ** 2 + chg_y ** 2)
        # angle = m.atan2(chg_y, chg_x)
        x_move = (chg_x * self.speed) / hyp	 # m.cos(angle) * self.speed
        y_move = (chg_y * self.speed) / hyp	 # m.sin(angle) * self.speed

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

    def set_dialogue(self, dialogue):
        self.dialogue = dialogue

    def perform_action(self, mouse):
        if mouse:
            for i in range(4):
                try:
                    actions.dialogue_list.pop(0)
                except:
                    break
            self.dialogue = actions.dialogue_list

    def draw(self, screen):
        self.dialogue = actions.dialogue_list
        if len(self.dialogue)>0:
            screen.blit(self.box_1, (100,25))
            screen.blit(self.box_2,(400,25))
            dialogues_shown = 4
            if len(self.dialogue)<4:
                dialogues_shown = len(self.dialogue)
            for i in range(dialogues_shown):
                dialogue_box = self.dialogue_box_font.render(self.dialogue[i], True, (0, 0, 0))
                screen.blit(dialogue_box,(120,35 + 20*i))
            return True
        return False

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
        Object.__init__(self,	overworld_image_name="graveyard-tombstone.png", x= x,y= y)
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
        self.drawn = True

    def changeMouse(self, mouse):

        return self.rect.collidepoint(mouse) and self.action != "" and world.state()

    def perform_action(self, mouse_click):
        if self.rect.collidepoint(mouse_click) and world.state():
            self.action = actions.perform_action(self.action)
        return False

    def update_action(self):
        self.action = self.action

    def update(self):
        self.rect = p.Rect(coord.screen_x(self.x), coord.screen_y(self.y), self.width, self.height)

class Object_chgs_image(Object):
    def __init__(self, start_image_name, end_image_name, x, y, width, height, action, conditional, name = "bones"):
        Object.__init__(self, start_image_name, x, y, width, height, action)
        self.start_image = p.transform.scale(loadify(start_image_name), (self.width, self.height))
        self.end_image = p.transform.scale(loadify(end_image_name), (self.width, self.height))
        self.conditional = conditional
        self.image = self.start_image
        self.start_image_name = start_image_name
        self.end_image_name = end_image_name
        self.name = name

    def get_image_name(self):
        if self.image == self.start_image:
            return self.start_image_name
        else:
            return self.end_image_name

    def chg_image(self):

        if self.image == self.start_image:
            self.image = self.end_image
        elif self.image == self.end_image:
            self.image = self.start_image


    def perform_action(self, mouse_click):
        if self.rect.collidepoint(mouse_click) and world.state():
            conditionals = self.conditional.split(", ")
            condition_met = True
            keys = 0
            for conditional in conditionals:
                if inventory.has(conditional) and "Key" in conditional:
                    keys += 1
                elif not inventory.has(conditional):
                    condition_met = False

            if condition_met or self.conditional == "" or keys >= 4:
                self.chg_image()
                if "Key" in self.conditional:
                    return True

            self.action = actions.perform_action(self.action)
            if self.conditional == "" or self.conditional == "bucket":
                self.chg_action()
    def chg_action(self):
        if self.image == self.end_image:
            self.action = """has(bucket){ "bucket" from inv}"""
            self.conditional = "bucket"
        elif self.image == self.start_image:
            self.action = """hasnt(bucket){"bucket" to inv}"""
            self.conditional = ""
        return False








