import pygame as p
import Objects

p.init()

def loadify(imgname):
	return p.image.load("images/" + imgname).convert_alpha()

def play_sound(name):
	  sound = p.mixer.Sound("effects/" + name + ".wav")
	  sound.play()

def main(screen):
	background = p.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	back = loadify('controls.png')
	backpos = back.get_rect()
	back = p.transform.scale(back, (800,600))
	backbutton = p.rect.Rect(500, 466, 635, 530)
	screen.blit(background, (0,0))
	p.display.flip()
	running = True
	cursor = p.transform.scale(Objects.loadify("cursor-small-arrow.png").convert_alpha(), (15,15))
	
	while running:
		#print(p.mouse.get_pos())
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
		p.mouse.set_visible(False)
		background.blit(cursor, p.mouse.get_pos())
		screen.blit(background, (0, 0))
		p.display.flip()

if __name__ == "__main__":
	main(p.display.set_mode((800, 600)))