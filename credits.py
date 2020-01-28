import pygame as p
import Objects

p.init()

def loadify(imgname):
	return p.image.load("images/" + imgname).convert_alpha()



def main(screen):
	background = p.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	back = loadify('credits.png')
	backpos = back.get_rect()
	back = p.transform.scale(back, (800,600))
	font = p.font.Font(None, 36)
	text = font.render("BACK", 1, (250, 250, 250))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	textpos = textpos.move(0,525)
	background.blit(back, backpos)
	background.blit(text, textpos)
	screen.blit(background, (0,0))
	p.display.flip()
	backbutton = p.rect.Rect(350, 500, 450, 550)
	running = True
	cursor = p.transform.scale(Objects.loadify("cursor-small-arrow.png").convert_alpha(), (15,15))
	
	
	while running:
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
		if backbutton.collidepoint(p.mouse.get_pos()) and clicked:
			return "back"
		background.blit(back, backpos)
		background.blit(text, textpos)
		p.mouse.set_visible(False)
		background.blit(cursor, p.mouse.get_pos())
		screen.blit(background, (0, 0))
		p.display.flip()


if __name__ == "__main__":
	main(p.display.set_mode((800, 600)))