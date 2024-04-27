__author__ = 'sarah'


# adapdted from aima-python-master: https://github.com/aimacode/aima-python

import logging
logger = logging.getLogger('aidm-logger')
logging.basicConfig(filename='aidm.log', encoding='utf-8', level=logging.DEBUG)


from typing import TypedDict, Any




from abc import ABC, abstractmethod


class Action(TypedDict):
    key: Any  # a hashable and equatable value for identifying unique actions
    content: Any  # the actual action value indiginous to the specific problem/env

class State(TypedDict):
    key: Any # a hashable and equatable value for identifying unique states
    content: Any  # the problem specific state



class ClosedList():

    ''' Holding the list of items that have been explored '''
    def __init__(self):
        self.dict = {}

    def add_or_update(self, key:Any, value:Any):
        self.dict[key] = value

    def get(self, key:Any):
        return self.dict.get(key)

class Criteria(ABC):

    @abstractmethod
    def isTerminal(self, node, problem):
        pass


class CriteriaOptimalValue(Criteria):

    def __init__(self, optimal_value, orSmaller=True):
        self.optimal_value = optimal_value
        self.orSmaller = orSmaller

    def isTerminal(self, node, problem):
        if self.orSmaller:
            if node.value <= self.optimal_value:
                return True
            else:
                return False

        else:  # or bigger
            if node.value >= self.optimal_value:
                return True
            else:
                return False

    def __str__(self):
        raise NotImplementedError


class CriteriaGoalState(Criteria):

    def isTerminal(self, node, problem):
        if problem.is_goal_state(node.state):
            return True
        else:
            return False
