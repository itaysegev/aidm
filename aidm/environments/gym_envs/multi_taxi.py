from multi_taxi import single_taxi_v0
from ..gymnasium.gymnasium_problem import GymnasiumProblem
from ...core.utils import State, Action


class MultiTaxiProblem(GymnasiumProblem):
    @classmethod
    def from_args(cls, *args, **kwargs):
        env = single_taxi_v0.gym_env(*args, **kwargs)
        env.reset()
        return cls(env)

    def get_applicable_actions(self, state: State) -> list[Action]:
        return list(map(
            lambda x: Action(key=x, content=x),
            range(self._env.action_space.n)
        ))

    def _get_successors(self, state: State, action: Action) -> list[tuple[State, float]]:
        transitions = self._env.unwrapped.state_action_transitions(state.content, action.content)
        state_prop_transitions = list(map(
            lambda trans: (State(key=trans[0], content=trans[0]), trans[-1]),
            transitions
        ))

        return state_prop_transitions

    def get_cost(self, state: State, action: Action = None, next_state: State = None):
        return 1  # TODO ???

    def get_value(self, state: State, action=None, next_state=None):
        return self.get_cost(state=state, action=action, next_state=next_state)  # TODO ???

    def is_goal_state(self, state: State):
        return self._env.unwrapped.env_done(state.content)

    def get_initial_state(self) -> State:
        s = self._env.unwrapped.state()

        # multi-taxi state is hashable
        return State(key=s, content=s)

    def set_initial_state(self, state: State):
        return self._env.unwrapped.set_state(state.content)

    def is_better(self, value_a, value_b) -> bool:
        return value_a < value_b  # TODO ???

    def evaluate(self, path, discount_factor=1):
        # TODO ???
        value = 0
        for state, action, next_state in path:
            if action:
                value += discount_factor * self.get_value(state, action, next_state)
        return value

    def state_to_key(self, state):
        return state
