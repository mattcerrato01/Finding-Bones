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

    def get_inventory(self):
        return Inventory.inventory[:]

    def append_to_inventory(self, object):
        Inventory.inventory.append(object)

    def remove_from_inventory(self, object):
        Inventory.inventory.remove(object)

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

            first_index = action.find("Q(")
            second_index = action.find(",")

            if "Q(" in action:
                if QuestManager.quests[int(action[first_index+2:second_index])] == action[second_index+1:action.find(")")] or action[second_index+1] == "A":

                    return_string+=self.perform_action(action[action.find("{")+1,action.find("}")])

            if "inv" in action:

                first_index = action.find("'")
                second_index = action.find("'", first_index+1)
                if 0 <= first_index < second_index:
                    found = False
                    for item_idx in range(len(Inventory.inventory)):
                        if action[first_index+1:second_index] in Inventory.inventory[item_idx]:
                            num = 0
                            if "to" in action:
                                int_index = Inventory.inventory[item_idx].find(" ")
                                num = int(Inventory.inventory[item_idx][int_index-1]) + 1
                            elif "from" in action:
                                int_index = Inventory.inventory[item_idx].find(" ")
                                num = int(Inventory.inventory[item_idx][int_index-1]) - 1
                            Inventory.inventory[item_idx] = str(num) + Inventory.inventory[item_idx][1:]
                            found = True
                            break
                    if not found:
                        if "to" in action:
                            Inventory.append_to_inventory(Inventory, "1 x "+ action[first_index+1:second_index])
                        elif "from" in action:
                            Inventory.remove_from_inventory(Inventory, action[first_index+1:second_index])

                    print(Inventory.inventory)

            elif "print" in action:
                first_index = action.find("'")
                second_index = action.find("'", first_index + 1)
                if 0 <= first_index < second_index:
                    self.dialogue_box(action[first_index+1:second_index])

        return return_string

    "Q(1,A) {} AND Q(2,4) {}"

class QuestManager:

    quests = []
    quest_actions = []

    def __init__(self, number_of_quests):
        for i in range(number_of_quests-1):
            QuestManager.quests.append(0)
            QuestManager.quest_actions.append([])

    def set_quest_actions(self, quest_num, quest_stage, action):

        while( len(QuestManager.quest_actions[quest_num])-1 < quest_stage ):
            QuestManager.quest_actions[quest_num].append('')

        QuestManager.quest_actions[quest_num][quest_stage] = action

    def advance_quest(self, quest_num):
        QuestManager.quests[quest_num]+=1
        #QuestManager.quest_actions.perform_action(QuestManager.quest_actions[quest_num][QuestManager.quests[quest_num]])


    def quest_stage(self, quest_num):
        return QuestManager.quests[quest_num]

    def is_quest_stage(self, quest_num, quest_stage):
        return QuestManager.quests[quest_num] == quest_stage

    def past_quest_stage(self, quest_num, quest_stage):
        return QuestManager.quests[quest_num] > quest_stage
