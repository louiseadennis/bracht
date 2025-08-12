class ResponsibilityAgent:
    def __init__(self, n, env):
        self.name = n
        self.beliefs = BeliefBase()
        self.responsibilities = []
        self.hierarchy = {}
        self.dgc = {}  # responsibilities as keys, list of agents with dgc as values
        self.tasks = []
        self.world = env
        
    def process_stage(self, stage):
        if (stage == 0):
        # At the start of step one the agent state is <B, R, A, C, H, T>.
        # At this point in the cycle T should be the empty set.
        # The agent needs to understand which responsibilities have succeeded or failed this depends upon its success and failure conditions - these may refer to its sub-responsibilities (e.g., a responsibility may fail if any sub-responsibility fails or if all sub-responsibilities fail and so on, depending upon the responsibility).
        # Let OR be the set of responsibilities that have succeeded or failed:
        # OR = {r | r \in R \land  r = <name, Sub, SC, FC, Cont, N> \land (B |= SC \or B |= FC)}
        # We then generate new responsibilities from the continuation:
        # NR = {r | \exists res \in OR.  res = <name, Sub, SC, FC, Cont, N> \land exists <C, R> \in Cont.  B |= C \land r \in R}
        # After Step 1 the responsibility model <B, R, A, C, H, T> becomes <B, R  \cup NR/OR, A, C, H, T>
        # Note: There may be responsibilities that never succeed or fail because they always hold - e.g., health and safety.

            new_r = []
            for r in self.getHighLevelResponsibilities():
                if (not r.succeed_or_fail(self.beliefs)):
                    new_r.append(r)
                    
                # At this point new_r is OR from theory
                 
                # Note this is a change from the theory in the word doc to avoid proliferation of responsibilities - this because health and safety has not clear success condition
                if r.succeed_or_fail(self.beliefs):
                    for res in r.get_continuations(self.beliefs):
                        new_r.append(res)
                    
                # new_r should now be NR
            self.responsibilities = new_r
        elif (stage == 1):
        
        # At the start of step two the agent state is <B, R, A, C, H, T>. T is the empty set.
        # In this stage the agent reasons about who has accepted each responsibility.   We treat A as a mapping from responsibilities to the set of the agents who are responsible for that responsibility.
        # We may have received messages from other agents (stored in our beliefs) about which responsibilities they have accepted, which they have delegated, any responsibilities they do not have dispositional guidance control for and so on.   These messages have been used to update the agent's beliefs, C mapping and so on (see Step 5).
        # Definition.  Given a responsibility model, RM = <B, R, A, C, H, T>  the default assignment of a responsibility in RM is
        # default_assignment(<name, Sub, SC, FC, Contl, N>) = {a | a \in N(B) \land (a, r) \in C})
        # The default assignment for a responsibility is the set of agents dictated by the norms associated with the responsibility unless we believe they do not have dispositional guidance control for that responsibility.  Note that N is a function from the beliefs to a set of agents.  This allows us to model, for instance, that the agent who finds a hazard is responsible for handling that hazard.
        # We update our assignment set with the default assignments:
        # Let A_1 be such that
        # A_1 = A \cup \{(r, a) | r \in R \land a \in default_assignment(r)\}

        # Then we update everything based on accept, not accept and delegate messages.
        # Let A_2 be such that
        # A_2 = A_1 \cup \{(r, a) | r \in R \land ( B |-accepts(a, r) \lor \exists a_1. (B |- delegate(r, a_1, a) \land (a_1, a) \in H) )\} / \{(a, r) | r \in R \land B |- not accepts(a, r)\}
        # Note that we allow agents to accept responsibilities even if we do not believe they have dispositional guidance control (this essentially means an agent trusts another agent's own knowledge of its capabilities to be more up-to-date/accurate.)
        # This means A_2(r) includes all agents who have explicitly accepted the responsibility, agents who have been delegated by the responsibility by someone this agent thinks has the right to do so and excludes all agents who have explicitly not accepted the responsibility and any agents who the agent previously thought were assigned the responsibility (if they have not signalled either way that they have accepted or rejected it - i.e., because it was assigned to them by the default norm or delegated to them by an authority agent).

        # Let
        # U = {r | A_2(r) = \emptyset}
        # U is the set of currently unassigned responsibilities after considering what all other agents have told us and the norms.
        # The agent must now consider whether it can accept responsibility for any of these unassigned responsibilities.
        # Let Accepted = {r | r \in U \land (self, r) \in C }
        # A_3 = A_2 \cup \{(self, r) | r \in Accepted\}

        # Lastly the agent assigns to itself the tasks to broadcast which responsibilities it has accepted (or not accepted?)
        # BT = \{broadcast(accept(self, r)) | r \in R \land self \in A_4(r) \}
        # After Step 2 the responsibility model <B, R, A, C, H, T> becomes <B, R, A_3, C, H, T \cup BT>

            for r in self.getAllResponsibilities():
                # print(self.name + " considering assigning " + r.name)
                if (not r.assigned):
                    for a in r.default_agents(self.beliefs):
                        if (a in self.dgc.get(r.name)):
                                                    # print(a + " gets it by default")
                            r.assigned.append(a)
                    # r is in A_1 above
                for a in r.assigned:
                    if (not a in self.dgc.get(r.name)):
                                                # print(a + " can't manage it")
                        r.assigned.remove(a)
                    
                for a in self.beliefs.accept(r):
                    if (not a in r.assigned):
                                                # print(a + " has accepted it")
                        r.assigned.append(a)
                for a in self.beliefs.delegated_to(r):
                    if (not a in r.assigned):
                                                # print(a + " has been delegated it")
                        r.assigned.append(a)
                for a in self.beliefs.not_accept(r):
                                            # print(a + " has refused it")
                    r.assigned.remove(a)
                # for these three r was in A_2 above
                
                if (not r.assigned):
                    # r was in U
                    if (self.dgc.get(r.name) and self.name in self.dgc.get(r.name) and self.want_to_accept(r.name)):
                        r.assigned.append(self.name)
                        # r is in A_3 above
                                                # print(self.dgc.get(r.name))
                                                # print("assigning to self")
                        self.tasks.append(Broadcast(Accept(self.name, r.name)))
                        # Add to BT
        elif (stage == 2):
            for r in self.getAllResponsibilities():
                if self.name in r.assigned:
                    self.tasks = self.tasks + self.generate_tasks(r)
            self.tasks.append(Broadcast(State(self.name, self.responsibilities, self.dgc)))
        elif (stage == 3):
            for task in self.tasks:
                self.world.do(self, task)
            self.tasks = []
        elif (stage == 4):
            percepts = self.world.get_percepts(self)
            messages = self.world.get_messages(self)
            
            for belief in percepts:
                if (not self.beliefs.believes(belief)):
                    self.beliefs.add(belief)
                    
            for belief in self.beliefs.beliefs:
                found = False
                for b in percepts:
                    if (b.name == belief.name):
                        found = True
                if (not found):
                    self.beliefs.beliefs.remove(belief)
            
            for message in messages:
                print(message.name)
                if (message.name == "accept"):
                    self.beliefs.add(message)
                    if (self.beliefs.not_accepted.get(message.responsibility) and message.agent in self.beliefs.not_accepted[message.responsibility]):
                        self.beliefs.not_accepted[message.responsibility].remove(message.agent)
                if (message.name == "not_accept"):
                    self.beliefs.add(message)
                    if (self.beliefs.not_accepted.get(message.responsibility) and message.agent in self.beliefs.accepted[message.responsibility]):
                        self.beliefs.accepted[message.responsibility].remove(message.agent)
                if (message.name == "delegate"):
                    print("adding delegation")
                    self.beliefs.add(message)
                if (message.name == "state"):
                    for r in message.rs:
                        if not r in self.responsibilities:
                            self.responsibilities.append(r)
                    for c in message.cap:
                        try:
                            if (message.agent in message.cap.get(c) and not message.agent in self.dgc.get(c)):
                                self.dgc[c].append(message.agent)
                                print(self.name + " thinks " + message.agent + " can do " + c)
                        except:
                            if (message.agent in message.cap.get(c)):
                                self.dgc[c] = [message.agent]
                    for c in self.dgc.keys():
                        if (not message.agent in message.cap.get(c) and message.agent in self.dgc.get(c)):
                            self.dgc.get(c).remove(message.agent)
                        
                                
                            
            self.update_dgc(percepts)
            
    # this needs to be overriden by agents - its an internal process
    def update_dgc(self, percepts):
        return
                            
    def addResponsibility(self, r):
        self.responsibilities.append(r)
        
    def getHighLevelResponsibilities(self):
        responsibilities = []
        for r in self.responsibilities:
            responsibilities.append(r)
        return responsibilities

        
    def getAllResponsibilities(self):
        responsibilities = []
        for r in self.responsibilities:
            responsibilities.append(r)
            for sr in r.getSubResponsibilities():
                responsibilities.append(sr)
        return responsibilities
                                    
    def print_agent(self, stage):
        if (stage != 3):
            print(self.name)
        if (stage == 1 or stage == 4):
            self.print_beliefs()
        if (stage == 0 or stage == 4):
            self.print_responsibilities()
        if (stage == 1):
            self.print_assignments()
            self.print_dgc()
        # print("Capabilities:")
        # for x in self.dgc.keys():
        #    print(x + " :: " + str(self.dgc.get(x)))
        # print("Hierarchy:")
        # print(self.hierarchy)
        if (stage == 1 or stage == 2):
            self.print_tasks()
       
    def print_responsibilities(self):
        print("   Responsibilities:")
        for r in self.responsibilities:
            r.print_concise("      ")
            
    def print_beliefs(self):
        print("   Beliefs:")
        self.beliefs.print("      ")
        
    def print_assignments(self):
        print("   Assignments:")
        for r in self.responsibilities:
            print("      " + r.name + " :: " + str(r.assigned))
            
    def print_dgc(self):
        print("   DGC:")
        for r in self.dgc.keys():
            print("      " + r + " :: " + str(self.dgc.get(r)))
            
    def print_tasks(self):
        print("   Tasks:")
        for t in self.tasks:
            t.print("      ")
            
