__author__ = 'sarah'

from abc import ABC, abstractmethod
from ..core.utils import State, Action


class Problem (ABC):

    # return the successors that will result from applying the action (without changing the state) and their associated probability
    @abstractmethod
    def _get_successors(self, action: Action, state: State) -> list[tuple[State, Action, float]]:
        """
        Args:
            action - the action to perform at the current state
            state - the current state
        Returns:
            A list of tuples of the form (s, p) where s is a state and p is a probability value in [0, 1]. the sum
            of all probabilities in the list must sum to 1.
        """
        pass

    def get_successors(self, action: Action, state: State) -> list[tuple[State, float]]:
        """same here"""
        out = self._get_successors(action, state)
        probs = [p for _, _, p in out]
        assert sum(probs) == 1, 'probabilities in successors must sum to 1'
        return out
        # for more complex situations, we can use np.close(sum(probs), 1)

    @abstractmethod
    def get_cost(self, state, action=None, next_state=None):
        pass

    @abstractmethod
    def get_value(self, state, action=None, next_state=None):
        pass

    @abstractmethod
    def is_goal_state(self, state:State):
        pass

    def sample_applicable_actions_at_state(self, state:State, sample_size:int):
        pass
