import GameStates as gs
inventory = gs.Inventory()
actions = gs.Actions()

class QuestManager:

    def __init__(self, number_of_quests):
        for i in range(number_of_quests-1):
            self.quests.append(0)
            self.quest_actions.append([])

    def set_quest_actions(self, quest_num, quest_stage, action):

        while( len(self.quest_actions[quest_num])-1 < quest_stage ):
            self.quest_actions[quest_num].append('')

        self.quest_actions[quest_num][quest_stage] = action

    def advance_quest(self, quest_num):
        self.quests[quest_num]+=1
        actions.perform_action(self.quest_actions[quest_num][self.quests[quest_num]])


    def quest_stage(self, quest_num):
        return self.quests[quest_num]

    def is_quest_stage(self, quest_num, quest_stage):
        return self.quests[quest_num] == quest_stage

    def past_quest_stage(self, quest_num, quest_stage):
        return self.quests[quest_num] > quest_stage



