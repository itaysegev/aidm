from aidm.core.utils import State, Action
from aidm.todos.gymnasium.gymnasium_problem import GymnasiumProblem


class TaxiProblem(GymnasiumProblem):
    def __init__(self, gymnasium_env, domain_name, init_state=None, operators_as_actions=True, dynamic_action_space=True):
        self.env = gymnasium_env #GymasiumEnv(domain_name, operators_as_actions=operators_as_actions, dynamic_action_space=dynamic_action_space)
        super().__init__(domain_name, init_state=None, operators_as_actions=True, dynamic_action_space=True)

    def get_cost(self, state: State, action: Action = None, next_state: State = None):
        return 1

    def get_value(self, state: State, action=None, next_state=None):
        return self.get_cost(state=state, action=action, next_state=next_state)

    def is_better(self, value_a, value_b) -> bool:
        # minimizing cost
        return True if value_a < value_b else False

    def evaluate(self, path: list[State, Action, State], discount_factor=1):
        value = 0
        for state, action, next_state in path:
            if action:
                value += discount_factor * self.get_value(state, action, next_state)
        return value

    def state_to_key(self, state):
        pass