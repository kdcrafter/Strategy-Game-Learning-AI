from agent import Agent
from config import TRAINING_AGENTS_DIRECTORY

from abc import ABC, abstractmethod, abstractproperty
import os, joblib

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

        filename = name + '.joblib'
        pathname = os.path.join(TRAINING_AGENTS_DIRECTORY, filename)

        data = (self.__class__, self.__dict__)
        joblib.dump(data, pathname)

    def load(self, name):
        assert(os.path.isdir(TRAINING_AGENTS_DIRECTORY))

        filename = name + '.joblib'
        pathname = os.path.join(TRAINING_AGENTS_DIRECTORY, filename)

        cls, attributes = joblib.load(pathname)
        assert(self.__class__ == cls)
        self.__dict__.update(attributes)
            