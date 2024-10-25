from responsibility_agent import Responsibility, Continuation, FakeLogicObject

# Name: clean spill,
# Sub Responsibilities: {},
# Success Condition?: no spill within 10 minutes of notification,
# Fail Condition: still a spill within 10 minutes of notification
# Conrinuation: {notify health and safety agent if failed},
# Default Agents: {cleaning robots}

class CleanSpill(Responsibility):
    def __init__(self):
        super().__init__("clean_spill")
        not_spill = FakeLogicObject("not_spill")
        self.addSuccess(not_spill)
        spill = FakeLogicObject("spill_10")
        self.addFailure(spill)
        self.addContinuation(CleanSpillFailContinuation())
        self.addContinuation(CleanSpillSuccessContinuation())
        self.agents = ["cleaning agent"]
        
class CleanSpillFailContinuation(Continuation):
    def __init__(self):
        super().__init__()
        spill = FakeLogicObject("spill_10")
        self.addCondition(spill)
        
    def getContinuation(self):
        print("generating notify responsibility")
        r = NotifyHealthAndSafety()
        return [r]
        
class CleanSpillSuccessContinuation(Continuation):
    def __init__(self):
        super().__init__()
        spill = FakeLogicObject("not_spill")
        self.addCondition(spill)
        
    def getContinuation(self):
        print("returning clean spill")
        r = CleanSpill()
        return [r]

class NotifyHealthAndSafety(Responsibility):
    def __init__(self):
        super().__init__("notify")
        self.addSuccess(FakeLogicObject("notified"))
