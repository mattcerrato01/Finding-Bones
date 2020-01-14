import GameStates as gs
inventory = gs.Inventory()

class QuestManager:

    def __init__(self, number_of_quests):
        for i in range(number_of_quests-1):
            self.quests.append(0)
            self.quest_actions.append([])

    def set_quest_actions(self, quest_num, quest_stage, action):

        while( len(self.quest_actions[quest_num])-1 < quest_stage )
            self.quest_actions[quest_num].append('')

        self.quest_actions[quest_num][quest_stage] = action



        """
        
        :param quest_num: which quest you are referencing
        :param quest_stage: what stage of that quest
        :param action: what actions to be performed upon completion of that stage. Should be a string. Possible Actions:
        
        " 'berry' to inv " adds berry to inventory
        " 'berry' from inv " removes berry from inventory
        " print 'Hello there!' " prints 'Hello there!' in the dialogue box
        " 'berry' to inv AND print 'You received a berry!' " adds a berry to inventory and prints 'You received a berry!' to dialogue box
        
        :return: 
        """

    def advance_quest(self, quest_num):
        self.quests[quest_num]+=1
        self.__quest_actions()


    def quest_stage(self, quest_num):
        return self.quests[quest_num]

    def is_quest_stage(self, quest_num, quest_stage):
        return self.quests[quest_num] == quest_stage

    def past_quest_stage(self, quest_num, quest_stage):
        return self.quests[quest_num] > quest_stage

    def __quest_actions(self, quest_num, quest_stage):
        for action in self.quest_actions[quest_num][quest_stage].split(' AND '):
            if "inv" in action:
                first_index = action.find("'")
                second_index = action.find("'", first_index+1)
                if 0 <= first_index < second_index:
                    if "to" in action:
                        inventory.append_to_inventory(action[first_index+1:second_index])
                    elif "from" in action:
                        inventory.remove_from_inventory(action[first_index+1:second_index])
                else:
                    print("error in quest action, no item found")
            elif "print" in action:
                first_index = action.find("'")
                second_index = action.find("'", first_index + 1)
                if 0 <= first_index < second_index:
                    #code for printing action[first_index+1:second_index]


