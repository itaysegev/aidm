__author__ = 'sarah'

from abc import ABC

from ...core.problem import Problem
from ...core.utils import Action, State


# Wrapping Gymnasium problems for which the probability function P can be accessed.
# Examples include taxi, frozen_lake and Cliff Walking
class GymnasiumProblem(Problem, ABC):

    """
       supporting Gymnasium problems
    """
    def __init__(self, env):
        self.env = env

    def apply_action(self, action):
        return self.env.step(int(action))

    def apply_plan(self, plan, render=False):
        for action_id in plan:
            self.apply_action(action_id)
            if render:
                self.env.render()

    # reset environment and return initial state
    def reset_env(self):
        return self.env.reset()[0]

