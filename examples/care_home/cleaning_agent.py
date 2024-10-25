from responsibility_agent import ResponsibilityAgent, FakeLogicObject
from care_home_responsibilities import CleanSpill

class CleaningAgent(ResponsibilityAgent):
    def __init__(self, env, name):
        super().__init__(name, env)
        self.addResponsibility(CleanSpill())
        self.dgc["clean_spill"] = [name]
        self.dgc["notify"] = [name]
        
    def generate_tasks(self, r):
        tasks = []
        if (r.name == "notify"):
            self.tasks.append(FakeLogicObject("notify"))
        elif (r.name == "clean_spill" and self.beliefs.believes(FakeLogicObject("spill"))):
            self.tasks.append(FakeLogicObject("clean"))
        return tasks
        
