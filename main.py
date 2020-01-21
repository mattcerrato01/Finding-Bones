
import pygame as p
import math as m
import Objects
import Tiles as t
import GameStates as gs
import random
import start as st
import end
import Setup



coord = gs.CoordConverter()
world = gs.WorldState()
inventory = gs.Inventory()
actions = gs.Actions()
quests = gs.QuestManager()

gs.Overworld_State = False
p.init()

screen = p.display.set_mode((800, 600))

p.display.set_caption("Grim Reaper")


quests.add_number_quests(3)

quests.advance_quest(1)
#quests.advance_quest(1)


def loadify(imgname):
    return p.image.load("images/" + imgname).convert_alpha()

'''Function that adds a set number of demons to a group of sprites, takes in a group of sprites, a player object, and
the amount of demons to be added to the group'''
def createDemons(demons, player, numDemons):
    for i in range(numDemons):
        randomx = random.randint(0, 800 * len(image_name_array[0]))
        randomy = random.randint(0, 600 * len(image_name_array))
        collided = False

        demon = Objects.Demons("M-F-L.png", randomx, randomy, ["M-F-L", "M-F-S", "M-F-R"], ["M-B-L", "M-B-S", "M-B-R"],
                               ["M-L-L", "M-L-S", "M-L-R"], ["M-R-L", "M-R-S", "M-R-R"], player)
        for boys in demons:
            if demon.collide(boys):
                collided = True
                i -= 1
                break
        if not collided:
            demons.add(demon)


player = Objects.Player("player.jpg", ["GR-F-L", "GR-F-S", "GR-F-R", "GR-F-S"],
                        ["GR-B-L", "GR-B-S", "GR-B-R", "GR-B-S"], ["GR-L-1", "GR-L-S", "GR-L-1", "GR-L-2"],
                        ["GR-R-1", "GR-R-S", "GR-R-1", "GR-R-2"])
# rect = Objects.Object("download.jpg", 100, 100)
rect2 = Objects.Object("download1.jpg")
rect3 = Objects.Object("download2.jpg")

setup = Setup.Setup()
collidables = setup.collidables()
print(collidables)

quest_villager = Objects.Quest_Villager("villager", True, (2,3), 400, 800)

graveyard = Objects.Graveyard(75,1325)

# rect.setX(100)
# rect.setY(300)
rect2.setX(400)
rect2.setY(400)
rect3.setX(820)
rect3.setY(900)
cage = Objects.Cage()
cage.setX(1200)
cage.setY(1200)
dialogue_box = Objects.Dialogue_box()

villager_tutorial = Objects.Quest_Villager("villager", True, (2,3), 400, 200)

collidable_group = p.sprite.Group( rect2, rect3, villager_tutorial, quest_villager, cage)
for i in range(5):
    villager = Objects.Villagers("villager", False, 500 + 100*i, 500 + 100*i)
    collidable_group.add(villager)
for collidable in collidables:
    collidable_group.add(collidable)

for tombstone in graveyard.get_tombstones():
    collidable_group.add(tombstone)
image_name_array = [["tile1.png", "tile5.png", "tile9.png", "tile13.png"],
                    ["tile2.png", "tile6.png", "tile10.png", "tile14.png"],
                    ["tile3.png", "tile7.png", "tile11.png", "tile15.png"],
                    ["tile4.png", "tile8.png", "tile12.png", "tile16.png"]]

tile_map = t.Map(image_name_array, collidable_group)
demons = p.sprite.Group()

# cursors:
p.mouse.set_visible(False)
cursor = p.transform.scale(loadify("cursor-small-arrow.png"), (15,15))
investigation_cursor = p.transform.scale(loadify("cursor-small-magnifyingglass.png"), (15,15))
scythe_cursor = p.transform.scale(loadify("cursor-small-scythe.png"), (15,15))
speech_cursor = p.transform.scale(loadify("cursor-small-speechbubble.png"), (15,15))



# tile = t.Tile("background.jpg", collidable_group, 0, 0)
createDemons(demons,player,int(200 / player.fate))
st.main(screen)
running = True

font = p.font.Font(None, 36)
pausetext = font.render("Paused", 1, (250, 250, 250))
ptextRect = pausetext.get_rect()
ptextRect.center = (400,300)

t_stage = 0
def run_tutorial():
    print("tutorial running")


time = 0
fate = player.fate
paused = False
ptime = 0
esc_holder = False
mouseChanged = False
tutorial_active = False

while running:

    if not paused:
        screen.fill([255, 255, 255])
        collision_group = tile_map.draw(screen, player)
        clicked = False

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONUP:

                pos = p.mouse.get_pos()

                for collidable in collision_group:
                    if collidable.perform_action(pos): #returns true if villager has been reaped
                        graveyard.add_grave(collidable)
                        collidable_group.add(graveyard.get_tombstones()[len(graveyard.get_tombstones())-1])
                        collidable_group.remove(collidable)
                        tile_map = t.Map(image_name_array, collidable_group)
                        player.soul += 10
                        break
                    collidable.update_action()
        if tutorial_active:
            run_tutorial()

        key = p.key.get_pressed()
        if key[p.K_i]:
            inventory.draw(screen)	#Draws inventory when holding i

        if key[p.K_p]:
            pass

        if key[p.K_ESCAPE] and esc_holder:
            esc_holder = False
            paused = True

        elif not key[p.K_ESCAPE]:
            esc_holder = True

        for x in range(p.time.get_ticks() // 10 - time // 10):
            player.move(p.key.get_pressed(), collision_group, demons)
            if not world.state():
                for demon in demons:
                    demon.move(player)
                    if demon.hit:
                        demons.remove(demon)
                        player.set_fate(player.get_fate()-10)
        # adding or subtracting demons when player's fate goes down
        if abs(fate - player.get_fate()) >= 5:
            i = 0
            while i < abs(fate - player.get_fate()) // 5:
                if fate - player.fate < 0:
                    randIDX = random.randint(0,len(demons)-1)
                    demons.remove(demons[randIDX])
                    i += 1
                elif fate - player.get_fate() > 0:
                    createDemons(demons,player,1)
                    i += 1
            fate = player.get_fate()
        if not world.state():
            for demon in demons:
                demon.draw(screen)

        dialogue_box.draw(screen)

        player.draw(screen)
        mouseChanged = False
        for collidable in collision_group:
            if collidable.changeMouse(p.mouse.get_pos()):
                if type(collidable) == Objects.Villagers or type(collidable)==Objects.Quest_Villager:
                    if world.state():
                        screen.blit(speech_cursor, p.mouse.get_pos())
                        mouseChanged = True
                        break
                    else:
                        if not type(collidable) == Objects.Quest_Villager:
                            screen.blit(scythe_cursor, p.mouse.get_pos())
                            mouseChanged = True
                            break
                else:
                    screen.blit(investigation_cursor, p.mouse.get_pos())
                    mouseChanged = True
                    break

        if not mouseChanged:
            screen.blit(cursor, p.mouse.get_pos())

        if player.fate <= 0 or player.soul <= 0:
            player.fate = 100
            player.soul = 100
            p.mouse.set_visible(True)
            if not end.main(screen):
                running = False
        time = p.time.get_ticks()
    else:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        key = p.key.get_pressed()
        if key[p.K_ESCAPE] and esc_holder:
            esc_holder = False
            paused = False

        elif not key[p.K_ESCAPE]:
            esc_holder = True
        #print(ptime)
        p.draw.rect(screen,(0,0,0),p.Rect(250,200,300,200))
        screen.blit(pausetext, ptextRect)


    p.display.update()
