import random
import pygame as p
def loadify(imgname):
    return p.image.load("images/" + imgname).convert_alpha()

def linesplitter(line, font, width, initial_string = ""):
    return_array = []
    subline = initial_string + " "

    words = line.split(" ")

    for word in words:
        if font.size(subline + word + " ")[0] <= width:
            subline += word + " "
        else:
            return_array.append(subline)
            subline = word + " "

    return_array.append(subline)

    return return_array


def reset():
    WorldState.overworld =True
    Inventory.inventory = []
    QuestManager.quests =  []
    QuestManager.quest_actions = []
class WorldState:
    overworld = True
    highscore = 0

    def state(self):
        return WorldState.overworld

    def toggle(self):
        WorldState.overworld = not WorldState.overworld


    def set_highscore(self,newhs):
        WorldState.highscore = newhs
    def get_highscore(self):
        return WorldState.highscore

def change_track(state):
    p.mixer.music.stop()
    if state == 1:
        p.mixer.music.load('soundtrack/Overworld_Track.wav')
    elif state == 2:
        p.mixer.music.load('soundtrack/Underworld_Theme.wav')
    elif state == 3:
        p.mixer.music.load('soundtrack/Game_Over.wav')
    elif state == 4:
        p.mixer.music.load('soundtrack/Start_Screen.wav')
    else:
        p.mixer.music.load('effects/BlehSound.wav')
    p.mixer.music.play(-1)


class NameGenerator:

    def __init__(self):
        self.male_names = ["William", "Jonathan", "Walter", "Peter", "Frederick", "Roger", "Arthur", "Cedric", "Leo",
                           "Ronald", "Robin", "Gavin", "Charles", "Benjamin", "Matthew", "Edwin", "Nick", "Bruce",
                           "Anthony", "Juan", "Albert", "Gabriel"]

        self.female_names = ["Mary", "Elizabeth", "Maria", "Claudia", "Lydia", "Cynthia", "Lauren", "Maisy", "Erika",
                             "Silvia", "Melody", "Ann", "Lisa", "Elise", "Joanne", "Sue"]

    def generate(self, male):
        if male == "m":
            return self.male_names[random.randint(0, len(self.male_names) - 1)]
        elif male == "f":
            return self.female_names[random.randint(0, len(self.female_names) - 1)]


class CoordConverter:
    offset_x = 0
    offset_y = 0

    def set_offset_x(self, offset_x):
        CoordConverter.offset_x = offset_x

    def set_offset_y(self, offset_y):
        CoordConverter.offset_y = offset_y
    def get_offset_x(self):
        return CoordConverter.offset_x
    def get_offset_y(self):
        return CoordConverter.offset_y

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
        num = 1
        if " x " in item:
            num = int(item[item.find(" x ")+ 3:])
            item = item[:item.find(" x ")]

        for things in Inventory.inventory:
            if item == things[0]:
                if num ==1:
                    return True
                else:
                    return things[1]>= num
        return False

    def get_inventory(self):
        return Inventory.inventory[:]

    def append_to_inventory(self, object):

        found_item = False

        for i in range(len(Inventory.inventory)):
            if object == Inventory.inventory[i][0]:
                Inventory.inventory[i][1] += 1
                found_item = True
                break
        if not found_item:
            image = p.transform.scale(loadify(object + ".png"), (18,18 ))
            Inventory.inventory.append([object, 1, image])


    def remove_from_inventory(self, object):
        for i in range(len(Inventory.inventory)):
            if Inventory.inventory[i][0] == object:
                if Inventory.inventory[i][1] == 1:
                    Inventory.inventory.pop(i)
                elif Inventory.inventory[i][1] > 1:
                    Inventory.inventory[i][1] -= 1
                break

    def draw(self, screen, loaded_image):
        height = 60 + 20 * len(Inventory.inventory)
        image = p.transform.scale(loaded_image, (150, height))
        screen.blit(image, (450, 228))
        # p.draw.rect(screen, (0, 0, 0), (450, 228, 150, height))
        dialogue_box_font = p.font.SysFont("papyrus", 20)
        dialogue_box = dialogue_box_font.render("Inventory:", True, (255, 255, 255))
        rect = dialogue_box.get_rect()
        screen.blit(dialogue_box, (525 - rect.width / 2, 238))
        for i in range(len(Inventory.inventory)):
            line = Inventory.inventory[i][0] + " x " + str(Inventory.inventory[i][1])
            dialogue_box = dialogue_box_font.render(line, True, (255, 255, 255))
            rect = dialogue_box.get_rect()
            screen.blit(dialogue_box, (525 - rect.width / 2, 258 + 20 * i))
            screen.blit(Inventory.inventory[i][2], (530 + rect.width / 2, 260 + 20 * i))


