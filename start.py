
import pygame as p
import Objects
import GameStates as gs
import credits
import controls

p.init()

def loadify(imgname):
    return p.image.load("images/" + imgname).convert_alpha()

def play_sound(name):
	  sound = p.mixer.Sound("effects/" + name + ".wav")
	  sound.play()

def main(screen):
	running = True
	clicked = False
	
	background = p.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	startbutton = loadify("Bones-WalkingRight-Rightfoot.png")
	startbutton = p.transform.scale(startbutton, (100,80))
	startbuttonpos = startbutton.get_rect()
	startbuttonpos.centerx = background.get_rect().centerx
	startbuttonpos = startbuttonpos.move(0,350)

	font = p.font.Font(None, 36)
	text = font.render("CONTROLS", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	textpos = textpos.move(15,550)
	back = loadify("startscreen.png")
	backpos = back.get_rect()
	back = p.transform.scale(back, (800,600))
	background.blit(back, backpos)
	#background.blit(text, textpos)
	background.blit(startbutton, startbuttonpos)
	screen.blit(background, (0, 0))
	p.display.flip()

	cursor = p.transform.scale(loadify("cursor-small-arrow.png").convert_alpha(), (15,15))
	
	while running:
		#screen.fill([255, 255, 255])
		clicked = False
		for event in p.event.get():
			if event.type == p.QUIT:
				running = False
				return "quit"
			elif event.type == p.MOUSEBUTTONUP:
				clicked = True
		key = p.key.get_pressed()
		if key[p.K_ESCAPE]:
			running = False
			return "quit"
		
		if clicked:
			if 35 < p.mouse.get_pos()[0] < 250 and 445 < p.mouse.get_pos()[1] < 530:
				play_sound("Button_Click")
				running = False
			elif 550 < p.mouse.get_pos()[0] < 765 and 445 < p.mouse.get_pos()[1] < 530:
				play_sound("Button_Click")
				c = credits.main(screen)
				if c == "quit":
					running = False
					return "quit"
				if c == "back":
					running = True
			elif 290 < p.mouse.get_pos()[0] < 505 and 445 < p.mouse.get_pos()[1] < 530:
				play_sound("Button_Click")
				o = controls.main(screen)
				if o == "quit":
					running = False
					return "quit"
				elif o == "back":
					running = True
					
		background.fill((250, 250, 250))
		background.blit(back, backpos)
		#background.blit(text, textpos)
		background.blit(startbutton, startbuttonpos)
		p.mouse.set_visible(False)
		background.blit(cursor, p.mouse.get_pos())
		screen.blit(background, (0, 0))
		p.display.flip()
		#startbutton.blit(screen, p.mouse.get_pos())
		
	


if __name__ == "__main__":
	main(p.display.set_mode((800, 600)))
	