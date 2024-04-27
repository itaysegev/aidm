__author__ = 'sarah'

from abc import ABC

from .gymnasium_env import GymasiumEnv
from ...core.problem import Problem
from ...core.utils import Action, State
import gymnasium as gym


# Wrapping Gymnasium problems for which the probability function P can be accessed.
# Examples include taxi, frozen_lake and Cliff Walking

class GymnasiumProblem(Problem):
    def __init__(self, domain_name, init_state, operators_as_actions=True, dynamic_action_space=True):
        self.env = GymasiumEnv(domain_name, operators_as_actions=operators_as_actions,
                           dynamic_action_space=dynamic_action_space)
        self.state = initial_state, _ = self.env.set_state(init_state)


    def _get_successors(self, state: State, action: Action) -> list[tuple[State, Action, float]]:
        pass

    def get_cost(self, state, action=None, next_state=None):
        pass

    def get_value(self, state, action=None, next_state=None):
        pass

    def is_goal_state(self, state: State):
        pass
