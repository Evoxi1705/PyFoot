import pygame

##=========================================
class State:
    pass

class Defend(State):
    def Execute(self):
        pass

class Attack(State):
    def Execute(self):
        pass
##=========================================

class Transitions(object):
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):
        pass
##=========================================

class FSM(object):
    def __init__(self, char):
        self.char = char
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.trans = None

    def SetState(self, stateName):
        self.curState = self.states[stateName]

    def Transition(self, transName):
        self.trans = self.transitions[transName]

    def Execute(self):
        if (self.trans):
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.trans = None
        self.curState.Execute()
##=========================================

if __name__ == "__main__":
    bot = EasyBot()

    light.FSM.state["Defending"] = Defend
