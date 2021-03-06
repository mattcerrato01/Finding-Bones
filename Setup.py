import pygame as p
import Objects
import GameStates as gs
qm = gs.QuestManager()

class WriteTest:
    file = open("testfile.txt", "w")

    file.write("Hello  \n")
    file.write("This is our new text file")
    file.write(" and this is another line.")

    file.close()

    file = open("testfile.txt", "r")


class Setup:
    def quest_dialogue(self):
        file = open("setup/forced_dialogue.txt")
        dialogues = file.readline()
        return dialogues

    def collidables(self):
        collidable = p.sprite.Group(self.villagers())
        for sprite in self.hitboxes():
            collidable.add(sprite)
        for sprite in self.objects():
            collidable.add(sprite)
        return collidable



    def villagers(self):

        file = open("setup/villagers.txt","r")

        villager_list = p.sprite.Group()
        file.readline()
        line = file.readline()

        while line:
            split_array = line.split(", ")


            villager_list.add( Objects.Villagers( split_array[0], split_array[1] == "True" , int(split_array[2]), int(split_array[3]), split_array[4][0:1]) )

            line = file.readline()

        return villager_list

    def quests(self):

        file = open("setup/quests.txt","r")

        villager_list = p.sprite.Group()
        line = file.readline()
        secret = False

        quest_text_array = []

        while line:

            command = line[ : line.find(" ")]

            if "Quest" in command:
                quest = int( line[line.find(" ")+1 : line.find(" /")] )
                quest_text_array.append([ (quest , line[line.find("/ ")+2 : len(line)-1 ]) ])

            elif command == "Stage":
                stage = int( line[line.find(" ")+1 : line.find(":")] )
                input = line[ line.find(":") + 1 : line.find(" /")]
                qm.set_quest_stage(quest, stage, input)

                quest_text_array[ len(quest_text_array)-1 ].append( (stage, line[ line.find("/ ") + 2 : len(line)-1 ] ))

            elif command == "Name":
                name = line[ line.find("= ")+2 : len(line)-1 ]
            elif command == "Image":
                image = line[ line.find("= ")+2 : ]
            elif command == "Fated":
                fated = line[ line.find("= ")+2 : line.rfind("e") + 1 ] == "True"
            elif command == "(x,y)":
                sub = line[ line.find("= ")+2 : ]
                x = int( sub[ sub.find("(")+1 : sub.find(",") ] )
                y = int( sub[ sub.find(",")+1 : sub.find(")") ] )
            elif command == "Gender":

                male = str(line[line.find("= ")+2: line.find("= ")+3])

            elif command == "Grey":
                grey = line[ line.find("= ")+2 : line.rfind("e")+1] == "True"
            elif command == "Secret":
                secret = line[ line.find("= ")+2 : line.rfind("e")+1] == "True"
            elif command == "Action":
                action = line[ line.find("= ")+2 : ]

                if "Q(" in action:
                    quest_array = [ int( action[action.rfind("Q(") + 2 : action.rfind("Q(") + 3 ] ) ]

                    last_index = -1

                    while True:

                        last_index = int( action.find("Q(", last_index+1) )

                        if last_index == -1:
                            break
                        else:
                            holder = action[action.find(",", last_index+1) + 1 : action.find( ")" , last_index+1)]
                            quest_array.append(int(holder))


                else:
                    quest_array = [-1,-1]

                villager_list.add(Objects.Quest_Villager( name, image.strip(), fated, quest_array, action, x, y, male, grey, secret))

            line = file.readline()

        qm.set_quest_text_array(quest_text_array)


        return villager_list

    def hitboxes(self):
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