from responsibility_agent import ResponsibilityAgent, FakeLogicObject
from task_world_responsibilities import Task, SpecificTask

class TaskAgentAnyColour(TaskAgent):
    def __init__(self, env, name, colour1, colour2, colour3):
        super().__init__(name, env, name, colour1)
        self.colours = [colour1, colour2, colour3]
        self.addResponsibility(Task(colour2))
        self.addResponsibility(Task(colour3))
        self.dgc[colour2 + "_tasks"] = [name]
        self.dgc[colour3 + "_tasks"] = [name]
        self.current_colour_tasks = []
  
        

