from responsibility_agent import ResponsibilityAgent, FakeLogicObject
from care_home_responsibilities import CleanSpill

class HealthAndSafetyAgent(ResponsibilityAgent):
    def __init__(self, env, name):
        super().__init__(name, env)
        self.addResponsibility(CleanSpill())
        self.dgc["clean_spill"] = ["cleaner1","cleaner2"]
        self.dgc["notify"] = ["cleaner1","cleaner2"]
        
    def generate_tasks(self, r):
        tasks = []
        return tasks
        
    def i_believe(self, string):
         if (self.beliefs.believes(FakeLogicObject(string))):
            return True
            
