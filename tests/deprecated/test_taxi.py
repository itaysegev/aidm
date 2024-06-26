import gym
from aidm.environments.gym_envs.gym_problem import GymProblem

import aidm.search.frontier
from aidm.search.best_first_search import best_first_search, breadth_first_search, depth_first_search, a_star, depth_first_search_l
import aidm.rl.mcts as mcts
import aidm.core.utils as utils
import aidm.search.defs as defs
import aidm.search.heuristic as heuristic

import aidm.core.resources as comp_resources



def main_taxi_bfs():

    # define the environment
    taxi_env = gym.make("Taxi-v3", render_mode='ansi').env
    taxi_env.reset()
    #init_state = taxi_env.encode(0, 4, 4, 1) # (taxi row, taxi column, passenger index, destination index)
    init_state = taxi_env.encode(0, 3, 4, 1)  # (taxi row, taxi column, passenger index, destination index)
    taxi_row, taxi_col, pass_idx, dest_idx = taxi_env.decode(init_state)
    print(taxi_row)
    taxi_env.unwrapped.s = init_state
    print("State:", init_state)
    print(taxi_env.render())

    # dropping off the passenger
    #observation, reward, done, info = taxi_env.step(5)
    #print(done)
    #taxi_env.render()


    # create a wrapper of the environment to the search
    taxi_p = GymProblem(taxi_env, taxi_env.unwrapped.s)

    # perform BFS
    [best_value, best_node, best_plan, explored_count, ex_terminated] = best_first_search(problem=taxi_p,
                                                                                          frontier=aidm.search.frontier.FIFOQueue(),
                                                                                          termination_criteria=utils.CriteriaGoalState(),
                                                                                          prune_func=None)
    print(best_plan)
    for action_id in best_plan:
        taxi_p.apply_action(action_id)
        taxi_p.env.render()


def main_taxi_dfs():


    # define the environment
    taxi_env = gym.make("Taxi-v3", render_mode='ansi').env
    taxi_env.reset()
    #init_state = taxi_env.encode(0, 4, 4, 1) # (taxi row, taxi column, passenger index, destination index)
    init_state = taxi_env.encode(0, 3, 4, 1)   # (taxi row, taxi column, passenger index, destination index)
    taxi_row, taxi_col, pass_idx, dest_idx = taxi_env.decode(init_state)
    taxi_env.unwrapped.s = init_state
    print("State:", init_state)
    print(taxi_env.render())

    # dropping off the passenger
    #observation, reward, done, info = taxi_env.step(5)
    #print(done)
    #taxi_env.render()


    # create a wrapper of the environment to the search
    taxi_p = GymProblem(taxi_env, taxi_env.unwrapped.s)


    # perform BFS
    [best_value, best_node, best_plan, explored_count, ex_terminated] = depth_first_search(problem=taxi_p,
                                                                                                        log=True,
                                                                                                        log_file=None,
                                                                                                        iter_limit=defs.NA,
                                                                                                        time_limit=defs.NA,
                                                                                                        )


    print(best_plan)
    for action_id in best_plan:
        taxi_p.apply_action(action_id)
        taxi_p.env.render()



def main_taxi_dfsl():


    # define the environment
    taxi_env = gym.make("Taxi-v3", render_mode='ansi').env
    taxi_env.reset()
    #init_state = taxi_env.encode(0, 4, 4, 1) # (taxi row, taxi column, passenger index, destination index)
    init_state = taxi_env.encode(0, 3, 4, 1)   # (taxi row, taxi column, passenger index, destination index)
    taxi_row, taxi_col, pass_idx, dest_idx = taxi_env.decode(init_state)
    taxi_env.unwrapped.s = init_state
    print("State:", init_state)
    print(taxi_env.render())

    # dropping off the passenger
    #observation, reward, done, info = taxi_env.step(5)
    #print(done)
    #taxi_env.render()


    # create a wrapper of the environment to the search
    taxi_p = GymProblem(taxi_env, taxi_env.unwrapped.s)


    # perform dfs-l
    [best_value, best_node, best_plan, explored_count, ex_terminated] = depth_first_search_l(problem=taxi_p, max_depth=3,
                                                                                                        log=True,
                                                                                                        log_file=None,
                                                                                                        iter_limit=defs.NA,
                                                                                                        time_limit=defs.NA,
                                                                                                        )


    print(best_plan)
    for action_id in best_plan:
        taxi_p.apply_action(action_id)
        taxi_p.env.render()



def main_taxi_bfs_exp():

    # define the environment
    taxi_env = gym.make("Taxi-v3", render_mode='ansi').env
    taxi_env.reset()
    #init_state = taxi_env.encode(0, 4, 4, 1) # (taxi row, taxi column, passenger index, destination index)
    init_state = taxi_env.encode(0, 3, 4, 1)  # (taxi row, taxi column, passenger index, destination index)
    taxi_row, taxi_col, pass_idx, dest_idx = taxi_env.decode(init_state)
    taxi_env.unwrapped.s = init_state
    print("State:", init_state)
    print(taxi_env.render())

    # dropping off the passenger
    #observation, reward, done, info = taxi_env.step(5)
    #print(done)
    #taxi_env.render()


    # create a wrapper of the environment to the search
    taxi_p = GymProblem(taxi_env, taxi_env.unwrapped.s)


    # perform BFS
    [best_value, best_node, best_plan, explored_count, ex_terminated] = breadth_first_search(problem=taxi_p,
                                                                                                          log=True,
                                                                                                          log_file=None,
                                                                                                          iter_limit=defs.NA,
                                                                                                          time_limit=defs.NA,
                                                                                                          )


    print(best_plan)
    for action_id in best_plan:
        taxi_p.apply_action(action_id)
        taxi_p.env.render()


