from responsibility_agent import Responsibility, Continuation, FakeLogicObject

class Task(Responsibility):
    def __init__(self, colour):
        super().__init__(colour + "_tasks")
        self.colour = colour
        self.addContinuation(TaskContinuation())
        self.addAllSubFailures()
        self.agents = [colour]
        
        # faking this because we don't have sophisticated logical reasonnig
    def get_continuations(self, beliefs):
        output = super().get_continuations(beliefs)

        for c in self.continuations:
            if isinstance(c, TaskContinuation):
                for b in beliefs.beliefs:
                    if self.is_colour(b, self.colour):
                        for r in c.getTaskContinuation(b, self.colour):
                            output.append(r)
        return output
        
    def is_colour(self, b, colour):
        if b.name.startswith(colour):
            return True
        else:
            return False
            
class TaskContinuation(Continuation):
    def __init__(self):
        super().__init__()
        # Not that if all conditions hold then the continuation returns
        #self.addCondition(there is a green task)
        
    def getTaskContinuation(self, b, colour):
        print("generating new reponsibilty")
        r = SpecificTask(b.name, colour)
        return [r]


class GreenTask(Task):
    def __init__(self):
        super().__init__("green")

            
        
class SpecificTask(Responsibility):
    def __init__(self, task_name, colour):
        super().__init__(task_name)
        done = FakeLogicObject("done_" + task_name)
        self.addSuccess(done)
        self.colour = colour
        # need to figure out what the continuations are.
        
    def getColour(self):
        return self.colour
        


        

