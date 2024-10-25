import sys
sys.path.insert(0, '../..')

from responsibility_agent import *
from dingstuff_agent import DingStuffAgent

class dingstuff_world:
    def __init__(self):
        agent = DingStuffAgent(self)
        self.total_iterations = 2
        self.perceptions = []
        self.messages = []

        self.agents = [agent]

    def run(self):
        iterations = 0
        while iterations < self.total_iterations:
            self.peceptions = []
            self.messages = []
            self.cycle_agents()
            iterations = iterations + 1;
            
    def cycle_agents(self):
        stage = 0
        while stage <= 5:
            actual_stage = stage % 5;
            # print(actual_stage)
            for agent in self.agents:
                agent.process_stage(actual_stage)
                agent.print_agent()
                
            input("Next Stage?")
            stage = stage + 1
            

           
    def do(self, agent, task):
        if (task.name == "make_ding"):
            print("DING")
            self.perceptions.append(FakeLogicObject("stuff"))
        if (task.name == "broadcast"):
            self.messages.append(task.message)
            
    def get_percepts(self, agent):
        return self.perceptions
        
    def get_messages(self, agent):
        return self.messages

world = dingstuff_world()
world.run()