def main_taxi_a_star():

    # define the environment
    taxi_env = gym.make("Taxi-v3", render_mode='ansi').env
    taxi_env.reset()
    #init_state = taxi_env.encode(0, 4, 4, 1) # (taxi row, taxi column, passenger index, destination index)
    init_state = taxi_env.encode(0, 3, 4, 1)  # (taxi row, taxi column, passenger index, destination index)
    taxi_row, taxi_col, pass_idx, dest_idx = taxi_env.decode(init_state)
    print(taxi_row)
    taxi_env.unwrapped.s = init_state
    print("State:", init_state)
    print(taxi_env.render())

    # dropping off the passenger
    #observation, reward, done, info = taxi_env.step(5)
    #print(done)
    #taxi_env.render()


    # create a wrapper of the environment to the search
    taxi_p = GymProblem(taxi_env, taxi_env.unwrapped.s)

    # perform A*
    [best_value, best_node, best_plan, explored_count, ex_terminated] = best_first_search(problem=taxi_p,
                                                                                          frontier=aidm.search.frontier.PriorityQueue(
                                                                                              heuristic.zero_heuristic),
                                                                                          termination_criteria=utils.CriteriaGoalState(),
                                                                                          prune_func=None)
    print(best_plan)
    for action_id in best_plan:
        taxi_p.apply_action(action_id)
        taxi_p.env.render()

def main_taxi_a_star():

    # define the environment
    taxi_env = gym.make("Taxi-v3", render_mode='ansi').env
    taxi_env.reset()
    #init_state = taxi_env.encode(0, 4, 4, 1) # (taxi row, taxi column, passenger index, destination index)
    init_state = taxi_env.encode(0, 3, 4, 1)  # (taxi row, taxi column, passenger index, destination index)
    taxi_row, taxi_col, pass_idx, dest_idx = taxi_env.decode(init_state)
    print(taxi_row)
    taxi_env.unwrapped.s = init_state
    print("State:", init_state)
    print(taxi_env.render())

    # dropping off the passenger
    #observation, reward, done, info = taxi_env.step(5)
    #print(done)
    #taxi_env.render()


    # create a wrapper of the environment to the search
    taxi_p = GymProblem(taxi_env, taxi_env.unwrapped.s)

    # perform A*
    [best_value, best_node, best_plan, explored_count, ex_terminated] = a_star(problem=taxi_p,heuristic_func=heuristic.zero_heuristic, log=True)

    print(best_plan)
    for action_id in best_plan:
        taxi_p.apply_action(action_id)
        taxi_p.env.render()


def main_test():

    # define the environment
    copy_env = gym.make('CartPole-v1')
    copy_env.reset()
    copy_env.render()

    # create a wrapper of the environment to the search
    copy_p = GymProblem(copy_env)

    # perform BFS
    optimal_path = best_first_search(problem=copy_p, frontier=aidm.search.frontier.FIFOQueue(),
                                     termination_criteria=utils.CriteriaGoalState(), prune_func=None)
    print(optimal_path)




def main_taxi_mcts():

    # define the environment
    taxi_env = gym.make("Taxi-v3", render_mode='ansi').env
    taxi_env.reset()
    #init_state = taxi_env.encode(0, 4, 4, 1) # (taxi row, taxi column, passenger index, destination index)
    init_state = taxi_env.encode(0, 3, 4, 1)  # (taxi row, taxi column, passenger index, destination index)
    taxi_row, taxi_col, pass_idx, dest_idx = taxi_env.decode(init_state)
    print(taxi_row)
    taxi_env.unwrapped.s = init_state
    print("State:", init_state)
    print(taxi_env.render())


    # create a wrapper of the environment to the search
    taxi_p = GymProblem(taxi_env, taxi_env.unwrapped.s)


    ## perform MCTS
    [best_value, best_node, best_plan, explored_count, ex_terminated] = mcts.mcts(problem=taxi_p, comp_resources=comp_resources.ComputationalResources(50), selection_policy= mcts.uct_selection_policy, expansion_policy= mcts.default_expansion_policy, rollout_policy=mcts.default_rollout_policy)

    #print(best_plan)
    #for action_id in best_plan:
    #    taxi_p.apply_action(action_id)
    #    taxi_p.env.render()



if __name__ == "__main__":
    # main_test()
    #main_taxi_bfs_exp()
    #main_taxi_dfs_exp()


    main_taxi_bfs()
    #main_taxi_dfs()
    #main_taxi_a_star()
    #main_taxi_dfsl()

    #main_taxi_mcts()