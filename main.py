
import pygame as p
import math as m
import Objects
import Tiles as t
import GameStates as gs
import random
import start as st

coord = gs.CoordConverter()
world = gs.WorldState()

gs.Overworld_State = False
p.init()

screen = p.display.set_mode((800, 600))

p.display.set_caption("Grim Reaper")




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
villager = Objects.Villagers("VillagerMaleFront.png")
villager.setX(800)
villager.setY(800)
rect.setX(100)
rect.setY(300)
rect2.setX(400)
rect2.setY(400)
rect3.setX(820)
rect3.setY(900)
dialogue_box = Objects.Dialogue_box()


villagers = [villager]

collidable_group = p.sprite.Group(rect, rect2, rect3, villager)

image_name_array = [["background.jpg", "background.jpg", "background.jpg", "background.jpg"],
                    ["background.jpg", "background.jpg", "background.jpg", "background.jpg"],
                    ["background.jpg", "background.jpg", "background.jpg", "background.jpg"],
                    ["background.jpg", "background.jpg", "background.jpg", "background.jpg"], ]

tile_map = t.Map(image_name_array, collidable_group)
demons = p.sprite.Group()

cc1 = p.image.load("VillagerMaleFront.png")
cc2 = p.image.load("VillagerMaleFront_underworld.png")


# tile = t.Tile("background.jpg", collidable_group, 0, 0)
createDemons(demons,player,int(200 / player.fate))
st.main(screen)
running = True

time = 0
fate = player.fate
dialogue_box_undraw_event = p.USEREVENT+1 #Event that will essentially undraw the text box of an object
while running:

    screen.fill([255, 255, 255])
    collision_group = tile_map.draw(screen)
    clicked = False

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONUP:
            clicked = True
            pos = p.mouse.get_pos()
        elif event.type == dialogue_box_undraw_event:
            dialogue_box.pop_dialogue()

    if clicked:

        for collidable in collision_group:
            if collidable.check_if_investigated(pos):
                if world.state():
                    dialogue_box.add_dialogue(collidable.get_investigation_pieces()[0])
                    p.time.set_timer(dialogue_box_undraw_event,3000)
                    if len(collidable.get_objects_to_inventory()) > 0:
                        player.append_to_inventory(collidable.get_objects_to_inventory()[0])
                        collidable.pop_objects_to_inventory()
                if type(collidable) == Objects.Villagers:
                    if collidable.get_soul_reaped():
                        collidable_group.remove(collidable)
                        tile_map = t.Map(image_name_array, collidable_group)
                        player.soul-=10
                break
        print(player.inventory)
        clicked = False

    for x in range(p.time.get_ticks() // 10 - time // 10):
        player.move(p.key.get_pressed(), collision_group)
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

    for villager in villagers:
        if villager.changeMouse(p.mouse.get_pos()):
            if world.state() and not villager.get_soul_reaped():
                p.mouse.set_visible(False)
                screen.blit(cc1, p.mouse.get_pos())
            else:
                if not villager.get_essential() and not villager.get_soul_reaped():
                    p.mouse.set_visible(False)
                    screen.blit(cc2, p.mouse.get_pos())
        else:
            p.mouse.set_cursor(*p.cursors.arrow)
            p.mouse.set_visible(True)


    p.display.update()

    time = p.time.get_ticks()