class Responsibility:
    def __init__(self, string):
        self.name = string
        self.sub_responsiblities = []
        self.success_conditions = []
        self.fail_conditions = []
        self.continuations = []
        self.agents = []
        self.assigned = []
        
    def default_agents(self, beliefs):
        return self.agents
                
    def succeed_or_fail(self, beliefs):
        success_outcome = True
        for b in self.success_conditions:
            if (not beliefs.believes(b)):
                success_outcome = False
                break
        if (len(self.success_conditions) == 0):
            success_outcome = False
        if (success_outcome):
            return True
                
        fail_outcome = True
        for b in self.fail_conditions:
            if (not beliefs.believes(b)):
                fail_outcome =  False
                break
                
        if (len(self.fail_conditions) == 0 ):
            fail_outcome = False
                
        
        return fail_outcome;
        
    def get_continuations(self, beliefs):
        output = []
        for c in self.continuations:
            holds = True
            for cond in c.condition:
                if not beliefs.believes(cond):
                    holds = False
                    break
            if holds:
                for r in c.getContinuation():
                    output.append(r)
        return output
                    
    def addSuccess(self, belief):
        self.success_conditions.append(belief)
        
    def addAllSubSuccesses(self):
        for r in self.sub_responsiblities:
            for s in r.getAllSuccesses():
                self.success_conditions.append(s)
                
    def getAllSuccesses(self):
        return self.success_conditions
        
    def addAllSubFailures(self):
        for r in self.sub_responsiblities:
            for f in r.getAllFailures():
                self.fail_conditions.append(f)
                
    def getAllFailures(self):
        return self.fail_conditions
        
    def getSubResponsibilities(self):
        responsibilities = []
        for r in self.sub_responsiblities:
            responsibilities.append(r)
            for sr in r.getSubResponsibilities():
                responsibilities.append(sr)
        return responsibilities
        
    def addFailure(self, belief):
        self.fail_conditions.append(belief)

    def addContinuation(self, continuation):
        self.continuations.append(continuation)
        
    def addResponsibility(self, responsibility):
        self.sub_responsiblities.append(responsibility)
                    
    def print(self):
        print("Name: ")
        print(self.name)
        print("\nSub Responsiblities: [")
        for r in self.sub_responsiblities:
            print(r.name)
            print(", ")
        print("]\nSuccess Conditions:")
        for s in self.success_conditions:
            s.print()
        print("\nFail Conditions:")
        for f in self.fail_conditions:
            f.print()
        print("\nContinuations: ")
        for c in self.continuations:
            c.print()
        print("\nDefault Agents: ")
        
    def print_concise(self, indent):
        print(indent + self.name)
        for r in self.sub_responsiblities:
            r.print_concise(indent + " ")
        
    def __eq__(self, other):
        return self.name == other.name
                    
                    
        
