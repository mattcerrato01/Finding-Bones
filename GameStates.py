import random
import pygame as p

class WorldState:

    overworld = True

    def state(self):
        return WorldState.overworld

    def toggle(self):
        WorldState.overworld = not WorldState.overworld
    def x(self):
        x = 0

class NameGenerator:

    def __init__(self):
        self.male_names = ["William","Jonathan","Walter","Peter","Frederick","Roger","Arthur","Cedric","Leo","Ronald","Robin","Gavin","Charles","Benjamin","Matthew","Edwin","Nick","Bruce","Anthony","Juan","Albert","Gabriel"]

        self.female_names = ["Mary","Elizabeth","Maria","Claudia","Lydia","Cynthia","Lauren","Maisy","Erika","Silvia","Melody","Ann","Lisa","Elise","Joanne","Sue"]

    def generate(self, male = True):
        if male:
            return self.male_names[random.randint(0, len(self.male_names)-1)]
        return self.female_names[random.randint(0, len(self.female_names)-1)]

class CoordConverter:

    offset_x = 0
    offset_y = 0

    def set_offset_x(self, offset_x):
        CoordConverter.offset_x = offset_x

    def set_offset_y(self, offset_y):
        CoordConverter.offset_y = offset_y

    def real_x(self, screen_x):
        return screen_x - CoordConverter.offset_x

    def real_y(self, screen_y):
        return screen_y - CoordConverter.offset_y

    def screen_x(self, real_x):
        return real_x + CoordConverter.offset_x

    def screen_y(self, real_y):
        return real_y + CoordConverter.offset_y

class Inventory:

    inventory = []

    def has(self, item):

        for item_idx in range(len(Inventory.inventory)):
            if item == Inventory.inventory[item_idx][0]:
                return Inventory.inventory[item_idx][1]
        return 0

    def get_inventory(self):
        return Inventory.inventory[:]

    def append_to_inventory(self, object):

        found_item = False

        for i in range(len(Inventory.inventory)):
            if Inventory.inventory[i][0] == object:
                Inventory.inventory[i][1] += 1
                found_item = True
                break
        if not found_item:
            Inventory.inventory.append( ( object , 1 ) )

    def remove_from_inventory(self, object):
        for i in range(len(Inventory.inventory)):
            if Inventory.inventory[i][0] == object:
                Inventory.inventory.remove( ( object, Inventory.inventory[i][1] ) )
                break

    def draw(self, screen):
        height  = 50 + 20*len(Inventory.inventory)
        p.draw.rect(screen,(0,0,0), (450,228,150, height))
        dialogue_box_font = p.font.SysFont("papyrus", 20)
        dialogue_box = dialogue_box_font.render("Inventory:", True, (255, 255, 255))
        rect = dialogue_box.get_rect()
        screen.blit(dialogue_box,(525 - rect.width/2,238))
        for i in range(len(Inventory.inventory)):
            dialogue_box = dialogue_box_font.render(Inventory.inventory[i], True, (255, 255, 255))
            rect = dialogue_box.get_rect()
            screen.blit(dialogue_box,(525 - rect.width/2 ,258 + 20*i))



