import sys
import random
sys.path.insert(0, '../..')

from responsibility_world import *
from responsibility_agent import FakeLogicObject

class task_world_base(responsibility_world):
    def __init__(self):
        super().__init__()
        self.interactive = True
        self.task_count = 0
        self.prob = 1
        random.seed(42)
        
    def update_perceptions(self):
        n = random.randint(1, 10)
        if (n <= self.prob):
            n = random.randint(1, 4)
            if (n == 1):
                self.add_percept('green_task_{self.task_count}')
            if (n == 2):
                self.add_percept('red_task_{self.task_count}')
            if (n == 3):
                self.add_percept('blue_task_{self.task_count}')
            if (n == 4):
                self.add_percept('yellow_task_{self.task_count}')
            self.task_count = self.task_count + 1
    
    
    
    def add_percept(self, string):
        self.perceptions.append(FakeLogicObject(string))
        
    def remove_percept(self, string):
        self.remove_perception(string)
