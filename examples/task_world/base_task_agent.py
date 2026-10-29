from responsibility_agent import ResponsibilityAgent, FakeLogicObject
from task_world_responsibilities import Task, SpecificTask

class TaskAgent(ResponsibilityAgent):
    def __init__(self, env, name, colour):
        super().__init__(name, env)
        self.colours = [colour]
        self.addResponsibility(Task(colour))
        self.dgc[colour + "_tasks"] = [name]
        self.current_colour_tasks = []
        
    def generate_tasks(self, r):
        tasks = []
        if self.current_colour_tasks and self.beliefs.believes(FakeLogicObject("done_" + self.current_colour_tasks[0])):
            self.current_colour_tasks = []
        if isinstance(r, SpecificTask) and self.my_colour(r.getColour()) and not self.current_colour_tasks:
            self.current_colour_tasks = [r.name]
        if self.current_colour_tasks and self.current_colour_tasks[0] == r.name:
            tasks.append(FakeLogicObject(self.current_colour_tasks[0]))
        return tasks

    def getHighLevelResponsibilities(self):
        new_r = super().getHighLevelResponsibilities()
        for b in self.beliefs.beliefs:
            self.print_level(b)
        return new_r
            
    def want_to_accept(self, r_name):
        return True
        
    def do_not_want_to_accept(self, r_name):
        return False
        
    def update_dgc(self, percepts):
        for p in percepts:
            if self.my_colour_starts_with(p.name):
                if p.name in self.dgc:
                    if self.name in self.dgc[p.name]:
                        self.print_level("do nothing", 4)
                    else:
                        self.dgc[p.name].add(self.name)
                else:
                    self.dgc[p.name] = [self.name]
                    
    def my_colour_starts_with(self, string):
        for colour in self.colours:
            if string.startswith(colour):
                return True
        return False
                    
    def my_colour(self, string):
        for colour in self.colours:
            if string == colour:
                return True
        return False

        

