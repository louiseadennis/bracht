import sys
sys.path.insert(0, '../..')

from responsibility_world import *
from responsibility_agent import *
from dingstuff_agent import DingStuffAgent

class dingstuff_world(responsibility_world):
    def __init__(self):
        super().__init__()
        agent = DingStuffAgent(self)
        self.total_iterations = 5
        self.interactive = True

        self.agents = [agent]
           
    def do(self, agent, task):
        if (task.name == "make_ding"):
            print(agent.name + " did DING")
            self.perceptions.append(FakeLogicObject("stuff"))
        if (task.name == "broadcast"):
            self.messages.append(task.message)
            
world = dingstuff_world()
world.run()
