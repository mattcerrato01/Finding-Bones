import pygame as p
import Objects

p.init()

def loadify(imgname):
	return p.image.load("images/" + imgname).convert_alpha()

def play_sound(name):
	sound = p.mixer.Sound("effects/" + name + ".wav")
	sound.play()

def main(screen):

	back = loadify('controlscreen.png')
	backpos = back.get_rect()
	back = p.transform.scale(back, (800,600))
	backbutton = p.rect.Rect(615, 520, 165, 70)
	back_text = p.font.SysFont("Times New Roman", 20)
	back_texts = back_text.render("Back", True, (255,255,255))
	text_rect = back_texts.get_rect()
	screen.blit(back, (0,0))
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
				print(p.mouse.get_pos())
				clicked = True
		key = p.key.get_pressed()
		if key[p.K_ESCAPE]:
			running = False
		if backbutton.collidepoint(p.mouse.get_pos()) and clicked:
			return "back"
		screen.blit(back, backpos)
		p.mouse.set_visible(False)
		p.draw.rect(screen, (0,0,0),backbutton)
		screen.blit(back_texts, (backbutton.x + backbutton.width/2 - text_rect.width/2, backbutton.y + backbutton.height/2 - text_rect.height/2 ))
		screen.blit(cursor, p.mouse.get_pos())


	p.display.flip()

if __name__ == "__main__":
	main(p.display.set_mode((800, 600)))