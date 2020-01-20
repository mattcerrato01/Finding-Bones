
import pygame as p
import math as m
import Objects
import Tiles as t
import GameStates as gs
import random
import start as st
import end

coord = gs.CoordConverter()
world = gs.WorldState()
inventory = gs.Inventory()
actions = gs.Actions()
quests = gs.QuestManager(3)

gs.Overworld_State = False
p.init()

screen = p.display.set_mode((800, 600))

p.display.set_caption("Grim Reaper")

quests.advance_quest(1)
#quests.advance_quest(1)


def loadify(imgname):  # Returns loaded Image
    return p.image.load(imgname).convert_alpha()

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
rect = Objects.Object("download.jpg", 100, 100)
rect2 = Objects.Object("download1.jpg")
rect3 = Objects.Object("download2.jpg")
villager = Objects.Villagers([["VillagerMaleFront.png", "VillagerMaleFrontIdle.png"],"VillagerMaleFaceLeft.png", "VillagerMaleFaceRight.png","VillagerMaleBack.png"])
villager.setX(800)
villager.setY(800)
rect.setX(100)
rect.setY(300)
rect2.setX(400)
rect2.setY(400)
rect3.setX(820)
rect3.setY(900)
dialogue_box = Objects.Dialogue_box()

villager_tutorial = Objects.Villagers([["VillagerMaleFront.png", "VillagerMaleFrontIdle.png"],"VillagerMaleFaceLeft.png", "VillagerMaleFaceRight.png","VillagerMaleBack.png"], essential = True)
villager_tutorial.setX(400)
villager_tutorial.setY(200)

villagers = [villager, villager_tutorial]

collidable_group = p.sprite.Group(rect, rect2, rect3, villager, villager_tutorial)

image_name_array = [["background.jpg", "background.jpg", "background.jpg", "background.jpg"],
                    ["background.jpg", "background.jpg", "background.jpg", "background.jpg"],
                    ["background.jpg", "background.jpg", "background.jpg", "background.jpg"],
                    ["background.jpg", "background.jpg", "background.jpg", "background.jpg"], ]

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


time = 0
fate = player.fate
paused = False
ptime = 0
esc_holder = False
mouseChanged = False

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
                    if collidable.perform_action(pos) and not collidable.get_essential: #returns true if villager has been reaped
                        collidable_group.remove(collidable)
                        tile_map = t.Map(image_name_array, collidable_group)
                        player.soul += 10
                        break
                    collidable.update_action()

        key = p.key.get_pressed()
        if key[p.K_i]:
            inventory.draw(screen)	#Draws inventory when holding i

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
                if type(collidable) == Objects.Villagers:
                    if world.state() and not villager.get_soul_reaped():
                        screen.blit(speech_cursor, p.mouse.get_pos())
                        mouseChanged = True
                        break
                    else:
                        if not collidable.get_essential() and not villager.get_soul_reaped():
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
            end.main(screen)
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