class Continuation:
    def __init__(self):
        self.condition = []
         
    def addCondition(self, criteria):
        self.condition.append(criteria)
        
    def getContinuation():
        return []
        
    def print(self):
        print("continuation")
        
class BeliefBase:
    def __init__(self):
        self.beliefs = []
        self.accepted = {}
        self.not_accepted = {}
        self.delegation = {}
        
    def believes(self, belief):
        for b in self.beliefs:
            if b.name == "accept":
                if b.name in self.accepted.get(b.responsibility):
                    return True
                return False
            if b.name == "not_accept":
                if b.name in self.not_accepted.get(b.responsibility):
                    return True
                return False

            if b.name == belief.name:
                return True
        return False
        
    def doesnt_believe(self, belief):
        for b in self.beliefs:
            if b.name == belief.name:
                return False
        return True
        
    def add(self, belief):
        if (belief.name == "accept"):
            if (belief.responsibility in self.accepted.keys()):
                self.accepted[belief.responsibility].append(belief.agent)
            else:
                self.accepted[belief.responsibility] = [belief.agent]
        elif (belief.name == "not_accept"):
            if (belief.responsibility in self.not_accepted.keys()):
                self.not_accepted[belief.responsibility].append(belief.agent)
            else:
                self.not_accepted[belief.responsibility] = [belief.agent]
        elif (belief.name == "delegate"):
            if (belief.responsibility in self.delegation.keys()):
                self.delegation[belief.responsibility].append([belief.boss, belief.minion])
            else:
                self.delegation[belief.responsibility] = [[belief.boss, belief.minion]]
        else:
            self.beliefs.append(belief)
        
    def print(self, indent):
        if (self.beliefs):
            print(indent + str(self.beliefs))
        if (self.accepted):
            for r in self.accepted:
                print(indent + r + " accepted by:" + str(self.accepted[r]))
        if (self.not_accepted):
            print(indent + "rejected responsibilities:" + self.not_accepted)
        if (self.delegation):
            print(indent + "delegated responsibilities:" + str(self.delegation))
        
    def accept(self,r):
        if (r.name in self.accepted.keys()):
            return self.accepted.get(r.name)
        else:
            return []
            
    def not_accept(self,r):
        if (r.name in self.not_accepted.keys()):
            return self.not_accepted.get(r.name)
        else:
            return []
            
    def delegated_to(self, r):
        if (r.name == self.delegation.keys()):
            minions = []
            for rel in self.delegation.get(r.name):
                minions.append(rel[1])
            return minions
        else:
            return []

