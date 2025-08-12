from responsibility_agent import ResponsibilityAgent, FakeLogicObject
from care_home_responsibilities import CleanSpill

class CleaningAgent(ResponsibilityAgent):
    def __init__(self, env, name):
        super().__init__(name, env)
        self.addResponsibility(CleanSpill())
        self.dgc["clean_spill"] = ["cleaner1","cleaner2"]
        self.dgc["notify"] = ["cleaner1","cleaner2"]
        
    def generate_tasks(self, r):
        tasks = []
        if (r.name == "notify"):
            self.tasks.append(FakeLogicObject("notify"))
        elif (r.name == "clean_spill" and self.i_believe("spill")):
            self.tasks.append(FakeLogicObject("clean"))
        elif (r.name == "clean_spill" and self.i_believe("spill_stairs") and self.name == "cleaner1" and self.i_believe("at_stairs_cleaner_1")):
            self.tasks.append(FakeLogicObject("clean"))
        elif (r.name == "clean_spill" and self.i_believe("spill_stairs") and self.name == "cleaner1" and not "cleaner2" in r.assigned and not self.i_believe("broken_cleaner_1")):
            self.tasks.append(FakeLogicObject("move_stairs"))
        elif (r.name == "clean_spill" and self.i_believe("spill_stairs") and self.name == "cleaner2" and self.i_believe("at_stairs_cleaner_2")):
            self.tasks.append(FakeLogicObject("clean"))
        elif (r.name == "clean_spill" and self.i_believe("spill_stairs") and self.name == "cleaner2" and not "cleaner1" in r.assigned):
            self.tasks.append(FakeLogicObject("move_stairs"))
        elif (r.name == "clean_spill" and self.i_believe("spill_hall") and self.name == "cleaner1" and self.i_believe("at_hall_cleaner_1")):
            self.tasks.append(FakeLogicObject("clean"))
        elif (r.name == "clean_spill" and self.i_believe("spill_hall") and self.name == "cleaner2" and self.i_believe("at_stairs_cleaner_2")):
            self.tasks.append(FakeLogicObject("clean"))
        elif (r.name == "clean_spill" and self.i_believe("spill_stairs") and self.nearest_to("stairs")) and (self.name == "cleaner2" or not self.i_believe("broken_cleaner_1")):
            self.tasks.append(FakeLogicObject("move_stairs"))
        elif (r.name == "clean_spill" and self.i_believe("spill_hall") and self.nearest_to("hall")):
            self.tasks.append(FakeLogicObject("move_hall"))
        return tasks
        
    def i_believe(self, string):
         if (self.beliefs.believes(FakeLogicObject(string))):
            return True
            
    def want_to_accept(self, r_name):
        return True
            
    def update_dgc(self, percepts):
        if (FakeLogicObject("broken_cleaner_1") in percepts and self.name == "cleaner1"):
            new_dgc = []
            for c in self.dgc.get("clean_spill"):
                if (c != "cleaner1"):
                    new_dgc.append(c)
            self.dgc["clean_spill"] = new_dgc
        self.print_dgc()
        
    def nearest_to(self, location):
        if (location == "stairs"):
            if (self.name == "cleaner1"):
                if (self.i_believe("at_stairs_cleaner_1")):
                    return True
                elif (self.i_believe("near_stairs_cleaner_1") and not self.i_believe("at_stairs_cleaner_2")):
                    return True
                elif (self.i_believe("middle_cleaner_1") and not self.i_believe("at_stairs_cleaner_2") and not self.i_believe("near_stairs_cleaner_2")):
                    return True
                elif (self.i_believe("near_hall_cleaner_1") and (self.i_believe("near_hall_cleaner_2") or self.i_believe("at_hall_cleaner_2"))):
                    return True
                elif (self.i_believe("at_hall_cleaner_1") and self.i_believe("at_hall_cleaner_2")):
                    return True
                else:
                    return False
            else:
                if (self.i_believe("at_stairs_cleaner_2")):
                    return True
                elif (self.i_believe("near_stairs_cleaner_2") and not self.i_believe("at_stairs_cleaner_1")):
                    return True
                elif (self.i_believe("middle_cleaner_2") and not self.i_believe("at_stairs_cleaner_1") and not self.i_believe("near_stairs_cleaner_1")):
                    return True
                elif (self.i_believe("near_hall_cleaner_2") and (self.i_believe("near_hall_cleaner_1") or self.i_believe("at_hall_cleaner_1"))):
                    return True
                elif (self.i_believe("at_hall_cleaner_2") and self.i_believe("at_hall_cleaner_1")):
                    return True
                else:
                    return False
        else:
            if (self.name == "cleaner1"):
                if (self.i_believe("at_hall_cleaner_1")):
                    return True
                elif (self.i_believe("near_hall_cleaner_1") and not self.i_believe("at_hall_cleaner_2")):
                    return True
                elif (self.i_believe("middle_cleaner_1") and not self.i_believe("at_hall_cleaner_2") and not self.i_believe("near_hall_cleaner_2")):
                    return True
                elif (self.i_believe("near_stairs_cleaner_1") and (self.i_believe("near_stairs_cleaner_2") or self.i_believe("at_stairs_cleaner_2"))):
                    return True
                elif (self.i_believe("at_stairs_cleaner_1") and self.i_believe("at_stairs_cleaner_2")):
                    return True
                else:
                    return False
            else:
                if (self.i_believe("at_hall_cleaner_2")):
                    return True
                elif (self.i_believe("near_hall_cleaner_2") and not self.i_believe("at_hall_cleaner_1")):
                    return True
                elif (self.i_believe("middle_cleaner_2") and not self.i_believe("at_hall_cleaner_1") and not self.i_believe("near_hall_cleaner_1")):
                    return True
                elif (self.i_believe("near_stairs_cleaner_2") and (self.i_believe("near_stairs_cleaner_1") or self.i_believe("at_stairs_cleaner_1"))):
                    return True
                elif (self.i_believe("at_stairs_cleaner_2") and self.i_believe("at_stairs_cleaner_1")):
                    return True
                else:
                    return False
                    
# Grumpy Cleaning Agents don't accept responsibility for things unless forced upon them
class GrumpyCleaningAgent(CleaningAgent):
    def __init__(self, env, name):
        super().__init__(env, name)
        
    def want_to_accept(self, r_name):
        return False
