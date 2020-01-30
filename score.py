import pygame as p
import Objects
import GameStates as gs

p.init()

def loadify(imgname):
	return p.image.load("images/" + imgname).convert_alpha()

def play_sound(name):
	  sound = p.mixer.Sound("effects/" + name + ".wav")
	  sound.play()

def main(screen, score, highscore):
	print(score)
	if score > highscore:
		gs.set_highscore(score)
	background = p.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	back = loadify('leaf.png')
	backpos = back.get_rect()
	back = p.transform.scale(back, (800,600))
	font = p.font.Font(None, 36)
	
	btext = font.render("BACK", 1, (250, 250, 250))
	btextpos = btext.get_rect()
	btextpos.centerx = background.get_rect().centerx
	btextpos = btextpos.move(0,525)
	
	topt = font.render("YOUR SCORE WAS: " + str(score), 1, (250, 250, 250))
	toptpos = topt.get_rect()
	toptpos.centerx = background.get_rect().centerx
	toptpos = toptpos.move(0,150)
	topt = p.transform.scale(topt, (300,100))
	
	midt = font.render("THE HIGH SCORE IS: " + str(highscore), 1, (250, 250, 250))
	midtpos = midt.get_rect()
	midtpos.centerx = background.get_rect().centerx
	midtpos = midtpos.move(0,350)
	midt = p.transform.scale(midt, (300,100))
	
	background.blit(back, backpos)
	background.blit(btext, btextpos)
	background.blit(topt, toptpos)
	background.blit(midt, midtpos)
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
		background.blit(btext, btextpos)
		background.blit(topt, toptpos)
		background.blit(midt, midtpos)
		p.mouse.set_visible(False)
		background.blit(cursor, p.mouse.get_pos())
		screen.blit(background, (0, 0))
		p.display.flip()


if __name__ == "__main__":
	main(p.display.set_mode((800, 600)), 10, 90)