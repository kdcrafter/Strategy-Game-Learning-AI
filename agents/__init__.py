import sys
import os

sys.path.append(os.path.abspath('agents/'))

from agent import Agent
from random_action import RandomAction
from human import Human
from minmax import Minmax
from closest_action import ClosestAction
from tabular_qlearning import TabularQlearning