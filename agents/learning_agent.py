from agent import Agent
from config import TRAINING_AGENTS_DIRECTORY

from abc import ABC, abstractmethod, abstractproperty
import os, dill

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

    def save(self, name):
        if not os.path.isdir(TRAINING_AGENTS_DIRECTORY):
            os.mkdir(TRAINING_AGENTS_DIRECTORY)

        filename = name + '.pickle'
        pathname = os.path.join(TRAINING_AGENTS_DIRECTORY, filename)

        with open(pathname, 'wb') as file:
            data = (self.__class__, self.__dict__)
            dill.dump(data, file)

    def load(self, name):
        assert(os.path.isdir(TRAINING_AGENTS_DIRECTORY))

        filename = name + '.pickle'
        pathname = os.path.join(TRAINING_AGENTS_DIRECTORY, filename)

        with open(pathname, 'rb') as file:
            cls, attributes = dill.load(file)
            assert(self.__class__ == cls)
            self.__dict__.update(attributes)
            