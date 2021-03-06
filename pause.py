import pygame as p

def play_sound(name):
	  sound = p.mixer.Sound("effects/" + name + ".wav")
	  sound.play()

def loadify(imgname):
	return p.image.load("images/" + imgname).convert_alpha()
class Pause():
	def __init__(self):
		self.image = loadify("pause.png")
		self.image = p.transform.scale(self.image, (800,600))



	def draw(self, screen):
		screen.blit(self.image,(0,0))
	def button_clicked(self, mouse):
		restart = p.rect.Rect(435, 280, 340, 120)
		continue_button = p.rect.Rect(434,420, 440, 120)
		if restart.collidepoint(mouse):
			play_sound("Button_Click")
			return "restart"
		elif continue_button.collidepoint(mouse):
			play_sound("Button_Click")
			return "continue"
		else:
			return "nothing"