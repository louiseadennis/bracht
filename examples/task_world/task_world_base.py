import sys
import random
sys.path.insert(0, '../..')

from responsibility_world import *
from responsibility_agent import FakeLogicObject
from base_task_agent import TaskAgent

class task_world_base(responsibility_world):
    def __init__(self):
        super().__init__()
        self.interactive = True
        self.task_count = 0
        #Note this means we always add a task - may want to drop that later
        self.green_prob = 1
        self.red_prob = 2
        self.blue_prob = 3
        self.total_iterations = 10
        random.seed(42)
        green_task_agent = TaskAgent(self, "green", "green")
        self.agents = [green_task_agent]
        self.tasks = {}
        
    def update_perceptions(self):
        n = random.randint(1, 10)
        if (n <= self.green_prob):
            self.add_percept(f'green_task_{self.task_count}')
            print(f'Adding green task {self.task_count}')
            self.task_count = self.task_count + 1
        n = random.randint(1, 10)
        if (n <= self.red_prob):
            self.add_percept(f'red_task_{self.task_count}')
            print(f'Adding red task {self.task_count}')
            self.task_count = self.task_count + 1
        n = random.randint(1, 10)
        if (n <= self.blue_prob):
            self.add_percept(f'blue_task_{self.task_count}')
            print(f'Adding blue task {self.task_count}')
            self.task_count = self.task_count + 1

    
            # def do(self, agent, task):
        # TO DO: make these have durations but for now keep simple
               #  self.remove_percept(task)
    
    def add_percept(self, string):
        self.perceptions.append(FakeLogicObject(string))
        
    def remove_percept(self, string):
        self.remove_perception(string)
        
    def do(self, agent, task):
        if task.name.startswith(agent.getColour()):
            print(agent.name + " did " + task.name)
            if task.name in self.tasks:
                self.tasks[task.name] += 1
            else:
                self.tasks[task.name] = 1
            
            if self.tasks[task.name] >= 5:
                self.remove_percept(task.name)
                self.add_percept("done_" + task.name)
                del self.tasks[task.name]
        else:
            super().do(agent, task)
        
world = task_world_base()
world.run()
