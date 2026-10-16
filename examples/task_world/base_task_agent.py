from responsibility_agent import ResponsibilityAgent, FakeLogicObject
from task_world_responsibilities import Task, SpecificTask

class TaskAgent(ResponsibilityAgent):
    def __init__(self, env, name, colour):
        super().__init__(name, env)
        self.colour = colour
        self.addResponsibility(GreenTask())
        self.dgc["green_tasks"] = ["green"]
        
    def generate_tasks(self, r):
        tasks = []
        if isinstance(r, SpecificGreenTask):
            self.tasks.append(FakeLogicObject(r.name))
        return tasks
        
    def is_colour(self, b, colour):
        if b.name.startswith(colour):
            return True
        else:
            return False

    def getHighLevelResponsibilities(self):
        new_r = super().getHighLevelResponsibilities()
        for b in self.beliefs.beliefs:
            print(b)
        return new_r
            
    def want_to_accept(self, r_name):
        return True
        
    def do_not_want_to_accept(self, r_name):
        return False
        
    def update_dgc(self, percepts):
        for p in percepts:
            if p.name.startswith(colour):
                if p.name in self.dgc:
                    if self.name in self.dgc[p.name]:
                        print("do nothing")
                    else:
                        self.dgc[p.name].add(self.name)
                else:
                    self.dgc[p.name] = [self.name]
    
        

