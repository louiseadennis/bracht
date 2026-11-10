import sys
import random
sys.path.insert(0, '../..')

#base line experiments.  Agents only do their own task.

from task_world_generic import *
from responsibility_agent import FakeLogicObject
from base_task_agent import TaskAgent

class task_world_base(task_world_generic):
    def __init__(self, seed, output_file):
        super().__init__(seed, output_file)
        
        #Add basic task agents, able only to do own colour tasks
        self.green_task_agent = TaskAgent(self, "green", "green")
        self.green_task_agent.setOutputLevel(self.output_level)
        self.red_task_agent = TaskAgent(self, "red", "red")
        self.red_task_agent.setOutputLevel(self.output_level)
        self.blue_task_agent = TaskAgent(self, "blue", "blue")
        self.blue_task_agent.setOutputLevel(self.output_level)
        self.agents = [self.green_task_agent, self.red_task_agent, self.blue_task_agent]
        self.tasks = {}


if __name__ == "__main__":
    task_world_base.run_experiment(sys.argv[1])
 
