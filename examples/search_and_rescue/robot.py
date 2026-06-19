from responsibility_agent import ResponsibilityAgent, FakeLogicObject
from search_and_rescue_resposibilities import Scout, ClearRubble, Rescue

# NB.  In some worlds the cleaners are cleaner1 and cleaner2 and some they are called cleanerA and cleanerB - at the moment this seems to work but is obviously messy.
class RobotAgent(ResponsibilityAgent):
    def __init__(self, env, name):
        super().__init__(name, env)
        self.dgc["scout"] = []
        self.dgc["clear_rubble"] = []
        self.dgc["rescue"] = []
        
    def generate_tasks(self, r):
        tasks = []
 
    def i_believe(self, string):
         if (self.beliefs.believes(FakeLogicObject(string))):
            return True
            
    def want_to_accept(self, r_name):
        return False
        
    def do_not_want_to_accept(self, r_name):
        return False
            
    def update_dgc(self, percepts):
        self.print_dgc()
        
  
