import pygame as p



def loadify(imgname):
    return p.image.load("images/" + imgname).convert_alpha()

class Pause():
    def __init__(self):
        self.image = loadify("pause.png")
        self.image = p.transform.scale(self.image, (800,600))


    def draw(self,screen):

        screen.blit(self.image, (0,0))
    def button_clicked(self, mouse):
        restart = p.rect.Rect(435, 280, 340, 115)
        continue_button = p.rect.Rect(435, 420,  340, 115)
        if  restart.collidepoint(mouse):
            return "restart"
        elif continue_button.collidepoint(mouse):
            return "continue"
        else:
            return "Nothing"