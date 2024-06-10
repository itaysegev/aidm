from abc import ABC
from typing import Any, Optional

from gymnasium import Env

from .spaces_utils import gymnasium_space_val_to_key
from ...core.problem import Problem
from ...core.utils import State, Action


class GymnasiumProblem(Problem, ABC):
    def __init__(self, env: Env):
        self._env = env

    def state_to_key(self, state: State):
        return gymnasium_space_val_to_key(state.content, self._env.observation_space)

    def sample_action(self, state: State, mask: Optional[Any] = None) -> Action:
        action = self._env.action_space.sample(mask=mask)
        return Action(
            key=gymnasium_space_val_to_key(action, self._env.action_space),
            content=action
        )
