import pygame as p
import Objects

class WriteTest:
    file = open("testfile.txt", "w")

    file.write("Hello  \n")
    file.write("This is our new text file")
    file.write(" and this is another line.")

    file.close()

    file = open("testfile.txt", "r")

    print(file.read(3))
    print(file.read(6))
    print(file.readline())

class Setup:

    def collidables(self):

        collidables = p.sprite.Group(self.villagers)

        return collidables



    def villagers(self):

        file = open("setup/villagers.txt","r")

        villager_list = []
        line = file.readline()

        while len(line) > 0:
            split_array = line.split(", ")[0]

            villager_list.append( Objects.Villagers( split_array[0] , split_array[1] , split_array[2]) )

            line = file.readline()

        return villager_list