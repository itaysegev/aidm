from pddlgymnasium.core import PDDLEnv

from ...core.problem import Problem
from ...core import utils


class PDDLProblem(Problem):

    def __init__(self, domain_file, problem_file, operators_as_actions=True,
                 dynamic_action_space=True):
        self.env = PDDLEnv(domain_file, problem_file, operators_as_actions=operators_as_actions,
                           dynamic_action_space=dynamic_action_space)
        initial_state, _ = self.env.reset()
        super().__init__(initial_state, constraints=[])

    def get_applicable_actions_at_state(self, state):
        return self.env.action_space.all_ground_literals(state)

    def get_applicable_actions_at_node(self, node):
        return self.get_applicable_actions_at_state(node.state.key)

    def get_successors(self, action, node):
        successor_nodes = []
        raw_transitions = self.env._get_successor_states(node.state.key, action, self.env.domain,
                                            inference_mode=self.env._inference_mode,
                                            raise_error_on_invalid_action=self.env._raise_error_on_invalid_action,
                                                         return_probs=True)

        if isinstance(raw_transitions, dict):
            processed_transitions = [(self.env._get_new_state_info(state), prob) for state, prob in raw_transitions.items()]
        else:
            processed_transitions = [(self.env._get_new_state_info(raw_transitions), 1)]

        transitions = [(prob, s, r, d) for (s, r, d, _), prob in processed_transitions]
        action_cost = self.get_action_cost(action, node.state)
        for prob, next_state_key, reward, done in transitions:
            info = {}
            info['prob'] = prob
            info['reward'] = reward
            next_state = utils.State(next_state_key, done)
            successor_node = utils.Node(state=next_state, action=action, parent=node)
            successor_nodes.append(successor_node)

        return successor_nodes

    def get_action_cost(self, action, state):
        return 1  #TODO support input cost with fluents?

    def is_goal_state(self, state):
        return self.env._is_goal_reached(state.key)

    def apply_action(self, action):
        return self.env.step(action)

    def reset_env(self):
        return self.env.reset()
