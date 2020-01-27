
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
	coord = gs.CoordConverter()
	world = gs.WorldState()
	inventory = gs.Inventory()
	actions = gs.Actions()
	quests = gs.QuestManager()
	sc = Canopy.Secret_Canopy(400, 600 * 3, 800 * 3, 600)
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
	collidables.add( setup.quests() )
	quest_dialogue = setup.quest_dialogue()

	#quest_villager = Objects.Quest_Villager("villager", True, (2,3), 400, 800)

	graveyard = Objects.Graveyard(45,1325)


	cage = Objects.Object_chgs_image("cage-locked-bones.png", "cage-unlocked.png",2875,1420,128,114, """has(key1, key2, key3){print "I'm freed",, "key1" from inv,, "key2" from inv,, "key3" from inv}""", "key1, key2, key3")
	well = Objects.Object_chgs_image("well-with-bucket.png", "well-without-bucket.png", 120, 1830, 108,168,"""hasnt(bucket){"bucket" to inv}""", "")
	dialogue_box = Objects.Dialogue_box()

	villager_tutorial = Objects.Quest_Villager("Harold Alfond Tutorial Villager", "villager", False, [2,3], "", 400, 200, "m")

	collidable_group = p.sprite.Group(villager_tutorial, cage, well)


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
	quest_progress_image = p.transform.scale(loadify("Nametag.png"), (150,160))

	# tile = t.Tile("background.jpg", collidable_group, 0, 0)
	createDemons(demons, player, int(200 / player.fate))
	gs.change_track(4)
	st.main(screen)
	running = True

	font = p.font.Font(None, 36)
	pausetext = font.render("Paused", 1, (250, 250, 250))
	ptextRect = pausetext.get_rect()
	ptextRect.center = (400,300)


	def forced_dialogue(dialogue):
		"""

		:param quest_villager: villager that will be speaking the forced dialogue with death
		:param dialogue: list of strings representing the print action a villager can perform
		:return: running
		"""
		for action in dialogue:
			actions.perform_action(action)


	def run_tutorial(t_stage, villager_tutorial, quest_dialogue):
		#print(t_stage)
		if t_stage == 0:
			t_stage = 1
		elif t_stage == 1:
			forced_dialogue(quest_dialogue[0])
			t_stage = 2
		elif t_stage == 2:
			if len(dialogue_box.dialogue) == 0:
				t_stage = 3
		elif t_stage == 3:
			if p.time.get_ticks() % 1000:
				villager_tutorial.setX(villager_tutorial.getX() + 0.5)
				villager_tutorial.setY(villager_tutorial.getY() + 1)
			if villager_tutorial.getX() == 420:
				t_stage = 4
		elif t_stage == 4:
			forced_dialogue(quest_dialogue[1])
			t_stage = 5
		elif t_stage == 5:
			if not world.state():
				t_stage = 6
		elif t_stage == 6:
			forced_dialogue(quest_dialogue[2])
			t_stage = 7
		elif t_stage == 7:
			if villager_tutorial.get_soul_reaped():
				forced_dialogue(quest_dialogue[3])
				t_stage = 8

		return t_stage


	t_stage = 0
	time = 0
	fate = player.fate
	paused = False
	ptime = 0
	esc_holder = False
	mouseChanged = False
	tutorial_active = True
	piles_of_bones = []
	gs.change_track(1)
	
	#print(forced_dialogue(quest_dialogue))

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
					print(coord.real_x(pos[0]), coord.real_y(pos[1]))
					if dialogue_box.draw(screen):
						play_sound(random.choice(["Greeting 1", "Greeting 2", "Greeting 3 (Female)", "Cough", "BlehSound"])) # FIX THIS SHIT LATER
						dialogue_box.perform_action(pos)
					else:
						for collidable in collision_group:
							if collidable.perform_action(pos):	# returns true if villager has been reaped
								play_sound("Scythe")
								graveyard.add_grave(collidable)
								bones = p.transform.scale(loadify("skull_and_bones.png"), (60, 62))
								piles_of_bones.append([bones, p.time.get_ticks(), collidable.x, collidable.y])

								tomb = graveyard.get_tombstones()[len(graveyard.get_tombstones()) - 1]
								collidable_group.add(tomb)

								tile_map.tile_array[0][2].add_to_group(tomb)
								tile_map.tile_array[int( collidable.x // 800 )][int( collidable.y // 600 )].remove_from_group(collidable)

								#if anyone sees this remind Will to fix that /\

								player.soul += 10
								if player.soul > 100:
									player.soul = 100

								if collidable.isFated():
									player.fate += 10
								else:
									player.fate -= 10

								if player.fate > 100:
									player.fate = 100
							print(collidable.__class__)
							if collidable.__class__ == <class 'Objects.Object_chgs_image'>:
								if collidable.image == "cage-locked-bones.png":
									print("bones")

								break
							collidable.update_action()
			if tutorial_active:
				t_stage = run_tutorial(t_stage, villager_tutorial, quest_dialogue[0])
				if t_stage == 8:
					tutorial_active = False


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
					if fate - player.fate < 0:
						randIDX = random.randint(0, len(demons) - 1)
						demons.remove(demons.sprites()[randIDX])
						i += 1
					elif fate - player.get_fate() > 0:
						createDemons(demons, player, 1)
						i += 1
				fate = player.get_fate()
			if not world.state():
				for demon in demons:
					demon.draw(screen)
			dialogue_box.draw(screen)
			for bone in piles_of_bones:
				screen.blit(bone[0], (coord.screen_x(bone[2]), coord.screen_y(bone[3])))
				if bone[1] + 3000 < p.time.get_ticks():
					piles_of_bones.remove(bone)

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

			if player.fate <= 0 or player.soul <= 0:
				player.fate = 100
				player.soul = 100
				p.mouse.set_visible(True)
				gs.change_track(3)
				endc = end.main(screen, False)
				if endc == "restart":
					gs.reset()
					main()
				elif endc == "score":
					running = False
				elif endc == "credits":
					pass
			if True:
				pass
				#endc = end.main(screen, True, player.get_fate()
			
			time = p.time.get_ticks()
		else:
			pause_screen = pause.Pause()
			button_clicked = ""
			for event in p.event.get():
				if event.type == p.QUIT:
					running = False
				elif event.type == p.MOUSEBUTTONUP:
					pos = p.mouse.get_pos()
					print(pos)
					button_clicked	=  pause_screen.button_clicked(pos)
			key = p.key.get_pressed()
			if key[p.K_ESCAPE] and esc_holder:
				esc_holder = False
				paused = False

			elif not key[p.K_ESCAPE]:
				esc_holder = True
			if button_clicked == "continue":
				paused = False
			elif button_clicked == "restart":
				gs.reset()
				main()


			pause_screen.draw(screen)
			if True:
				screen.blit(cursor, p.mouse.get_pos())
		p.display.update()
if __name__ == "__main__":
	main()

