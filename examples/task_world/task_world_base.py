import sys
import random
sys.path.insert(0, '../..')

from responsibility_world import *
from responsibility_agent import FakeLogicObject
from base_task_agent import TaskAgent

class task_world_base(responsibility_world):
    def __init__(self, seed, output_file):
        super().__init__()
        self.interactive = False
        self.task_count = 0
        #Note this means we always add a task - may want to drop that later
        self.green_prob = 1
        self.red_prob = 2
        self.blue_prob = 3
        self.total_iterations = 100
        random.seed(seed)
        self.output_level = 0
        self.output_file = output_file
        
        green_task_agent = TaskAgent(self, "green", "green")
        green_task_agent.setOutputLevel(self.output_level)
        red_task_agent = TaskAgent(self, "red", "red")
        red_task_agent.setOutputLevel(self.output_level)
        blue_task_agent = TaskAgent(self, "blue", "blue")
        blue_task_agent.setOutputLevel(self.output_level)
        self.agents = [green_task_agent, red_task_agent, blue_task_agent]
        self.tasks = {}
        
    def on_end(self):
        blue_count = 0
        red_count = 0
        green_count = 0
        for percept in self.perceptions:
            if percept.name.startswith("blue"):
                blue_count = blue_count + 1
                
            if percept.name.startswith("red"):
                red_count = red_count + 1
                
            if percept.name.startswith("green"):
                green_count = green_count + 1
                
        with open(self.output_file, "a") as f:
            f.write(str(green_count) + ",")
            f.write(str(red_count) + ",")
            f.write(str(blue_count) + "\n")
        print(self.output_file)
        print("Green: " + str(green_count))
        print("Red: " + str(red_count))
        print("Blue: " + str(blue_count))
        
    def update_perceptions(self):
        n = random.randint(1, 10)
        if (n <= self.green_prob):
            self.add_percept(f'green_task_{self.task_count}')
            self.print_level(f'Adding green task {self.task_count}')
            self.task_count = self.task_count + 1
        n = random.randint(1, 10)
        if (n <= self.red_prob):
            self.add_percept(f'red_task_{self.task_count}')
            self.print_level(f'Adding red task {self.task_count}')
            self.task_count = self.task_count + 1
        n = random.randint(1, 10)
        if (n <= self.blue_prob):
            self.add_percept(f'blue_task_{self.task_count}')
            self.print_level(f'Adding blue task {self.task_count}')
            self.task_count = self.task_count + 1
    
    def add_percept(self, string):
        self.perceptions.append(FakeLogicObject(string))
        
    def remove_percept(self, string):
        self.remove_perception(string)
        
    def do(self, agent, task):
        if task.name.startswith("red") or task.name.startswith("blue") or task.name.startswith("gree"):
            self.print_level(agent.name + " did " + task.name)
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
        
seeds = list(range(100))
for seed in seeds:
    world = task_world_base(seed, sys.argv[1])
    world.run()
