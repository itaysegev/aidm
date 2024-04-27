__author__ = 'sarah'

import aidm.search.frontier
from ..core.resources import ComputationalResources
from ..core.utils import logger, ClosedList, CriteriaGoalState
from .node import Node

def best_first_search(problem, frontier, termination_criteria=None, prune_func=None, closed_list=None, is_anytime=False, iter_limit=None, time_limit=None, logging=False):
    """Search for an action sequence with maximal value.
       The search problem must specify the following elements:

       - problem - specifies for each node its value and its successors

       The search related elements that need to be defined are the following:
       - frontier (fringe) - keeps the open nodes and defines the order by which they are examined (e.g., queue) see search.utils for options
                    if this is a heuristic search, the heuristic is used by the frontier when add is evoked
       - closed_list - maintains the states that have been explored (if set to None, no list is maintained)
       - termination_criteria - a termination condition for which the current best result is returned.
         For example, for a goal directed search the search will stop once the goal condition is satisfied
       - prune_func - given the successors of a node, the pruning function returns only the nodes to be further explored
    """

    # init the search node
    root_node = Node(state=problem.get_current_state(),action=None, parent=None)
    # the frontier sets the order by which nodes are explored (e.g.FIFO, LIFO etc.)
    # we are assuming the root node is valid, i.e., it doesn't violate the constraints
    frontier.add(root_node, problem)
    # keeping the best solution found so far
    best_node = None
    best_value = None
    best_plan = None
    # keep track of search resources
    resources=ComputationalResources(iteration_bound=iter_limit, time_bound=time_limit)

    try:

        while not frontier.is_empty():

            # update resources (iteration count will advance by 1)
            # check resource limit has not been reached
            resources.update()
            if resources.are_exhausted():
                if logging: logger.info('best_first_search: resources exhausted')
                if is_anytime:
                    return [best_node, best_plan, resources]
                else:
                    return [None, None, resources]

            # get the current node and its value
            cur_node = frontier.extract()
            cur_value = problem.evaluate(path=cur_node.get_transition_path())
            if logging:logger.info('best_first_search resources %s cur_node:%s cur_value:%f' % (resources.__str__(),cur_node.__str__(), cur_value))

            # if the closed list was specified - check if this state should be explored again
            if closed_list:
                # if the state is already in the closed list and a better value was found
                # extract it from the closed list
                if not closed_list.get(cur_node.state['key']) or problem.is_better(cur_value, closed_list.get(cur_node.state['key'])):
                    # update value in closed list
                    closed_list.add_or_update(key=cur_node.state['key'],value=cur_value)

            # if anytime is true - keep the best node so far
            if is_anytime:
                if best_node is None or problem.is_better(cur_value, best_value):
                    best_value = cur_value
                    best_node  = cur_node
                    best_plan  = best_node.get_transition_path_string()

            # check if termination criteria had been met - and stop the search if it has
            if termination_criteria and termination_criteria.isTerminal(cur_node, problem):
                plan = cur_node.get_transition_path_string()
                if logging: logger.info('best_first_search: termination_criteria reached with solution %s' % (cur_node.get_transition_path_string()))
                return [cur_node, plan, resources]

            # get the succsessor states of the state of the current node
            all_successors = problem.get_successors(state=cur_node.state)
            successors = []
            for action, outcomes in all_successors:
                for state,_ in outcomes:
                    successors.append(Node(state, action, cur_node))

            # if pruning is applied - prune the set of successors
            if prune_func is not None:
                successors = prune_func(successors, cur_node)
            # sort successors to make sure goal is reached at the same time for all approaches
            successors = sorted(successors, key=lambda x: x.get_transition_path_string(), reverse=False)

            # add successors to the frontier
            for child in successors:
                frontier.add(child,problem)

        # search graph fully explored without finding a solution
        if logging: logger.info('best_first_search: search graph fully explored without finding a solution')
        return [None, None, resources]

    except Exception as e:
        if logging: logger.info('best_first_search: exception occurred: %s'%str(e))
        raise e

def breadth_first_search(problem, iter_limit=None, time_limit=None, logging=False):
    return best_first_search(problem, frontier=aidm.search.frontier.FIFOQueue(),
                             termination_criteria= CriteriaGoalState(), prune_func=None,
                             closed_list=ClosedList(), iter_limit=iter_limit, time_limit=time_limit,
                             logging=logging)

def depth_first_search(problem, iter_limit=None, time_limit=None, logging=False):
    return best_first_search(problem, frontier=aidm.search.frontier.LIFOQueue(),
                             termination_criteria=CriteriaGoalState(), prune_func=None,
                             closed_list=ClosedList(), iter_limit=iter_limit, time_limit=time_limit,
                             logging=logging)

def depth_first_search_l(problem, max_depth, iter_limit=None, time_limit=None, logging=False):
    return best_first_search(problem, frontier=aidm.search.frontier.LIFOQueue(),
                             termination_criteria=CriteriaGoalState(), prune_func=None,
                             closed_list=ClosedList(), iter_limit=iter_limit, time_limit=time_limit,
                             logging=logging)

def a_star(problem, heuristic_func, iter_limit=None, time_limit=None, logging=False):
    #f_func = lambda x: x.get_path_cost(problem)[0]+heuristic_func(x)
    f_func = lambda x: problem.evaluate(path=x.get_transition_path())+heuristic_func(x)
    return best_first_search(problem=problem, frontier=aidm.search.frontier.PriorityQueue(f_func),
                             termination_criteria=CriteriaGoalState(), prune_func=None,
                             closed_list=ClosedList(), iter_limit=iter_limit, time_limit=time_limit,
                             logging=logging)

def greedy_best_first_search(problem, heuristic_func, iter_limit=None, time_limit=None, logging=False):
    return best_first_search(problem=problem, frontier=aidm.search.frontier.PriorityQueue(heuristic_func),
                             termination_criteria=CriteriaGoalState(), prune_func=None,
                             closed_list=ClosedList(), iter_limit=iter_limit, time_limit=time_limit,
                             logging=logging)










