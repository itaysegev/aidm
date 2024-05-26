import gymnasium as gym
from aidm.core.env import Env
from aidm.core.utils import Action, State


class GymasiumEnv(Env):
    def __int__(self):
        super().__init__()

    def __gym_state_to_aidm_state(self, state) -> State:
        return State(
            key=str(state),
            content=state
        )

    def get_current_state(self) -> State:
        return self.env.get_state()

    def apply_action(self, action) -> State:
        return self.env.step(action.value)

    def set_state(self, state: State):
        return self.env.set_state(state.value)