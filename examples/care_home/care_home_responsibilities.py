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
        self.agents = ["cleaner1", "cleaner2"]
        
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

# Name: notify,
# Sub Responsibilities: {},
# Success Condition?: none
# Fail Condition: none
# Conrinuation: {},
# Default Agents: {}
class NotifyHealthAndSafety(Responsibility):
    def __init__(self):
        super().__init__("notify")
        self.addSuccess(FakeLogicObject("notified"))

# Name: keep_cleaning,
# Sub Responsibilities: {},
# Success Condition?: no spill
# Fail Condition: none
# Conrinuation: {},
# Default Agents: {}


# Name: health_and_safety,
# Sub Responsibilities: [ensure_no_spills],
# Success Condition: all sub-responsibilities sucessful
# Fail Condition: a sub-responsibility fails
# Continuation: {generate_report},
# Default Agents: {health_and_safety_agent}
class HealthAndSafety(Responsibility):
    def __init__(self):
        super().__init__("health_and_safety")
        self.addResponsibility(EnsureNoSpills())
        self.addContinuation(HealthandSafetyFailContinuation())
        self.addContinuation(HealthandSafetySuccessContinuation())
        self.addAllSubSuccesses()
        self.addAllSubFailures()
        self.agents = ["coordinator"]

class HealthandSafetyFailContinuation(Continuation):
    def __init__(self):
        super().__init__()
        spill = FakeLogicObject("notified")
        self.addCondition(spill)
        
    def getContinuation(self):
        print("generating report responsibility")
        r = GenerateReport()
        return [r]
        
class HealthandSafetySuccessContinuation(Continuation):
    def __init__(self):
        super().__init__()
        
    def getContinuation(self):
        r = HealthAndSafety()
        return [r]

class GenerateReport(Responsibility):
    def __init__(self):
        super().__init__("generate_report")
        self.addSuccess(FakeLogicObject("reported"))


# Name: ensure_no_spills,
# Sub Responsibilities: [],
# Success Condition: not_spill
# Fail Condition: notify
# Continuation: {ensure_continued_cleaning_attempts},
# Default Agents: {}
class EnsureNoSpills(Responsibility):
    def __init__(self):
        super().__init__("ensure_no_spills")
        not_spill = FakeLogicObject("not_spill")
        self.addSuccess(not_spill)
        spill = FakeLogicObject("notified")
        self.addFailure(spill)
        self.addContinuation(ContinueCleaningAttemptsContinuation())
        self.agents = ["coordinator"]
        
class ContinueCleaningAttemptsContinuation(Continuation):
    def __init__(self):
        super().__init__()
        spill = FakeLogicObject("notified")
        self.addCondition(spill)
        
    def getContinuation(self):
        print("tell cleaners to keep trying")
        r = EnsureContinueCleaning()
        return [r]

# Name: ensure_continued_cleaning_attmpts,
# Sub Responsibilities: [],
# Success Condition: not_spill
# Fail Condition:
# Continuation: {},
# Default Agents: {}
class EnsureContinueCleaning(Responsibility):
    def __init__(self):
        not_spill = FakeLogicObject("not_spill")
        self.addSuccess(not_spill)

