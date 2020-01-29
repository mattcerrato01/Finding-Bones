
import pygame as p
import Objects
import GameStates as gs
import credits

p.init()

def loadify(imgname):
    return p.image.load("images/" + imgname).convert_alpha()

def main(screen):
	#print("starting in", screen)
	running = True
	clicked = False
	
	background = p.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	startbutton = loadify("Bones-WalkingRight-Rightfoot.png")
	startbutton = p.transform.scale(startbutton, (100,80))
	startbuttonpos = startbutton.get_rect()
	#print(startbuttonpos)
	startbuttonpos.centerx = background.get_rect().centerx
	startbuttonpos = startbuttonpos.move(0,350)
	#print(startbuttonpos)
	
	font = p.font.Font(None, 36)
	text = font.render("CONTROLS", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	textpos = textpos.move(15,550)
	back = loadify("startscreen.png")
	backpos = back.get_rect()
	back = p.transform.scale(back, (800,600))
	background.blit(back, backpos)
	background.blit(text, textpos)
	background.blit(startbutton, startbuttonpos)
	screen.blit(background, (0, 0))
	p.display.flip()

	cursor = p.transform.scale(loadify("cursor-small-arrow.png").convert_alpha(), (15,15))
	
	while running:
		#screen.fill([255, 255, 255])
		clicked = False
		#print(p.mouse.get_pos())
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
			if 90 < p.mouse.get_pos()[0] < 350 and 445 < p.mouse.get_pos()[1] < 530:
				running = False
			elif 480 < p.mouse.get_pos()[0] < 730 and 445 < p.mouse.get_pos()[1] < 530:
				c = credits.main(screen)
				if c == "quit":
					endrunning = False
					return "quit"
				if c == "back":
					endrunning = True
			elif 350 < p.mouse.get_pos()[0] < 480 and 525 < p.mouse.get_pos()[1] < 575:
				running = False
		background.fill((250, 250, 250))
		background.blit(back, backpos)
		background.blit(text, textpos)
		background.blit(startbutton, startbuttonpos)
		p.mouse.set_visible(False)
		background.blit(cursor, p.mouse.get_pos())
		screen.blit(background, (0, 0))
		p.display.flip()
		#startbutton.blit(screen, p.mouse.get_pos())
		
	
	print("starting main")


if __name__ == "__main__":
	main(p.display.set_mode((800, 600)))
	