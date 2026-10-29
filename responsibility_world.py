from responsibility_agent import *

class responsibility_world:
    def __init__(self):
        self.perceptions = []
        self.agent_perceptions = {}
        self.messages = []
        self.iterations = 0
        self.agents = []
        self.output_level = 5

    def run(self):
        self.iterations = 0
        while self.iterations < self.total_iterations:
            self.update_perceptions()
            self.messages = []
            self.cycle_agents()
            self.iterations = self.iterations + 1;
        self.on_end()
            
    def cycle_agents(self):
        stage = 0
        while stage < 5:
            actual_stage = stage % 5;
            self.print_stage(actual_stage)
            for agent in self.agents:
                agent.process_stage(actual_stage)
                agent.print_agent(actual_stage, self.output_level)
            
            if (self.interactive):
                input("Next Stage?")
            stage = stage + 1
            
    def print_level(self, string, output_level=None):
        if output_level is not None:
            if self.output_level > output_level:
                print(string)
        else:
            if self.output_level > 0:
                print(string)

            
    def on_end(self):
        print("Completed " + str(self.iterations) + " iterations.")
    
    def print_stage(self, stage):
        if (stage == 0):
            self.print_level("stage 1 - What are the Agents and Responsibilities?")
        elif (stage == 1):
            self.print_level("stage 2 - Assign Responsibilities")
        elif (stage == 2):
            self.print_level("stage 3 - Generate Tasks")
        elif (stage == 3):
            self.print_level("stage 4 - Do Tasks")
        elif (stage == 4):
            self.print_level("stage 5 - Get Input")
            
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
        
    def update_perceptions(self):
        return
        
    def remove_perception(self, string):
        for p in self.perceptions:
            if (p.name == string):
                self.perceptions.remove(p)
                
    def agent_names(self):
        agent_names = []
        for a in self.agents:
            agent_names.append(a.name)
        return agent_names

