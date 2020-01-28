import pygame as p


def loadify(imgname):
    return p.image.load("images/" + imgname).convert_alpha()

def main():
	pass



if __name__ == "__main__":
	main(p.display.set_mode((800, 600)), True)