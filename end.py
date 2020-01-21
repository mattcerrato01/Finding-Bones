import pygame as p
import Objects

p.init()

def main(screen):
	endrunning = True
	clicked = False
	
	background = p.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	
	font = p.font.Font(None, 36)
	text = font.render("Quit", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	textpos = textpos.move(0,150)
	background.blit(text, textpos)
	
	screen.blit(background, (0, 0))
	p.display.flip()
	
	cursor = p.transform.scale(Objects.loadify("cursor-small-arrow.png").convert_alpha(), (15,15))
	
	while endrunning:
		#screen.fill([255, 255, 255])
		clicked = False
		#print(p.mouse.get_pos())
		for event in p.event.get():
			if event.type == p.QUIT:
				endrunning = False
			elif event.type == p.MOUSEBUTTONUP:
				clicked = True
		key = p.key.get_pressed()
		if key[p.K_ESCAPE]:
			endrunning = False
		
		if 300 < p.mouse.get_pos()[0] < 500 and 140 < p.mouse.get_pos()[1] < 180:
			#print("mouse is over 'newGameButton'")
			if clicked:
				endrunning = False
				return False
		background.fill((250, 250, 250))
		background.blit(text, textpos)
		p.mouse.set_visible(False)
		background.blit(cursor, p.mouse.get_pos())
		screen.blit(background, (0, 0))
		p.display.flip()
		#startbutton.blit(screen, p.mouse.get_pos())
		
	


if __name__ == "__main__":
	main(p.display.set_mode((800, 600)))
	