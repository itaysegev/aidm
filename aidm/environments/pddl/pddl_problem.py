from pddlgymnasium.core import PDDLEnv
from pddlgymnasium.downward_translate.pddl_parser import open as downward_open

from ...core.problem import Problem
from ...core.utils import State, Action


class PDDLProblem(Problem):
    def __init__(self, domain, problem, operators_as_actions=True, dynamic_action_space=True, relaxed=False):
        self.env = PDDLEnv(domain, problem, operators_as_actions=operators_as_actions,
                           dynamic_action_space=dynamic_action_space, relaxed=relaxed)
        self.__dynamic_action_space = dynamic_action_space  # saving this for the copy constructor

        self.current_state = None
        self.reset_env()

        self.relaxed_version = None

        super().__init__()

    def relaxed(self):
        return PDDLProblem(
            domain=self.env.domain.domain_fname,
            problem=self.env._problem.problem_fname,
            operators_as_actions=self.env.operators_as_actions,
            dynamic_action_space=self.__dynamic_action_space,
            relaxed=True
        )

    def get_relaxed_problem(self):
        if self.relaxed_version is None:
            self.relaxed_version = self.relaxed()
        return self.relaxed_version

    def get_current_state(self)->State:
        return State(key=self.state_to_key(self.current_state), content=self.current_state) #TODO decide about the state

    def set_current_state(self, state:State):
        self.current_state = state['content']
        self.env.set_state(state['content'])

    def sample_action(self, state: State) -> Action:
        # convert ai_dm state to pddl state
        pddl_state = self.convert_state(state)
        action = self.env.action_space.sample(pddl_state)
        return Action(key=self.action_to_key(action),content=action)


    def convert_state(self, state: State):
        return state['content']

    def state_to_key(self, state):
        literals = sorted(state.literals)
        key = ''
        for lit in literals:
            key+=str(lit)
        return key

    def action_to_key(self, action):
        return action

    def evaluate(self,path:list[State,Action,State], discount_factor=1):
        value = 0
        for state,action,next_state in path:
            if action:
                value += discount_factor*self.get_value(state,action,next_state)
        return value

    def is_better(self, value_a, value_b)->bool:
        return True if value_a < value_b else False

    def get_applicable_actions(self, state:State)-> list[Action]:
        actions = []
        grounded_actions = self.env.action_space.all_ground_literals(state['content'])
        for action in grounded_actions:
            actions.append(Action(key=action,content=action))
        return actions

    def _get_successors(self, pre_state, action)  -> list[tuple[State, float]]:
        successors = []
        raw_transitions = self.env._get_successor_states(pre_state['content'], action['content'], self.env.domain,
                                            inference_mode=self.env._inference_mode,
                                            raise_error_on_invalid_action=self.env._raise_error_on_invalid_action,
                                                         return_probs=True)

        if isinstance(raw_transitions, dict):
            processed_transitions = [(self.env._get_new_state_info(state), prob) for state, prob in raw_transitions.items()]
        else:
            processed_transitions = [(self.env._get_new_state_info(raw_transitions), 1)]

        transitions = [(prob, s, r, d) for (s, r, d, _), prob in processed_transitions]
        #action_cost = self.get_action_cost(action, state)
        for prob, next_state, reward, done in transitions:
            info = {}
            info['prob'] = prob
            info['reward'] = reward
            next_state=State(key=self.state_to_key(next_state),content=next_state)
            successors.append([next_state, prob])

        return successors

    def get_cost(self, state: State, action: Action = None, next_state: State = None):
        task = downward_open(self.env.domain.domain_fname, self.env._problem.problem_fname)
        for downward_action in task.actions:
            if downward_action.name == action['content'].predicate.name:
                cost = downward_action.cost
                if cost is None:
                    break
                return cost

        return 1

    def get_value(self, state: State, action=None, next_state=None):
        return self.get_cost(state=state, action=action, next_state=next_state)

    def is_goal_state(self, state:State):
        return self.env._is_goal_reached(state['content'])

    def apply_action(self, action):
        return self.env.step(action['content'])

    def reset_env(self):
        self.current_state, _ = self.env.reset()
        return  State(key=self.state_to_key(self.current_state), content=self.current_state)

    def get_env(self):
        return self.env

    def get_goal(self):
        return self.env._goal

