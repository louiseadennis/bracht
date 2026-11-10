from responsibility_agent import FakeLogicObject
from task_world_responsibilities import Task, SpecificTask
from base_task_agent import *

class PriorityTaskAgent(base_task_agent):
    def __init__(self, env, name, colour):
        super().__init__(env, name, colour)
        
    def generate_tasks(self, r):
        tasks = []
        if self.current_colour_tasks and self.beliefs.believes(FakeLogicObject("done_" + self.current_colour_tasks[0])):
            self.current_colour_tasks = []
        if isinstance(r, SpecificTask) and self.my_colour(r.getColour()) and not self.current_colour_tasks:
            self.current_colour_tasks = [r.name]
        if self.current_colour_tasks and self.current_colour_tasks[0] == r.name:
            tasks.append(FakeLogicObject(self.current_colour_tasks[0]))
        return tasks
            
    def want_to_accept(self, r_name):
        if self.my_colour_starts_with(r_name):
            return True
        
        # return false if already have sub-responsibilities
        for r in self.responsibilities:
            for sr in r.getSubResponsibilities():
                return False
        
        return True
        
    def do_not_want_to_accept(self, r_name):
        return not self.want_to_accept(r_name)
        
        

