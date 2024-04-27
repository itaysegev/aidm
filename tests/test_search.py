#from aidm.environments.gymnasium.gymnasium_problem import GymnasiumProblem
from aidm.search.frontier import PriorityQueue
from aidm.environments.pddl.pddl_problem import PDDLProblem
from aidm.search.best_first_search import best_first_search, breadth_first_search
import aidm.core.utils as utils

import gymnasium as gym

from aidm.search.heuristic import goal_heuristic, zero_heuristic
from pddl import DOMAIN,PROBLEM

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
    problem = GymnasiumProblem(taxi_env, taxi_env.unwrapped.s)

    # perform best_first_serch
    [best_value, best_node, best_plan, explored_count, ex_terminated] = best_first_search(problem=problem,
                                                                                          frontier=aidm.search.frontier.FIFOQueue(),
                                                                                          termination_criteria=utils.CriteriaGoalState(),
                                                                                          prune_func=None,
                                                                                          closed_list=utils.ClosedList(),
                                                                                          iter_limit=None,
                                                                                          time_limit=None,
                                                                                          logging=False)
    print('best_plan'+str(best_plan))
    problem.apply_plan(plan=best_plan,render=True)


def test_pddl_search():



    # create a wrapper of the environment to the search
    problem = PDDLProblem(domain_file=DOMAIN, problem_file=PROBLEM)
    # perform best_first_serch

    [best_node, best_plan, resources] = breadth_first_search(problem=problem,
                                                          iter_limit=1000,
                                                          logging=True)
    [best_node, best_plan, resources] = best_first_search(problem=problem,
                                                          frontier=PriorityQueue(eval_func=zero_heuristic),  #aidm.search.frontier.FIFOQueue(),
                                                          termination_criteria=utils.CriteriaGoalState(),
                                                          prune_func=None,
                                                          closed_list=None,  #utils.ClosedList(),
                                                          is_anytime = False,
                                                          iter_limit=10000,
                                                          time_limit=None,
                                                          logging=True)

    if best_plan:
        print('best_plan:')
        for action in best_plan:
            print(action)
        env = problem.get_env()
        env.apply_plan(plan=best_plan,render=True)
    else:
        print('no plan fround')

if __name__ == "__main__":
    test_pddl_search()
