from responsibility_agent import Responsibility, Continuation, FakeLogicObject

class GreenTasks(Responsibility):
    def __init__(self):
        super().__init__("green_tasks")
        self.addContinuation(GreenTaskContinuation)
        self.addAllSuccesses()
        self.addAllSubFailures()
        
