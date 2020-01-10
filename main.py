import pygame as p
import math as m
import Objects
import Tiles as t
import GameStates as gs
import random

coord = gs.CoordConverter()


p.init()

screen = p.display.set_mode((800, 600))


p.display.set_caption("Grim Reaper")


def loadify(imgname): #Returns loaded Image
    return p.image.load(imgname).convert_alpha()



player = Objects.Player("player.jpg", ["GR-F-L","GR-F-S","GR-F-R","GR-F-S"], ["GR-B-L","GR-B-S","GR-B-R","GR-B-S"], ["GR-L-1","GR-L-S","GR-L-1","GR-L-2"], ["GR-R-1","GR-R-S","GR-R-1","GR-R-2"])
rect = Objects.Object("download.jpg",100,100)
rect2 = Objects.Object("download1.jpg")
rect3 = Objects.Object("download2.jpg")
rect.setX(100)
rect.setY(300)
rect2.setX(400)
rect2.setY(400)
rect3.setX(820)
rect3.setY(900)




collidable_group = p.sprite.Group(rect, rect2, rect3)

image_name_array = [["background.jpg","background.jpg","background.jpg","background.jpg"],
                    ["background.jpg","background.jpg","background.jpg","background.jpg"],
                    ["background.jpg","background.jpg","background.jpg","background.jpg"],
                    ["background.jpg","background.jpg","background.jpg","background.jpg"],]

tile_map = t.Map(image_name_array, collidable_group)
demons = p.sprite.Group()
#tile = t.Tile("background.jpg", collidable_group, 0, 0)
for i in range(int(200/player.fate)):
    randomx = random.randint(0, 800*len(image_name_array[0]))
    randomy = random.randint(0,600*len(image_name_array))
    collided = False

    demon = Objects.Demons("player.jpg", randomx, randomy, ["M-F-L", "M-F-S", "M-F-R"],["M-B-L", "M-B-S", "M-B-R"],["M-L-L", "M-L-S", "M-L-R"],["M-R-L", "M-R-S", "M-R-R"])
    for boys in demons:
        if demon.collide(boys):
            collided = True
            i -= 1
            break
    if not collided:
        demons.add(demon)



running = True

time = 0

while running:


    screen.fill([255, 255, 255])



    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    collision_group = tile_map.draw(screen)
    for x in range(p.time.get_ticks()//10 - time//10):
        player.move(p.key.get_pressed(), collision_group)
        for demon in demons:
            demon.move(player)
            if demon.hit:
                demons.remove(demon)
                # player.fate -= 10 # This will decrease player's fate when a demon hits it

    for demon in demons:
        demon.draw(screen)

    player.draw(screen)

    p.display.update()

    time = p.time.get_ticks()