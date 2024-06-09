#from aidm.environments.gymnasium.gymnasium_problem import GymnasiumProblem

from pddlgymnasium.structs import LiteralConjunction
from multi_taxi import single_taxi_v0, maps

from aidm.environments.gym_envs.multi_taxi import MultiTaxiProblem
from aidm.search.frontier import PriorityQueue
from aidm.environments.pddl.pddl_problem import PDDLProblem
from aidm.search.best_first_search import best_first_search, breadth_first_search, depth_first_search, \
    depth_first_search_l, a_star, uniform_cost_search
from aidm.core.utils import CriteriaGoalState, print_results

import gymnasium as gym

from aidm.search.heuristic import goal_heuristic, zero_heuristic
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
    relaxed_problem.set_initial_state(node.state)
    [best_node, best_plan, resources] = breadth_first_search(relaxed_problem, logging=False)
    if best_plan is None:
        return np.inf
    return len(best_plan)

def my_heuristic2(node, problem):
    #get current state literals
    current_state_literals = node.state.content.literals
    #get goal literals
    goal_state_literals = problem.env.problems[0].goal.literals
    #check difference
    count = len(goal_state_literals)
    for literal in goal_state_literals:
        if literal in  current_state_literals:
            count -=1
    return count

def test_pddl_search(problem_name):

    # create a wrapper of the environment to the search
    #problem = PDDLProblem(domain=DOMAIN, problem=PROBLEM2)
    problem = PDDLProblem(domain='domain.pddl', problem=problem_name, relaxed=False)

    # perform bfs
    [best_node, best_plan, resources] = breadth_first_search(problem=problem, logging=False)

    print_results(info='breadth_first_search', node=best_node, plan=best_plan, resources=resources)
    [best_node, best_plan, resources] = a_star(problem=problem, heuristic_func=goal_heuristic, logging=False, use_closed_list=True)

    print_results(info='a_star with goal heuristic', node=best_node, plan=best_plan, resources=resources)



    [best_node, best_plan, resources] = best_first_search(problem=problem,
                                                          frontier=PriorityQueue(eval_func=zero_heuristic),
                                                          termination_criteria=[CriteriaGoalState()],
                                                          prune_func=None, is_anytime=False, iter_limit=None,
                                                          time_limit=None, logging=False)

    print_results(info='best_first_search',node=best_node, plan=best_plan, resources=resources)

    [best_node, best_plan, resources] = depth_first_search(problem=problem,use_closed_list=True, iter_limit=None, logging=False)

    print_results(info='depth_first_search', node=best_node, plan=best_plan, resources=resources)

    [best_node, best_plan, resources] = depth_first_search_l(problem=problem, depth_bound=2, use_closed_list=True, logging=False)

    print_results(info='depth_first_search_l', node=best_node, plan=best_plan, resources=resources)

    [best_node, best_plan, resources] = uniform_cost_search(problem=problem, use_closed_list=True, logging=False)

    print_results(info='uniform_cost_search', node=best_node, plan=best_plan, resources=resources)

    [best_node, best_plan, resources] = a_star(problem=problem, heuristic_func=my_heuristic2, logging=False, use_closed_list=True)

    print_results(info='a_star with my heuristic', node=best_node, plan=best_plan, resources=resources)

    #    env = problem.get_env()
    #    env.apply_plan(plan=best_plan,render=True)
    #else:
    #    print('no plan fround')

def test_taxi_BFS():
    # define the environment
    taxi_env = single_taxi_v0.gym_env(domain_map=maps.SMALL_MAP, render_mode='human')

    taxi_env.reset()

    # get cur state object
    init_state = taxi_env.state()

    # update state to init state
    init_state.taxis[0].location = (0, 3)
    init_state.passengers[0].location = (0, 4)
    init_state.passengers[0].destination = (1, 4)

    # set init state
    taxi_env.unwrapped.set_state(init_state)

    # render env
    taxi_env.render()

    # create a wrapper of the environment to the search
    problem = MultiTaxiProblem(taxi_env)

    # perform best_first_serch
    # perform bfs
    print('planning...')
    [best_node, best_plan, resources] = breadth_first_search(problem=problem, iter_limit=None, logging=False)

    print_results(info='breadth_first_search', node=best_node, plan=best_plan, resources=resources)

    # problem.apply_plan(plan=best_plan,render=True)

def test_taxi_a_star():
    def manhatten_dist(r1, c1, r2, c2):
        # calssic manhatten dist |row1 - row2| + |col1 - col2|
        return abs(r1 - r2) + abs(c1 - c2)

    def taxi_heuristic(node, problem):
        # decode state integer to interpretable values
        state = node.state.content
        taxi = state.taxis[0]
        passenger = state.passengers[0]

        # split to 2 cases where the passenger is in the taxi and not in the taxi.
        if passenger.in_taxi:
            # dist from the taxi to the destination
            return manhatten_dist(*taxi.location, *passenger.destination) + 1  # include dropoff
        elif passenger.arrived:
            # passenger has reached the destination. this is a goal state
            return 0
        else:
            # dist from the taxi to the passenger and from the passenger to the destination
            passenger_dist = manhatten_dist(*taxi.location, *passenger.location)
            dest_dist = manhatten_dist(*passenger.location, *passenger.destination)
            return passenger_dist + dest_dist + 2  # include pickup and dropoff actions

    # define the environment
    taxi_env = single_taxi_v0.gym_env(domain_map=maps.SMALL_MAP, render_mode='human')

    taxi_env.reset()

    # get cur state object
    init_state = taxi_env.state()

    # update state to init state
    init_state.taxis[0].location = (0, 3)
    init_state.passengers[0].location = (4, 1)
    init_state.passengers[0].destination = (0, 0)

    # set init state
    taxi_env.unwrapped.set_state(init_state)

    # render env
    taxi_env.render()

    # create a wrapper of the environment to the search
    problem = MultiTaxiProblem(taxi_env)

    # perform best_first_serch
    # perform bfs
    print('planning...')
    [best_node, best_plan, resources] = a_star(problem=problem, heuristic_func=taxi_heuristic)

    print_results(info='breadth_first_search', node=best_node, plan=best_plan, resources=resources)

    # problem.apply_plan(plan=best_plan,render=True)

def test_relaxed(problem_name):
    problem = PDDLProblem(domain='domain.pddl', problem=problem_name, relaxed=False)
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


    [best_node, best_plan, resources] = a_star(problem=problem, heuristic_func=my_heuristic, logging=False, use_closed_list=True)

    print_results(info='a_star with my heuristic', node=best_node, plan=best_plan, resources=resources)



    [best_node, best_plan, resources] = a_star(problem=problem, heuristic_func=my_heuristic2, logging=False, use_closed_list=True)

    print_results(info='a_star with my heuristic2', node=best_node, plan=best_plan, resources=resources)




if __name__ == "__main__":
    # test_taxi_BFS()
    test_taxi_a_star()
    # print("test_relaxed('problem0.2.pddl'")
    # test_pddl_search('problem0.2.pddl')
    # test_relaxed('problem0.2.pddl')
    # print("test_relaxed('problem0.5.pddl'")
    # test_pddl_search('problem0.5.pddl')
    # test_relaxed('problem0.5.pddl')
