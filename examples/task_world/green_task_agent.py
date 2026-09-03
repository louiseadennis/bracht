from responsibility_agent import ResponsibilityAgent, FakeLogicObject
from task_world_responsibilities import GreenTask

class GreenTaskAgent(ResponsibilityAgent):
    def __init__(self, env, name):
        super().__init__(name, env)
        self.addResponsibility(GreenTask())
        
    def generate_tasks(self, r):
        tasks = []
        if self.is_green(r):
            self.tasks.append(FakeLogicObject(r.name))
        return tasks
        
        
    def is_green(r):
        if r.name.startswith("green_task"):
            return True
        else:
            return False
            
    def want_to_accept(self, r_name):
        return True
        
    def do_not_want_to_accept(self, r_name):
        return False
        
    def update_dgc(self, percepts):
        for (p in percepts):
            if p.name.startswith("green"):
                if p.name in self.dgc:
                    print("do nothing")
                else:
                    self.dgc[p.name] = self.name
    
        
q
