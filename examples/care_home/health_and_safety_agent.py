from responsibility_agent import ResponsibilityAgent, FakeLogicObject, Broadcast, Delegate
from care_home_responsibilities import HealthAndSafety

class HealthAndSafetyAgent(ResponsibilityAgent):
    def __init__(self, env, name):
        super().__init__(name, env)
        self.addResponsibility(HealthAndSafety())
        self.dgc["clean_spill"] = ["cleanerA","cleanerB"]
        self.dgc["notify"] = ["cleanerA","cleanerB"]
        self.dgc["health_and_safety"] = ["coordinator"]
        self.dgc["ensure_no_spills"] = ["coordinator"]
        self.dgc["generate_report"] = ["coordinator"]
        for r in self.responsibilities:
            print("      " + r.name)

    def generate_tasks(self, r):
        tasks = []
        if (r.name == "ensure_no_spills" and self.i_believe("spill_stairs")):
            self.tasks.append(Broadcast(Delegate("coordinator", "clean_spill", "cleanerA")))
        return tasks
        
    def i_believe(self, string):
         if (self.beliefs.believes(FakeLogicObject(string))):
            return True
            
    def want_to_accept(self, r_name):
        return True
            