class FakeLogicObject:
    def __init__(self, string):
        self.name = string
        self.positive = True
        # We will use time stamp in the belief base to indicate when the belief appeared
        self.time_stamp = None
        # We will use deadline in success conditions to mean - succeeded before and in fail conditions to mean continues after.
        self.deadline = None
        
    def print(self, indent):
        print(indent + self.name)
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name
        
    def __eq__(self, other):
        if self.name == other.name:
            return True
        
class Not(FakeLogicObject):
    def __init__(self, string):
        self.name = string
        self.positive = False
        
    def print(self):
        return ("NOT " + self.name)
        
    def __str__(self):
        return ("NOT " + self.name)
        
    def __repr__(self):
        return ("NOT " + self.name)

class Broadcast(FakeLogicObject):
    def __init__(self, m):
        super().__init__("broadcast")
        self.message = m
        
    def print(self, indent):
        print(indent + self.name + "(" + self.message.toString() + ")")

class Accept(FakeLogicObject):
    def __init__(self, ag, r):
        super().__init__("accept")
        self.agent = ag
        self.responsibility = r
        
    def toString(self):
        return ("accept(" + self.agent + ", " + self.responsibility + ")")
        
class Not_Accept(FakeLogicObject):
    def __init__(self, ag, r):
        super().__init__("not_accept")
        self.agent = ag
        self.responsibility = r

class Delegate(FakeLogicObject):
    def __init__(self, ag1, ag2, r):
        super().__init__("delegate")
        self.boss = ag1
        self.minion = ag2
        self.responsibility = r
        
    def toString(self):
        return ("delegate(" + self.boss + " delegated " + self.responsibility + " to " + self.minion + ")")

        
class State(FakeLogicObject):
    def __init__(self, ag, res, dgc):
        super().__init__("state")
        self.agent = ag
        self.rs = res
        self.cap = dgc
        
    def toString(self):
        return self.name
        
    def print(self):
        print(self.name)
