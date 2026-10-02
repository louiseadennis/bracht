from responsibility_agent import Responsibility, Continuation, FakeLogicObject

class GreenTask(Responsibility):
    def __init__(self):
        super().__init__("green_tasks")
        self.addContinuation(GreenTaskContinuation())
        self.addAllSubFailures()
        self.agents = ["green"]
        
    # faking this because we don't have sophisticated logical reasonnig
    def get_continuations(self, beliefs):
        output = super().get_continuations(beliefs)

        for c in self.continuations:
            if isinstance(c, GreenTaskContinuation):
                for b in beliefs.beliefs:
                    if self.is_green(b):
                        for r in c.getGreenContinuation(b):
                            output.append(r)
        return output
        
    def is_green(self, b):
        if b.name.startswith("green_task"):
            return True
        else:
            return False
            
        
class SpecificGreenTask(Responsibility):
    def __init__(self, task_name):
        super().__init__(task_name)
        done = FakeLogicObject("done_" + task_name)
        self.addSuccess(done)
        # need to figure out what the continuations are.
        

class GreenTaskContinuation(Continuation):
    def __init__(self):
        super().__init__()
        # Not that if all conditions hold then the continuation returns
        #self.addCondition(there is a green task)
        
    def getGreenContinuation(self, b):
        print("generating new reponsibilty")
        r = SpecificGreenTask(b.name)
        return [r]
        

