from aidm.environments.gymnasium.gymnasium_problem import GymnasiumProblem
from aidm.search.best_first_search import best_first_search
import aidm.core.utils as utils

import gymnasium as gym

def test_search():
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
                                                                                          frontier=utils.FIFOQueue(),
                                                                                          closed_list=utils.ClosedListOfKeys(),
                                                                                          termination_criteria=utils.TerminationCriteriaGoalStateReached(),
                                                                                          prune_func=None,
                                                                                          iter_limit=None,
                                                                                          time_limit=None,
                                                                                          logging=False)
    print('best_plan'+str(best_plan))
    problem.apply_plan(plan=best_plan,render=True)




if __name__ == "__main__":
    test_search()
