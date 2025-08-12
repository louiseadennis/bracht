from responsibility_agent import ResponsibilityAgent, Responsibility, FakeLogicObject, Continuation

class DingStuffAgent(ResponsibilityAgent):
    def __init__(self, env):
        super().__init__("dingstuff agent", env)
        self.addResponsibility(DingStuffResponsibility())
        self.dgc["dingstuff"] = ["dingstuff agent"]
        
    def generate_tasks(self, r):
        tasks = []
        if (r.name == "dingstuff"):
            if not self.beliefs.believes(FakeLogicObject("stuff")):
                self.tasks.append(FakeLogicObject("make_ding"))
        return tasks
        
    def want_to_accept(self, r):
        return True
         
 
class DingStuffResponsibility(Responsibility):
    def __init__(self):
        super().__init__("dingstuff")
        self.addSuccess(FakeLogicObject("stuff"))
        self.addContinuation(DingStuffContinuation())
        
 
class DingStuffContinuation(Continuation):
    def __init__(self):
        super().__init__()
        self.addCondition(FakeLogicObject("stuff"))
        
    def getContinuation(self):
        r = DingStuffResponsibility()
        return [r]
