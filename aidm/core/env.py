from abc import ABC, abstractmethod

from .problem import Problem
from ..core.utils import Action, State


class Env(ABC):
    def __init__(self, problem: Problem):
        self.problem = problem

    @abstractmethod
    def get_current_state(self) -> State:
        """

        """
        pass

    @abstractmethod
    def apply_action(self, action: Action) -> State:
        """

        """
        pass

    @abstractmethod
    def set_state(self, state):
        """

        """
        pass

    def render(self):
        pass

    def apply_plan(self, plan: list[Action], render=False):
        if render:
            self.render()
        for action in plan:
            self.apply_action(action)
            if render:
                self.render()

