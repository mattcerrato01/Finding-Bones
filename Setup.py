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
        collidable = p.sprite.Group(self.villagers())
        for sprite in self.hitboxes():
            collidable.add(sprite)




        return collidable



    def villagers(self):
        print("here we are")

        file = open("setup/villagers.txt","r")

        villager_list = p.sprite.Group()
        file.readline()
        line = file.readline()

        while line:
            split_array = line.split(", ")

            villager_list.add( Objects.Villagers( split_array[0] , split_array[1] == "True" , int(split_array[2]), int(split_array[3]), split_array[4] == "True" ) )

            line = file.readline()

        return villager_list

    def hitboxes(self):
        print("here we lay")
        file = open("setup/hitboxes.txt", "r")
        hitbox_list = p.sprite.Group()
        file.readline()
        line = file.readline()

        while line:
            split_array = line.split(", ")

            hitbox_list.add( Objects.Hitbox( int(split_array[0]), int(split_array[1]), int(split_array[2]), int(split_array[3])))

            line = file.readline()

        return hitbox_list