
import pygame as p
import math as m
import Objects
import Tiles as t
import GameStates as gs
import random
import start as st
import end
import pause
import Setup
import Canopy
import os

def play_sound(name):
      sound = p.mixer.Sound("effects/" + name + ".wav")
      sound.play()
def loadify(imgname):
    return p.image.load("images/" + imgname).convert_alpha()

def main():
    start_time = p.time.get_ticks()
    pause_counter = 0
    coord = gs.CoordConverter()
    world = gs.WorldState()
    inventory = gs.Inventory()
    actions = gs.Actions()
    quests = gs.QuestManager()
    sc = Canopy.Secret_Canopy(800, 1800, 800 * 3, 600)
    sc1 = Canopy.Canopy(-400, -300, 400, 600 * 5)
    sc2 = Canopy.Canopy(0, -300, 800 * 4, 300)
    sc3 = Canopy.Canopy(800 * 4, -300, 400, 600 * 5)
    sc4 = Canopy.Canopy(0, 600 * 4, 800 * 4, 300)


    gs.Overworld_State = False
    p.init()


    screen = p.display.set_mode((800, 600))

    p.display.set_caption("Grim Reaper")



    #quests.advance_quest(1)

    def play_sound(name):
      sound = p.mixer.Sound("effects/" + name + ".wav")
      sound.play()







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


    setup = Setup.Setup()
    collidables = setup.collidables()
    q_vills = setup.quests()
    villager_tutorial = q_vills.sprites()[0]
    collidables.add(q_vills)


    graveyard = Objects.Graveyard(40,1325)


    cage = Objects.Object_chgs_image("cage-locked-bones.png", "cage-unlocked.png",2875,1420,128,114, """has(Iron Key, Gem Key, Silver Key, Onyx Key, Gold Key){print "I'm freed",, "Iron Key" from inv,, "Gem Key" from inv,, "Silver Key" from inv,, "Onyx Key" from inv,, "Gold Key" from inv} AND print"Death: Oh no Bones, I'll key you out of there I just need to get the keys to your cage, I'll come back for you " """, "Iron Key, Gem Key, Gold Key, Onyx Key, Silver Key")
    well = Objects.Object_chgs_image("well-with-bucket.png", "well-without-bucket.png", 120, 1830, 108,168,"""hasnt(bucket){"bucket" to inv}""", "")
    dialogue_box = Objects.Dialogue_box()


    collidable_group = p.sprite.Group( cage, well)


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
    cursor = p.transform.scale(loadify("cursor-small-arrow.png"), (15, 15))
    investigation_cursor = p.transform.scale(loadify("cursor-small-magnifyingglass.png"), (15, 15))
    scythe_cursor = p.transform.scale(loadify("cursor-small-scythe.png"), (15, 15))
    speech_cursor = p.transform.scale(loadify("cursor-small-speechbubble.png"), (15, 15))
    inventory_image = p.transform.scale(loadify("Nametag.png"), (150,150))
    quest_progress_image = p.transform.scale(loadify("quest_plate.png"), (360,500))

    # tile = t.Tile("background.jpg", collidable_group, 0, 0)
    createDemons(demons, player, int(200 / player.fate))
    gs.change_track(4)
    running = True
    str = st.main(screen)
    if str == "quit":
        running = False

    font = p.font.Font(None, 36)
    pausetext = font.render("Paused", 1, (250, 250, 250))
    ptextRect = pausetext.get_rect()
    ptextRect.center = (400,300)
    can_do_action = True


    def run_tutorial(villager_tutorial, mouse_click = (0,0)):


        if quests.quest_stage(0) == -1:
            quests.set_quest(0,0)
        if quests.quest_stage(0) == 1:
            if p.time.get_ticks() % 1000:
                villager_tutorial.setX(villager_tutorial.getX() + 0.5)
                villager_tutorial.setY(villager_tutorial.getY() + 1)
            if villager_tutorial.getX() == 420:
                quests.set_quest(0, 2)
        elif quests.quest_stage(0) == 3:
            if not world.state():
                actions.set_uwa(True)
                quests.set_quest(0, 4)
                villager_tutorial.set_essential(False)
        elif quests.quest_stage(0) == 4:
            if not world.state() and villager_tutorial.rect.collidepoint(mouse_click):
                quests.set_quest(0, 5)
                player.set_fate(player.get_fate()-10)
                tile_map.tile_array[int( villager_tutorial.x // 800 )][int( villager_tutorial.y // 600 )].remove_from_group(villager_tutorial)
        elif quests.quest_stage(0) == 6:
                actions.set_uwa(False)
                return False
        return True


    time = 0
    fate = player.get_fate()
    paused = False
    esc_holder = False
    tutorial_active = True
    piles_of_bones = []
    gs.change_track(1)
    win = False


    #player.move(p.key.get_pressed(),collidable_group,demons)
    player.moveX(0, collidable_group)
    player.moveY(0, collidable_group)

    while running:


        if not paused:
            screen.fill([255, 255, 255])
            collision_group = tile_map.draw(screen, player)

            sc.draw(screen)
            sc1.draw(screen)
            sc2.draw(screen)
            sc3.draw(screen)
            sc4.draw(screen)

            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                elif event.type == p.MOUSEBUTTONUP:

                    pos = p.mouse.get_pos()
                    if quests.quest_stage(0) == 4:
                        run_tutorial(villager_tutorial, pos)


                    if dialogue_box.draw(screen):
                        play_sound(random.choice(["Greeting 1", "Greeting 2", "Greeting 3 (Female)", "Cough", "BlehSound"])) # FIX THIS SHIT LATER
                        dialogue_box.perform_action(pos)
                    else:
                        for sprite in collision_group:

                            if quests.quest_stage(0)!= 4 and sprite.perform_action(pos):	# returns true if villager has been reaped
                                if sprite.image == "cage-locked-bones.png":
                                    win = True
                                play_sound("Scythe")
                                graveyard.add_grave(sprite)
                                bones = p.transform.scale(loadify("skull_and_bones.png"), (60, 62))
                                piles_of_bones.append([bones, p.time.get_ticks(), sprite.x, sprite.y])

                                tomb = graveyard.get_tombstones()[len(graveyard.get_tombstones()) - 1]
                                collidable_group.add(tomb)

                                tile_map.tile_array[0][2].add_to_group(tomb)
                                tile_map.tile_array[int( sprite.x // 800 )][int( sprite.y // 600 )].remove_from_group(sprite)

                                #if anyone sees this remind Will to fix that /\

                                player.soul += 10
                                if player.soul > 100:
                                    player.soul = 100

                                if sprite.isFated():
                                    player.set_fate(player.get_fate()+10)
                                else:
                                    player.set_fate(player.get_fate()-10)

                                if player.fate > 100:
                                    player.set_fate(100)
                                if sprite.__class__ == Objects.Object_chgs_image:
                                    if sprite.get_image_name() == "cage-unlocked.png":
                                        win = True
                                        end_time = p.time.get_ticks()

                                break
                            sprite.update_action()
            if tutorial_active:
                tutorial_active = run_tutorial(villager_tutorial)


            key = p.key.get_pressed()
            if key[p.K_i]:
                inventory.draw(screen, inventory_image)	 # Draws inventory when holding i
            elif key[p.K_q]:
                quests.draw(screen, quest_progress_image)

            elif key[p.K_p]:
                if tutorial_active:
                    actions.set_dialogue([])
                tutorial_active = False

            elif key[p.K_ESCAPE] and esc_holder:
                esc_holder = False
                paused = True
                pause_time = p.time.get_ticks()


            elif not key[p.K_ESCAPE]:
                esc_holder = True

            if not dialogue_box.draw(screen):
                for x in range(p.time.get_ticks() // 10 - time // 10):
                    player.move(p.key.get_pressed(), collision_group, demons)
                    if not world.state():
                        for demon in demons:
                            demon.move(player)
                            if demon.hit:
                                demons.remove(demon)
                                player.set_fate(player.get_fate() - 10)
            # adding or subtracting demons when player's fate goes down
            if abs(fate - player.get_fate()) >= 5:
                i = 0
                while i < abs(fate - player.get_fate()) // 5:
                    if fate - player.get_fate() < 0:
                        try:
                            randIDX = random.randint(0, len(demons)-1)
                            demons.remove(demons.sprites()[randIDX])
                        except:
                            pass
                        i += 1
                    elif fate - player.get_fate() > 0:
                        createDemons(demons, player, 1)
                        i += 1
                fate = player.get_fate()
            if not world.state():
                for demon in demons:
                    demon.draw(screen)

            for bone in piles_of_bones:
                screen.blit(bone[0], (coord.screen_x(bone[2]), coord.screen_y(bone[3])))
                if bone[1] + 3000 < p.time.get_ticks():
                    piles_of_bones.remove(bone)

            dialogue_box.draw(screen)



            player.draw(screen)

            mouseChanged = False
            for collidable in collision_group:
                if collidable.changeMouse(p.mouse.get_pos()):
                    if type(collidable) == Objects.Villagers or type(collidable) == Objects.Quest_Villager:
                        if world.state():
                            screen.blit(speech_cursor, p.mouse.get_pos())
                            mouseChanged = True
                            break
                        else:
                            screen.blit(scythe_cursor, p.mouse.get_pos())
                            mouseChanged = True
                            break
                    else:
                        screen.blit(investigation_cursor, p.mouse.get_pos())
                        mouseChanged = True
                        break

            if not mouseChanged:
                screen.blit(cursor, p.mouse.get_pos())

            endc = ""
            if player.fate <= 0 or player.soul <= 0:
                player.set_fate(100)
                player.set_soul(100)
                p.mouse.set_visible(True)
                gs.change_track(3)
                endc = end.main(screen, False)
                end_time = p.time.get_ticks()

            if win:
                player.set_fate(100)
                player.set_soul(100)
                p.mouse.set_visible(True)
                endc = end.main(screen, True, end_time-start_time - pause_counter)
            if endc == "restart":
                gs.reset()
                main()
            elif endc == "score":
                running = False
            elif endc == "quit":
                running = False

            time = p.time.get_ticks()
        else:

            pause_screen = pause.Pause()
            button_clicked = ""
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                elif event.type == p.MOUSEBUTTONUP:
                    pos = p.mouse.get_pos()
                    button_clicked	=  pause_screen.button_clicked(pos)
            key = p.key.get_pressed()
            if key[p.K_ESCAPE] and esc_holder:
                esc_holder = False
                paused = False
                end_pause_time = p.time.get_ticks()
                pause_counter += (end_pause_time-pause_time)


            elif not key[p.K_ESCAPE]:
                esc_holder = True
            if button_clicked == "continue":
                paused = False
                end_pause_time = p.time.get_ticks()
                pause_counter += (end_pause_time-pause_time)
            elif button_clicked == "restart":
                gs.reset()
                main()


            pause_screen.draw(screen)
            if True:
                screen.blit(cursor, p.mouse.get_pos())
        p.display.update()
if __name__ == "__main__":
    main()

