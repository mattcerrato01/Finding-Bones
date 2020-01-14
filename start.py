
import pygame as p
import Objects

p.init()

def main(screen):
	#print("starting in", screen)
	running = True
	
	background = p.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	startbutton = p.image.load("VillagerMaleFront.png")
	startbutton = p.transform.scale(startbutton, (100,80))
	startbuttonpos = startbutton.get_rect()
	print(startbuttonpos)
	startbuttonpos.centerx = background.get_rect().centerx
	startbuttonpos = startbuttonpos.move(0,300)
	print(startbuttonpos)
	
	font = p.font.Font(None, 36)
	text = font.render("Press Esc to Start", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	textpos = textpos.move(0,150)
	background.blit(text, textpos)
	background.blit(startbutton, startbuttonpos)
	screen.blit(background, (0, 0))
	p.display.flip()

	
	while running:
		#screen.fill([255, 255, 255])
		
		print(p.mouse.get_pos())
		for event in p.event.get():
			if event.type == p.QUIT:
				running = False
		key = p.key.get_pressed()
		if key[p.K_ESCAPE]:
			running = False
		
		if startbutton.get_rect().collidepoint(p.mouse.get_pos()):
   			print("mouse is over 'newGameButton'")

		screen.blit(background, (0, 0))
		p.display.flip()
		#startbutton.blit(screen, p.mouse.get_pos())
	
	print("starting main")


if __name__ == "__main__":
	main(p.display.set_mode((800, 600)))
	