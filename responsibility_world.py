from responsibility_agent import *

class responsibility_world:
    def __init__(self):
        self.perceptions = []
        self.agent_perceptions = {}
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
            self.print_stage(actual_stage)
            for agent in self.agents:
                agent.process_stage(actual_stage)
                agent.print_agent(actual_stage)
            
            if (self.interactive):
                input("Next Stage?")
            stage = stage + 1
    
    def print_stage(self, stage):
        if (stage == 0):
            print("stage 1 - What are the Responsibilities?")
        elif (stage == 1):
            print("stage 2 - Assign Responsibilities")
        elif (stage == 2):
            print("stage 3 - Generate Tasks")
        elif (stage == 3):
            print("stage 4 - Do Tasks")
        elif (stage == 4):
            print("stage 5 - Get Input")
            
    def do(self, agent, task):
        if (task.name == "broadcast"):
            self.messages.append(task.message)
            
    def get_percepts(self, agent):
        agent_perceptions = self.agent_perceptions.get(agent.name)
        perceptions = self.agent_perceptions
        if (agent_perceptions):
            perceptions += agent_perceptions
        return self.perceptions
        
    def get_messages(self, agent):
        return self.messages

