from agent import Agent

from abc import ABC, abstractmethod, abstractproperty

class LearningAgent(Agent):
    def __init__(self):
        super().__init__()

        self.learn()

    @abstractmethod
    def learn(self):
        pass

    @abstractmethod
    def stop_learning(self):
        pass