import sys
sys.path.insert(0, '../..')

from responsibility_world import *
from responsibility_agent import FakeLogicObject
from cleaning_agent import GrumpyCleaningAgent
from health_and_safety_agent import HealthAndSafetyAgent


class care_home_world(responsibility_world):
    def __init__(self):
        super().__init__()
        simple_cleaning_agent_1 = GrumpyCleaningAgent(self, "cleaner1")
        simple_cleaning_agent_2 = GrumpyCleaningAgent(self, "cleaner2")
        coordinator_agent = HealthAndSafetyAgent(self, "coordinator")
        self.total_iterations = 10
        self.interactive = True
        self.spill_duration = 0
        self.location_cleaner_1 = 2 # near hall
        self.location_cleaner_2 = 4 # near stairs
        self.agents = [simple_cleaning_agent_1, simple_cleaning_agent_2, coordinator_agent]
           
    def update_perceptions(self):
        if self.iterations == 1:
            self.add_percept('spill_stairs')
            self.remove_percept('not_spill')
            self.spill_duration = 1
        if (not FakeLogicObject('spill_hall') in self.perceptions and not FakeLogicObject('spill_stairs') in self.perceptions):
            self.add_percept('not_spill')
            self.spill_duration = 0
        else:
            self.spill_duration = self.spill_duration + 1
            if (self.spill_duration > 8):
                self.add_percept('spill_10')
                
        
    def update_locations(self):
        self.remove_percept('at_stairs_cleaner_1')
        self.remove_percept('at_stairs_cleaner_2')
        self.remove_percept('near_stairs_cleaner_1')
        self.remove_percept('near_stairs_cleaner_2')
        self.remove_percept('middle_cleaner_1')
        self.remove_percept('middle_cleaner_2')
        self.remove_percept('at_hall_cleaner_1')
        self.remove_percept('at_hall_cleaner_2')
        self.remove_percept('near_hall_cleaner_1')
        self.remove_percept('near_hall_cleaner_2')
        if (self.location_cleaner_1 == 0):
            self.add_percept('at_stairs_cleaner_1')
        elif (self.location_cleaner_1 == 1 or self.location_cleaner_1 == 2):
            self.add_percept('near_stairs_cleaner_1')
        elif (self.location_cleaner_1 == 3):
            self.add_percept('middle_cleaner_1')
        elif (self.location_cleaner_1 == 4 or self.location_cleaner_1 == 5):
            self.add_percept('near_hall_cleaner_1')
        else:
            self.add_percept('at_hall_cleaner_1')
            
        if (self.location_cleaner_2 == 0):
            self.add_percept('at_stairs_cleaner_2')
        elif (self.location_cleaner_2 == 1 or self.location_cleaner_2 == 2):
            self.add_percept('near_stairs_cleaner_2')
        elif (self.location_cleaner_2 == 3):
            self.add_percept('middle_cleaner_2')
        elif (self.location_cleaner_1 == 4 or self.location_cleaner_2 == 5):
            self.add_percept('near_hall_cleaner_2')
        else:
            self.add_percept('at_hall_cleaner_2')

    def do(self, agent, task):
        if (task.name == "notify"):
            print(agent.name + " did NOTIFIED")
            self.add_percept("notified")
        if (task.name == "clean"):
            if (agent.name == "cleaner1" and self.location_cleaner_1 == 0):
                self.remove_perception("spill_stairs")
            elif (agent.name == "cleaner1" and self.location_cleaner_1 == 4):
                self.remove_perception("spill_hall")
            elif (agent.name == "cleaner2" and self.location_cleaner_2 == 0):
                self.remove_perception("spill_stairs")
            elif (agent.name == "cleaner2" and self.location_cleaner_2 == 4):
                self.remove_perception("spill_hall")
            print(agent.name + " did CLEANED")
        if (task.name == "move_hall"):
            if (agent.name == "cleaner1"):
                self.location_cleaner_1 = self.location_cleaner_1 + 1
            else:
                self.location_cleaner_2 = self.location_cleaner_2 + 1
            print(agent.name + " moved towards hall")
        if (task.name == "move_stairs"):
            if (agent.name == "cleaner1"):
                self.location_cleaner_1 = self.location_cleaner_1 - 1
            else:
                self.location_cleaner_2 = self.location_cleaner_2 - 1
            print(agent.name + " moved towards stairs")
        else:
            super().do(agent, task)
            
        self.update_locations()
                
    def add_percept(self, string):
        self.perceptions.append(FakeLogicObject(string))
        
    def remove_percept(self, string):
        self.remove_perception(string)
                    
world = care_home_world()
world.run()
    
