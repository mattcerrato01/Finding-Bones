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
        dialogues = []
        dialogues.append([])
        dialogues[0].append([])
        line = file.readline()
        quest_num = 0
        quest_event = 0
        while line:
            if "quest advance" in line:
                quest_num += 1
                quest_event = 0
                dialogues.append([])
                dialogues[quest_num].append([])
                line = file.readline()
            elif "quest event" in line:
                q = quest_event
                first_index = line.find("'")
                second_index = line.find("'", first_index+1)
                quest_event = int(line[first_index+1:second_index])
                q_chg = quest_event- q
                for i in range(q_chg):
                    dialogues[quest_num].append([])
                line = file.readline()
            dialogues[quest_num][quest_event].append(str(line))

            line = file.readline()
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

        while line:

            command = line[ : line.find(" ")]

            if "Quest" in command:
                quest = int( line[line.find(" ")+1 : line.find(":")] )
            elif command == "Stage":
                stage = int( line[line.find(" ")+1 : line.find(":")] )
                input = line[ line.find(":") + 1 : ]

                qm.set_quest_stage(quest, stage, input)
            elif command == "Name":
                name = line[ line.find("= ")+2 : len(line)-1 ]
            elif command == "Image":
                image = line[ line.find("= ")+2 : ]
            elif command == "Fated":
                fated = line[ line.find("= ")+2 : ]
            elif command == "(x,y)":
                sub = line[ line.find("= ")+2 : ]
                x = int( sub[ sub.find("(")+1 : sub.find(",") ] )
                y = int( sub[ sub.find(",")+1 : sub.find(")") ] )
            elif command == "Gender":

                male = str(line[line.find("= ")+2: line.find("= ")+3])
                print(male)

            elif command == "Grey":
                grey = line[ line.find("= ")+2 : line.rfind("e")] == "True"
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

                print( quest_array )

                villager_list.add(Objects.Quest_Villager( name, image.strip(), fated, quest_array, action, x, y, male, grey))

            line = file.readline()

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