class Actions:

    dialogue_list = []

    def dialogue_box(self, dialogue):

        Actions.dialogue_list.append((dialogue, p.time.get_ticks()))

    def update_dialogue_box(self):

        while len(Actions.dialogue_list) > 4:
            Actions.dialogue_list.pop(0)

        while len(Actions.dialogue_list) > 0:
            if Actions.dialogue_list[0][1]+3000 < p.time.get_ticks():
                Actions.dialogue_list.pop(0)
            else:
                break

        return len(Actions.dialogue_list) > 0

    def perform_action(self, quest_actions):

        """

                :param quest_num: which quest you are referencing
                :param quest_stage: what stage of that quest
                :param action: what actions to be performed upon completion of that stage. Should be a string. Possible Actions:

                " 'berry' to inv " adds berry to inventory
                " 'berry' from inv " removes berry from inventory
                " print 'Hello there!' " prints 'Hello there!' in the dialogue box
                " 'berry' to inv AND print 'You received a berry!' " adds a berry to inventory and prints 'You received a berry!' to dialogue box

                do(3) {}
                do(A) {}
                Q(2,3) {}
                Q(2,A) {}
                if(has "berry")
                if(fate>=100)
                if(soul<90)

                :return:
                """

        return_string = ""

        for action in quest_actions.split(' AND '):

            return_sub_string = ""

            first_index = action.find("Q(")
            second_index = action.find(",")

            if "Q(" in action:
                if QuestManager.quests[int(action[first_index+2:second_index])] == int(action[second_index+1:action.find(")")]) or action[second_index+1] == "A":

                    return_sub_string = action[action.find("Q"):action.find("{")+1] + self.perform_action(action[action.find("{")+1:action.find("}")]) + "}" +" AND "


            elif "do(" in action:

                first_index = action.find("do(")+3
                second_index = action.find(")")

                if ":" in action[first_index:second_index]:

                    lower_bound = int(action[first_index:action.find(":")])
                    upper_bound = int(action[action.find(":")+1:second_index])

                    will_run = False

                    if lower_bound>0:
                        return_sub_string = "do(" + str(lower_bound-1) + ":" + str(upper_bound) + ") {" + action[action.find("{")+1:action.find("}")] + "}" +" AND "
                    else:
                        will_run = True

                else:
                    upper_bound = int(action[first_index:second_index])
                    will_run = True



                if will_run and upper_bound>0:

                    return_sub_string = "do(" + str(upper_bound-1) + ") {" + self.perform_action(action[action.find("{")+1:action.find("}")]) + "}" +" AND "
            # """elif "if(" in action:
            #
            #     first_index = action.find("if(") + 3
            #     second_index = action.find(")")
            #
            #     if "has " in action[first_index: second_index]:
            #         index_one = action.find("'")
            #         index_two = action.find("'", first_index + 1)
            #
            #         print("Current action is " + action)
            #         print("Initiating search of " + action[index_one+1:index_two])
            #         if Inventory.has(Inventory,action[index_one+1:index_two]) > 0:
            #             return_sub_string = "if(" + action[first_index:second_index] + ") {" + self.perform_action(action[action.find("{") + 1:action.find("}")]) + "}" + " AND "
            #         else:
            #             return_sub_string = action+" AND "
            #
            #     elif "hasnt " in action[first_index: second_index]:
            #         index_one = action.find("'")
            #         index_two = action.find("'", first_index + 1)
            #         if Inventory.has(Inventory,action[index_one+1:index_two]) == 0:
            #             return_sub_string = "if(" + action[first_index:second_index] + ") {" + self.perform_action(action[action.find("{") + 1:action.find("}")]) + "}" + " AND "
            #         else:
            #             return_sub_string = action+" AND "
            # """

            elif "has(" in action:

                first_index = action.find("has(")+4
                second_index = action.find(")")

                if Inventory.has(Inventory,action[first_index:second_index]):
                    return_sub_string = action[action.find("has("):action.find("{") + 1] + self.perform_action(action[action.find("{") + 1:action.find("}")]) + "}" + " AND "


            elif "inv" in action:

                return_sub_string = action+" AND "

                first_index = action.find("'")
                second_index = action.find("'", first_index+1)

                if 0 <= first_index < second_index:
                    found = False
                    for item_idx in range(len(Inventory.inventory)):
                        if action[first_index+1:second_index] in Inventory.inventory[item_idx]:
                            num = 0
                            if "to" in action:
                                int_index = Inventory.inventory[item_idx].find(" ")
                                num = int(Inventory.inventory[item_idx][:int_index]) + 1
                            elif "from" in action:
                                int_index = Inventory.inventory[item_idx].find(" ")
                                num = int(Inventory.inventory[item_idx][:int_index]) - 1

                            Inventory.inventory[item_idx] = str(num) + Inventory.inventory[item_idx][int_index:]

                            found = True
                            break
                    if not found:
                        if "to" in action:
                            Inventory.append_to_inventory(Inventory, "1 x "+ action[first_index+1:second_index])
                        elif "from" in action:
                            Inventory.remove_from_inventory(Inventory, action[first_index+1:second_index])


            elif "print" in action:
                return_sub_string = action+" AND "
                first_index = action.find("'")
                second_index = action.find("'", first_index + 1)
                if 0 <= first_index < second_index:
                    self.dialogue_box(action[first_index+1:second_index])


            return_string+=return_sub_string

        return return_string[:-5]
        #return ""

    "Q(1,A) {} AND Q(2,4) {}"

class QuestManager:

    quests = []
    quest_actions = []


    def add_number_quests(self, num):
        while True:
            if self.add_quest() >= num:
                break

    def add_quest(self):
        QuestManager.quests.append(0)
        QuestManager.quest_actions.append([])
        return len(QuestManager.quests)

    def set_quest_actions(self, quest_num, quest_stage, action):

        while( len(QuestManager.quest_actions[quest_num])-1 < quest_stage ):
            QuestManager.quest_actions[quest_num].append('')

        QuestManager.quest_actions[quest_num][quest_stage] = action

    def advance_quest(self, quest_num):
        while(len(QuestManager.quests) <= quest_num):
            QuestManager.quests.append(0)
            QuestManager.quest_actions.append([])
        QuestManager.quests[quest_num]+=1
        while (len(QuestManager.quest_actions[quest_num]) <= QuestManager.quests[quest_num]):
            QuestManager.quest_actions[quest_num].append('')
        Actions.perform_action(Actions, QuestManager.quest_actions[quest_num][QuestManager.quests[quest_num]])


    def quest_stage(self, quest_num):
        return QuestManager.quests[quest_num]

    def is_quest_stage(self, quest_num, quest_stage):
        return QuestManager.quests[quest_num] == quest_stage

    def past_quest_stage(self, quest_num, quest_stage):
        return QuestManager.quests[quest_num] > quest_stage
