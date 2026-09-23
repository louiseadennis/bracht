from responsibility_agent import Responsibility, Continuation, FakeLogicObject

class GreenTask(Responsibility):
    def __init__(self):
        super().__init__("green_tasks")
        #self.addContinuation(GreenTaskContinuation)
        self.addAllSubSuccesses()
        self.addAllSubFailures()
        
