import pygame as p
import Objects
import GameStates as gs
import credits
import score as scr
world = gs.WorldState()

p.init()

def loadify(imgname):
	return p.image.load("images/" + imgname).convert_alpha()

def play_sound(name):
	  sound = p.mixer.Sound("effects/" + name + ".wav")
	  sound.play()

def win_anim(animI):
	back = loadify('victoryscreen-' + str(animI) + '.png')
	animI += 1
	return animI, back

def main(screen, win, score = 0):
	endrunning = True
	clicked = False

	background = p.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	if not win:
		back = loadify('endscreen.png')
	else:
		back = loadify('victoryscreen-1.png')
	backpos = back.get_rect()
	back = p.transform.scale(back, (800,600))
	#backpos.centerx = background.get_rect().centerx
	background.blit(back, backpos)
	
	font = p.font.Font(None, 36)
	t = "SCORE: " + str(score)
	text = font.render(t, 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	textpos = textpos.move(15,200)
	text = p.transform.scale(text, (150,100))
	
	screen.blit(background, (0, 0))
	p.display.flip()

	cursor = p.transform.scale(Objects.loadify("cursor-small-arrow.png").convert_alpha(), (15,15))
	restart_button = p.rect.Rect(535, 285,240, 90)
	score_button = p.rect.Rect(530, 380, 240, 90)
	credit_button = p.rect.Rect(530, 470, 240, 90)

	animI = 1
	
	highscore = world.get_highscore()
	if score > highscore:
		world.set_highscore(score)
		highscore = score

	while endrunning:
		#screen.fill([255, 255, 255])
		#print(p.mouse.get_pos())
		if win:
			if animI < 23:
				animS = win_anim(animI)
				animI = animS[0]
				back = animS[1]
				backpos = back.get_rect()
				back = p.transform.scale(back, (800,600))
			else:
				animI = 1

		clicked = False
		for event in p.event.get():
			if event.type == p.QUIT:
				endrunning = False
				return "quit"
			elif event.type == p.MOUSEBUTTONUP:
				clicked = True
				pos = p.mouse.get_pos()
		key = p.key.get_pressed()
		if key[p.K_ESCAPE]:
			endrunning = False

		if clicked:
			if restart_button.collidepoint(pos):
			# if 530 < p.mouse.get_pos()[0] < 770 and 280 < p.mouse.get_pos()[1] < 360:
				play_sound("Button_Click")
				endrunning = False
				return "restart"
			elif score_button.collidepoint(pos):
			# elif 530 < p.mouse.get_pos()[0] < 770 and 380 < p.mouse.get_pos()[1] < 460:
				#endrunning = False
				#return "score"
				play_sound("Button_Click")
				s = scr.main(screen, score, highscore)
				if s == "quit":
					endrunning = False
					return "quit"
			elif credit_button.collidepoint(pos):
			# elif 530 < p.mouse.get_pos()[0] < 770 and 470 < p.mouse.get_pos()[1] < 560:
				play_sound("Button_Click")
				endrunning = False
				c = credits.main(screen)
				if c == "quit":
					endrunning = False
					return "quit"
				if c == "back":
					endrunning = True
		background.fill((250, 250, 250))
		background.blit(back, backpos)
		p.mouse.set_visible(False)
		if win:
			background.blit(text, textpos)
		background.blit(cursor, p.mouse.get_pos())
		screen.blit(background, (0, 0))
		p.display.flip()
		#startbutton.blit(screen, p.mouse.get_pos())




if __name__ == "__main__":
	main(p.display.set_mode((800, 600)), True, 40)
