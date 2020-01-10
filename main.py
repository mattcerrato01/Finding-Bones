import pygame as p
import math as m
import Objects
import Tiles as t

#HI
#blah
p.init()

screen = p.display.set_mode((800, 600))


p.display.set_caption("Grim Reaper")


def loadify(imgname): #Returns loaded Image
    return p.image.load(imgname).convert_alpha()



player = Objects.Player("player.jpg", ["GR-F-L","GR-F-S","GR-F-R","GR-F-S"], ["GR-B-L","GR-B-S","GR-B-R","GR-B-S"], ["GR-L-1","GR-L-S","GR-L-1","GR-L-2"], ["GR-R-1","GR-R-S","GR-R-1","GR-R-2"])
rect = Objects.Object("download.jpg",100,100)
rect2 = Objects.Object("download1.jpg")
rect3 = Objects.Object("download2.jpg")

demon = Objects.Demons("demon.png", 100,100, ["M-F-L", "M-F-S", "M-F-R"],["M-B-L", "M-B-S", "M-B-R"],["M-L-L", "M-L-S", "M-L-R"],["M-R-L", "M-R-S", "M-R-R"])
demons = p.sprite.Group(demon)
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
#tile = t.Tile("background.jpg", collidable_group, 0, 0)




running = True

time = 0

while running:


    screen.fill([255, 255, 255])



    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    collision_group = tile_map.draw(screen, player.x, player.y)
    for x in range(p.time.get_ticks()//10 - time//10):
        player.move(p.key.get_pressed(), collision_group)
        for demon in demons:
            demon.move(player)
            if demon.hit:
                demons.remove(demon)
                # player.fate -= 10 # This will decrease player's fate when a demon hits it



    for demon in demons:
        demon.draw(screen, player.x, player.y)


    player.draw(screen)
    p.display.update()

    time = p.time.get_ticks()