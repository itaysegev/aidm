#from aidm.environments.gymnasium.gymnasium_problem import GymnasiumProblem
import copy

from pddlgymnasium.structs import LiteralConjunction

from aidm.environments.gymnasium.gymnasium_problem import GymnasiumProblem
from aidm.environments.gymnasium.taxi_problem import TaxiProblem
from aidm.search.frontier import PriorityQueue, FIFOQueue
from aidm.environments.pddl.pddl_problem import PDDLProblem
from aidm.search.best_first_search import best_first_search, breadth_first_search, depth_first_search, \
    depth_first_search_l, a_star, uniform_cost_search
from aidm.core.utils import CriteriaGoalState, print_results, State, Action

import gymnasium as gym

from aidm.search.heuristic import goal_heuristic, zero_heuristic
from pddl import DOMAIN, PROBLEM, PROBLEM2
import numpy as np

from pddlgymnasium.parser import Operator
class RelaxedPDDLProblem(PDDLProblem):
    def __init__(self, domain, problem):
        super().__init__(domain, problem)
        #remove delete effects
        parsed_operators = {}
        for operator in self.env.domain.operators:
            parsed_literals = []
            effects = self.env.domain.operators[operator].effects.literals
            for effect in self.env.domain.operators[operator].effects.literals:
                if not effect.is_anti:
                    parsed_literals.append(effect)
            parsed_effects =  LiteralConjunction(parsed_literals)
            parsed_operators[operator] = Operator(name=operator, params=self.env.domain.operators[operator].params, preconds=self.env.domain.operators[operator].preconds, effects=parsed_effects)
        self.env.domain.operators = parsed_operators

# todo: avoid recreating the problem at every iteration
def my_heuristic(node, problem):
    relaxed_problem = problem.get_relaxed_problem()
    relaxed_problem.set_current_state(node.state)
    [best_node, best_plan, resources] = breadth_first_search(relaxed_problem, logging=False)
    if best_plan is None:
        print('my heuristic for node %s is %f'%(node, np.inf))
        return np.inf
    print('my heuristic for node %s is %f'%(node, len(best_plan)))
    return len(best_plan)

def my_heuristic2(node, problem):
    #get current state literals
    current_state_literals = node.state['content'].literals
    #get goal literals
    goal_state_literals = problem.env.problems[0].goal.literals
    #check difference
    count = len(goal_state_literals)
    for literal in goal_state_literals:
        if literal in  current_state_literals:
            count -=1
    return count
def test_pddl_search():

    # create a wrapper of the environment to the search
    problem = PDDLProblem(domain=DOMAIN, problem=PROBLEM2)

    # perform bfs
    #[best_node, best_plan, resources] = breadth_first_search(problem=problem, iter_limit=1000, logging=False)

    #print_results(info='breadth_first_search', node=best_node, plan=best_plan, resources=resources)
    #[best_node, best_plan, resources] = a_star(problem=problem, heuristic_func=goal_heuristic, logging=False, use_closed_list=True)

    #print_results(info='a_star with goal heuristic', node=best_node, plan=best_plan, resources=resources)



    #[best_node, best_plan, resources] = best_first_search(problem=problem,
    #                                                      frontier=PriorityQueue(eval_func=zero_heuristic),
    #                                                      termination_criteria=[CriteriaGoalState()],
    #                                                      prune_func=None, is_anytime=False, iter_limit=10000,
    #                                                      time_limit=None, logging=False)

    #print_results(info='best_first_search',node=best_node, plan=best_plan, resources=resources)

    #[best_node, best_plan, resources] = depth_first_search(problem=problem,use_closed_list=True, iter_limit=100, logging=False)

    #print_results(info='depth_first_search', node=best_node, plan=best_plan, resources=resources)

    #[best_node, best_plan, resources] = depth_first_search_l(problem=problem, depth_bound=2, use_closed_list=True, logging=False)

    #print_results(info='depth_first_search_l', node=best_node, plan=best_plan, resources=resources)

    #[best_node, best_plan, resources] = uniform_cost_search(problem=problem, use_closed_list=True, logging=False)

    #print_results(info='uniform_cost_search', node=best_node, plan=best_plan, resources=resources)

    [best_node, best_plan, resources] = a_star(problem=problem, heuristic_func=my_heuristic2, logging=False, use_closed_list=True)

    print_results(info='a_star with my heuristic', node=best_node, plan=best_plan, resources=resources)

    #    env = problem.get_env()
    #    env.apply_plan(plan=best_plan,render=True)
    #else:
    #    print('no plan fround')

def test_gym_search():

    # define the environment
    taxi_env= gym.make('Taxi-v3',render_mode='human')

    taxi_env.reset()
    init_state = taxi_env.encode(0, 3, 4, 1)  # (taxi row, taxi column, passenger index, destination index)
    taxi_row, taxi_col, pass_idx, dest_idx = taxi_env.decode(init_state)
    print(taxi_row)
    taxi_env.unwrapped.s = init_state
    print("State:", init_state)
    taxi_env.render()

    # create a wrapper of the environment to the search
    problem = TaxiProblem(taxi_env, taxi_env.unwrapped.s)

    # perform best_first_serch
    # perform bfs
    [best_node, best_plan, resources] = breadth_first_search(problem=problem, iter_limit=1000, logging=False)

    print_results(info='breadth_first_search', node=best_node, plan=best_plan, resources=resources)

    problem.apply_plan(plan=best_plan,render=True)

def test_relaxed():
    problem = PDDLProblem(domain='domain.pddl', problem='problem0.2.pddl', relaxed=False)
    #problem = PDDLProblem(domain=DOMAIN, problem=PROBLEM2, relaxed=False)

    #best_node, best_plan, resources = breadth_first_search(
    #    problem=problem,
    #    use_closed_list=True,
    #)
    #print_results(info='bfs', node=best_node, plan=best_plan, resources=resources)

    #relaxed_problem = problem.relaxed()

    #r_best_node, r_best_plan, r_resources = breadth_first_search(
    #    problem=relaxed_problem,
    #    use_closed_list=True,
    #)
    #print_results(info='bfs relaxed', node=r_best_node, plan=r_best_plan, resources=r_resources)

    #[best_node, best_plan, resources] = a_star(problem=problem, heuristic_func=goal_heuristic, logging=False, use_closed_list=True)

    #print_results(info='a_star with goal heuristic', node=best_node, plan=best_plan, resources=resources)


    [best_node, best_plan, resources] = a_star(problem=problem, heuristic_func=my_heuristic2, logging=False, use_closed_list=True)

    print_results(info='a_star with my heuristic2', node=best_node, plan=best_plan, resources=resources)



if __name__ == "__main__":
    #test_pddl_search()
    #test_gym_search()
    test_relaxed()