class Actions:
    dialogue_list = []
    perform_action_in_underworld = False

    def dialogue_box(self, dialogue):

        dialogue_box_font = p.font.SysFont("papyrus", 20)

        temp = dialogue.split("â€™")

        dialogue = ""

        for word in temp:
            dialogue += "'" + word

        dialogue = dialogue[1:]

        words = dialogue.split(" ")

        temp_string = ""

        for word in words:

            if dialogue_box_font.size(temp_string + " " + word)[0] > 460:
                Actions.dialogue_list.append(temp_string)
                temp_string = word
            else:
                temp_string += " " + word
        Actions.dialogue_list.append(temp_string)

    def set_uwa(self, uwa):
        Actions.perform_action_in_underworld = uwa

    def set_dialogue(self, dialogue):
        Actions.dialogue_list = dialogue

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

                :return:
                """

        return_string = ""

        for action in quest_actions.split(' AND '):


            return_sub_string = ""
            end_of_string = ""
            if "reaped" in action and WorldState.state(WorldState):
                action = action[:action.find("reaped")] + "}"
                end_of_string = action[action.find("reaped"): action.rfind(")")]


            first_index = action.find("Q(")
            second_index = action.find(",")

            if (WorldState.state(WorldState) or Actions.perform_action_in_underworld):

                if "Q(" in action:
                    if QuestManager.quest_stage(QuestManager,int(action[first_index + 2:second_index])) == int(
                            action[second_index + 1:action.find(")")]) or action[second_index + 1] == "A":
                        conditional_action = action[action.find("{") + 1:action.rfind("}")]
                        return_sub_string = action[action.find("Q("):action.find("{") + 1]
                        for string in conditional_action.split("**"):
                            return_sub_string = action[action.find("Q("):action.find("{") + 1] + self.perform_action(string) + "} AND "


                elif "do(" in action:

                    boundless = False

                    first_index = action.find("do(")+3
                    second_index = action.find(")")

                    if ":" in action[first_index:second_index]:

                        lower_bound = int(action[first_index:action.find(":")])
                        upper_bound = action[action.find(":") + 1:second_index]


                        if upper_bound == "A":
                            upper_bound = 25
                            boundless = True
                        else:
                            upper_bound = int(upper_bound)

                        will_run = False

                        if lower_bound > 0:
                            return_sub_string = "do(" + str(lower_bound - 1) + ":" + str(upper_bound) + ") {" + action[action.find("{") + 1:action.find("}")] + "}" + " AND "
                        else:
                            will_run = True

                    else:
                        upper_bound = action[first_index:second_index]
                        if upper_bound == "A":
                            upper_bound = 25
                            boundless = True
                        else:
                            upper_bound = int(upper_bound)
                        will_run = True

                    if will_run and upper_bound > 0:
                        conditional_action = action[action.find("{") + 1:action.find("}")]
                        strings = conditional_action.split(",, ")
                        upper_bound_chg = 0
                        end_string = ""
                        for idx in range(len(strings)):
                            if idx == (len(strings) - 1):
                                upper_bound_chg = 1
                            end_string += self.perform_action(strings[idx]) + ",, "

                        if boundless:
                            return_sub_string = "do(A) {" + end_string + "}" + " AND "
                        else:
                            return_sub_string = "do(" + str(upper_bound - upper_bound_chg) + ") {" + end_string + "}" + " AND "

                elif "has(" in action:

                    first_index = action.find("has(") + 4
                    second_index = action.find(")")
                    condition_met = True
                    for conditions in action[first_index:second_index].split(",, "):

                        if not Inventory.has(Inventory, conditions):
                            condition_met = False
                            break
                    if condition_met:
                        conditional_action = action[action.find("{") + 1:action.find("}")]
                        for string in conditional_action.split(",,"):
                            return_sub_string = action[action.find("has("):action.find("{") + 1] + self.perform_action(string) +"}" + " AND "
                    else:
                        return_sub_string = action + " AND "
                elif "hasnt(" in action:

                    first_index = action.find("hasnt(") + 6
                    second_index = action.find(")")

                    if not Inventory.has(Inventory, action[first_index:second_index]):
                        conditional_action = action[action.find("{") + 1:action.find("}")]
                        for string in conditional_action.split(",, "):
                            return_sub_string = action[action.find("hasnt("):action.find("{") + 1] + self.perform_action(
                                string) + "}" + " AND "
                    else:
                        return_sub_string = action + " AND "

                elif "inv" in action:

                    return_sub_string = action + " AND "

                    first_index = action.find('"')
                    second_index = action.find('"', first_index + 1)

                    if 0 <= first_index < second_index:
                        if "to" in action:
                            Inventory.append_to_inventory(Inventory, action[first_index + 1:second_index])

                        elif "from" in action:
                            Inventory.remove_from_inventory(Inventory, action[first_index + 1:second_index])

                elif "print" in action:
                    return_sub_string = action + " AND "
                    first_index = action.find('"')
                    second_index = action.find('"', first_index + 1)
                    if 0 <= first_index < second_index:
                        Actions.dialogue_box(Actions, action[first_index + 1:second_index])

                elif "adv quest" in action:
                    QuestManager.add_quest()
                elif "set quest(" in action:
                    first_index = action.find("set quest(") + 10
                    second_index = action.find(",")
                    third_index = action.find(")")
                    return_sub_string = action + " AND "
                    try:
                        QuestManager.set_quest(QuestManager, int(action[first_index: second_index]) , int(action[second_index+1 : third_index]) )
                    except:
                        pass

            elif not WorldState.state(WorldState) and "reaped" in action:
                Actions.perform_action_in_underworld = True
                conditional_action = action[action.find("reaped(") + 7:action.rfind(")")]
                for string in conditional_action.split(",,"):
                    return_sub_string = "reaped(" + Actions.perform_action(Actions, string) + ")" + " AND "
                Actions.perform_action_in_underworld = False

            return_string += return_sub_string + end_of_string

        return return_string[:-5]
        # return ""

    "Q(1,A) {} AND Q(2,4) {}"


class QuestManager:
    quests = []
    quest_actions = []
    quest_text_array = []


    def add_quest(self, add_to = -1):

        if add_to == -1:
            QuestManager.quests.append(-1)
            QuestManager.quest_actions.append([])
        else:
            while len(QuestManager.quests) <= add_to:
                QuestManager.quests.append(-1)
                QuestManager.quest_actions.append([])

    def set_quest_stage(self, quest_num, quest_stage, action):

        QuestManager.add_quest(self, quest_num)

        while len(QuestManager.quest_actions[quest_num]) <= quest_stage:
            QuestManager.quest_actions[quest_num].append('')

        QuestManager.quest_actions[quest_num][quest_stage] = action

    def advance_quest(self, quest_num):
        while(len(QuestManager.quests) <= quest_num):
            QuestManager.quests.append(-1)
            QuestManager.quest_actions.append([])
        QuestManager.quests[quest_num]+=1
        while (len(QuestManager.quest_actions[quest_num]) <= QuestManager.quests[quest_num]):
            QuestManager.quest_actions[quest_num].append('')

        Actions.perform_action(Actions, QuestManager.quest_actions[quest_num][QuestManager.quests[quest_num]])

    def set_quest(self, quest_num, quest_stage):
        while QuestManager.quests[quest_num] < quest_stage:
            QuestManager.advance_quest(QuestManager, quest_num)

    def run_stage(self, quest_num, quest_stage):
        Actions.perform_action(Actions, QuestManager.quest_actions[quest_num][quest_stage])

    def quest_stage(self, quest_num):
        try:
            return QuestManager.quests[quest_num]
        except:
            return -1

    def is_quest_stage(self, quest_num, quest_stage):
        return QuestManager.quests[quest_num] == quest_stage

    def past_quest_stage(self, quest_num, quest_stage):
        return QuestManager.quests[quest_num] > quest_stage

    def set_quest_text_array(self, quest_text_array):
        QuestManager.quest_text_array = quest_text_array

    def draw(self, screen, loaded_image):
        screen.blit(loaded_image, (0, 0))
        dialogue_box_font = p.font.SysFont("papyrus", 20)
        dialogue_box = dialogue_box_font.render("Quests Progress:", True, (0, 0, 0))
        screen.blit(dialogue_box, (30, 20))



        i = 0

        for array in QuestManager.quest_text_array:
            current_quest_number = array[0][0]
            current_quest_title = array[0][1]
            current_quest_stage = QuestManager.quest_stage(QuestManager, current_quest_number)

            for stage in array[1 : ]:
                if stage[0] == current_quest_stage:

                    split_line = linesplitter(stage[1], dialogue_box_font, 300, current_quest_title+":")

                    for subline in split_line:

                        dialogue_box = dialogue_box_font.render(subline, True, (0, 0, 0))
                        screen.blit(dialogue_box, (30, 45 + 25 * i))
                        i += 1


                    break





        #for i in range(len(quest_titles)):
        #    stage_chg = 0
        #    if i == 2 and QuestManager.quest_stage(QuestManager,1)>=2:
        #        stage_chg = -1
        #    line = quest_titles[i] + "  " + str(QuestManager.quest_stage(QuestManager, i) +stage_chg)
        #    if QuestManager.quest_stage(QuestManager, i) >= len(QuestManager.quest_actions[i])-1:
        #       line = quest_titles[i] + "  " + "DONE"
        #    dialogue_box = dialogue_box_font.render(line, True, (255, 255, 255))
        #    rect = dialogue_box.get_rect()
        #    screen.blit(dialogue_box, (275 - rect.width / 2, 258 + 20 * i))
