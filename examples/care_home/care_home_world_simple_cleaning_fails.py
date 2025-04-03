import sys
sys.path.insert(0, '../..')

from responsibility_world import *
from responsibility_agent import FakeLogicObject
from cleaning_agent import CleaningAgent


class care_home_world(responsibility_world):
    def __init__(self):
        super().__init__()
        simple_cleaning_agent_1 = CleaningAgent(self, "cleaner1")
        simple_cleaning_agent_2 = CleaningAgent(self, "cleaner2")
        self.total_iterations = 5
        self.interactive = True
        self.spill_duration = 0
        self.agents = [simple_cleaning_agent_1, simple_cleaning_agent_2]
           
    def update_perceptions(self):
        if self.iterations == 1:
            self.perceptions.append(FakeLogicObject('spill'))
            self.perceptions.remove(FakeLogicObject('not_spill'))
            self.spill_duration = 1
        if (not FakeLogicObject('spill') in self.perceptions):
            self.perceptions.append(FakeLogicObject('not_spill'))
        else:
            self.spill_duration = self.spill_duration + 1
            if (self.spill_duration > 3):
                self.perceptions.append(FakeLogicObject('spill_10'))
            
    def do(self, agent, task):
        if (task.name == "notify"):
            print(agent.name + " did NOTIFIED")
            self.perceptions.append(FakeLogicObject("notified"))
        if (task.name == "clean"):
            #self.remove_perception("spill")
            print(agent.name + " did CLEANED")
            
    def remove_perception(self, string):
        for p in self.perceptions:
            if (p.name == string):
                self.perceptions.remove(p)
                    
world = care_home_world()
world.run()
    
