__author__ = 'sarah'

from abc import ABC, abstractmethod
from ..core.utils import State, Action


class Problem (ABC):

    @abstractmethod
    def get_applicable_actions(self, state:State)-> list[Action]:
        pass

    # return the successors that will result from applying the action (without changing the state) and their associated probability
    @abstractmethod
    def _get_successors(self, state: State, action: Action) -> list[tuple[State, float]]:
        """
        Args:
            action - the action to perform at the current state
            state - the current state
        Returns:
            A list of tuples of the form (s, p) where s is a state and p is a probability value in [0, 1]. the sum
            of all probabilities in the list must sum to 1.
        """
        pass

    @abstractmethod
    def get_cost(self, state: State, action: Action = None, next_state: State = None):
        pass

    @abstractmethod
    def get_value(self, state: State, action=None, next_state=None):
        pass

    @abstractmethod
    def is_goal_state(self, state:State):
        pass

    @abstractmethod
    def get_initial_state(self)->State:
        pass

    @abstractmethod
    def set_initial_state(self, state:State):
        pass

    @abstractmethod
    def is_better(self, value_a, value_b)->bool:
        pass

    @abstractmethod
    def evaluate(self,path):
        pass

    @abstractmethod
    def state_to_key(self, state:State):
        pass


    @abstractmethod
    def sample_action(self,state:State)->Action:
        pass


    def get_successors(self, state: State, action: Action=None) -> list[Action,list[tuple[State, float]]]:
        if action:
            out = self._get_successors(state, action)
            probs = [p for _, _, p in out]
            assert sum(probs) == 1, 'probabilities in successors must sum to 1'
        else:
            out = []
            for action in self.get_applicable_actions(state=state):
                cur=self._get_successors(state, action)
                probs = [p for _, p in cur]
                assert sum(probs) == 1, 'probabilities in successors must sum to 1'
                out.append([action,cur])
        return out

        # for more complex situations, we can use np.close(sum(probs), 1)




