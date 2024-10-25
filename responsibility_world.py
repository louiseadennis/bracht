from responsibility_agent import *

class responsibility_world:
    def __init__(self):
        self.perceptions = []
        self.messages = []
        self.iterations = 0

    def run(self):
        iterations = 0
        while self.iterations < self.total_iterations:
            self.update_perceptions()
            self.messages = []
            self.cycle_agents()
            self.iterations = self.iterations + 1;
            
    def cycle_agents(self):
        stage = 0
        while stage < 5:
            actual_stage = stage % 5;
            for agent in self.agents:
                agent.process_stage(actual_stage)
                agent.print_agent()
            
            if (self.interactive):
                input("Next Stage?")
            stage = stage + 1
            
    def do(self, agent, task):
        if (task.name == "broadcast"):
            self.messages.append(task.message)
            
    def get_percepts(self, agent):
        return self.perceptions
        
    def get_messages(self, agent):
        return self.messages

