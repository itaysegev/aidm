__author__ = 'sarah'

from abc import ABC

from .gymnasium_env import GymasiumEnv
from ...core.problem import Problem
from ...core.utils import Action, State
import gymnasium as gym


# Wrapping Gymnasium problems for which the probability function P can be accessed.
# Examples include taxi, frozen_lake and Cliff Walking
class GymnasiumProblem(Problem):

    def __init__(self, domain_name, init_state=None, operators_as_actions=True, dynamic_action_space=True):
        super().__init__()
        self.env = GymasiumEnv(domain_name, operators_as_actions=operators_as_actions,
                               dynamic_action_space=dynamic_action_space)
        if init_state:
            self.current_state = self.env.set_state(init_state)
        else:
            self.current_state = self.env.reset()

    def get_current_state(self) -> State:
        return State(key=self.get_state_key(self.current_state),content=self.current_state)

    def get_state_key(self, state: State):
        return str(state[0])

    def get_action_key(self, action: Action):
        return action

    def is_better(self, value_a, value_b) -> bool:
        return True if value_a > value_b else False

    def get_applicable_actions(self, state: State) -> list[Action]:
        actions = []
        grounded_actions = self.env.action_space
        for action in grounded_actions:
            actions.append(Action(key=self.get_action_key(action), content=action))
        return actions

    def _get_successors(self, state, action) -> list[tuple[State, float]]:
        successors = []
        raw_transitions = self.env._get_successor_states(state['content'], action['content'], self.env.domain,
                                                         inference_mode=self.env._inference_mode,
                                                         raise_error_on_invalid_action=self.env._raise_error_on_invalid_action,
                                                         return_probs=True)

        return successors

    def get_cost(self, state: State, action: Action = None, next_state: State = None):
        return 1

    def get_value(self, state: State, action=None, next_state=None):
        return self.get_cost(state=state, action=action, next_state=next_state)

    def is_goal_state(self, state: State):
        return self.env._is_goal_reached(state['content'])

    def apply_action(self, action):
        return self.env.step(action)

    def reset_env(self):
        return self.env.reset()

    def get_env(self):
        return self.env
