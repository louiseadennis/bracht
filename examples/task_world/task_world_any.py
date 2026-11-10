import sys
import random
sys.path.insert(0, '../..')

#base line experiments.  Agents only do their own task.

from task_world_generic import *
from responsibility_agent import FakeLogicObject
from base_task_agent import TaskAgent

class task_world_any(task_world_generic):
    def __init__(self, seed, output_file):
        super().__init__(seed, output_file)
        self.output_level = 5
        self.interactive = True
        
        self.green_task_agent = TaskAgent(self, "green", "green")
        self.green_task_agent.setOutputLevel(self.output_level)
        self.red_task_agent = TaskAgent(self, "red", "red")
        self.red_task_agent.setOutputLevel(self.output_level)
        self.blue_task_agent = TaskAgent(self, "blue", "blue")
        self.blue_task_agent.setOutputLevel(self.output_level)

        self.green_task_agent.add_dgc("blue")
        self.green_task_agent.add_dgc("red")
        self.blue_task_agent.add_dgc("red")
        self.blue_task_agent.add_dgc("green")
        self.red_task_agent.add_dgc("blue")
        self.red_task_agent.add_dgc("green")
        self.green_task_agent.add_colour("blue")
        self.green_task_agent.add_colour("red")
        self.red_task_agent.add_colour("blue")
        self.red_task_agent.add_colour("green")
        self.blue_task_agent.add_colour("green")
        self.blue_task_agent.add_colour("red")
        
        self.agents = [self.green_task_agent, self.red_task_agent, self.blue_task_agent]
        self.tasks = {}




if __name__ == "__main__":
    task_world_any.run_experiment(sys.argv[1])
 
