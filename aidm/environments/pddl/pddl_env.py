from pddlgymnasium.structs import State as pddlState
from .pddl_problem import PDDLProblem
from ...core.env import Env
from ...core.utils import Action, State


class PDDLEnv(Env):
    def __int__(self):
        super().__init__()

    def __pddl_state_to_aidm_state(self, state: pddlState) -> State:
        return State(key=str(state),content=state)

    def __aidm_state_to_pddl_state(self, state: State) -> pddlState:
        return state['content']

    def get_current_state(self) -> State:
        return self.__pddl_state_to_aidm_state(self.env.get_state())

    def apply_action(self, action: Action) -> State:
        return self.env.step(action.value)

    def set_state(self, state: State):
        return self.env.set_state(state.value)