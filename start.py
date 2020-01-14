
import pygame as p
import Objects


def main(screen):
	#print("starting in", screen)
	running = True
	startbutton = p.image.load("VillagerMaleFront.png")
	
	while running:
		#screen.fill([255, 255, 255])
		startbutton.blit(screen, (0,0))
		print(p.mouse.get_pos())
		for event in p.event.get():
			if event.type == p.QUIT:
				running = False
		key = p.key.get_pressed()
		if key[p.K_ESCAPE]:
			running = False
	
	print("starting main")


if __name__ == "__main__":
	p.init()
	main(p.display.set_mode((800, 600)))
	