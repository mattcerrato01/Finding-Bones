import pygame as p
import Objects

class WriteTest:
    file = open("testfile.txt", "w")

    file.write("Hello  \n")
    file.write("This is our new text file")
    file.write(" and this is another line.")

    file.close()

    file = open("testfile.txt", "r")

    # print(file.read(3))
    # print(file.read(6))
    # print(file.readline())

class Setup:
    def quest_dialogue(self):
        file = open("setup/forced_dialogue.txt")
        dialogue = []
        line = file.readline()
        while line:
            dialogue.append(str(line))
            # print(line)
            line = file.readline()
        return dialogue

    def collidables(self):
        collidable = p.sprite.Group(self.villagers())
        for sprite in self.hitboxes():
            collidable.add(sprite)
        for sprite in self.objects():
            collidable.add(sprite)
        return collidable



    def villagers(self):
        # print("here we are")

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
        # print("here we lay")
        file = open("setup/hitboxes.txt", "r")
        hitbox_list = p.sprite.Group()
        file.readline()
        line = file.readline()

        while line:
            split_array = line.split(", ")
            action = ""
            if len(split_array) > 4:
                action = split_array[4]
                for i in range(4, len(split_array)-1):
                    action += ", " +  split_array[i+1]

            hitbox_list.add( Objects.Hitbox( int(split_array[0]), int(split_array[1]), int(split_array[2]), int(split_array[3]), action))

            line = file.readline()

        return hitbox_list

    def objects(self):
        # print("here we go")
        file = open("setup/objects.txt", "r")
        object_list = p.sprite.Group()
        file.readline()
        line = file.readline()

        while line:
            split_array = line.split(", ")
            action = ""
            if len(split_array) > 5:
                action = split_array[5]
                for i in range(5, len(split_array)-1):
                    action += ", " +  split_array[i+1]

            object_list.add(Objects.Object(split_array[0], int(split_array[1]), int(split_array[2]), int(split_array[3]), int(split_array[4]), action ))

            line = file.readline()

        return object_list
    
   