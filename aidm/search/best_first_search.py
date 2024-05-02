__author__ = 'sarah'

import aidm.search.frontier
from ..core.resources import ComputationalResources
from ..core.utils import logger, ClosedList, CriteriaGoalState
from .node import Node

def best_first_search(problem, frontier, termination_criteria=None, prune_func=None, use_closed_list=False,
                      is_anytime=False, iter_limit=None, time_limit=None, logging=False, depth_bound=None, sort_successors=True):
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
    root_node = Node(state=problem.get_current_state(),action=None, parent=None, value=0)
    # the frontier sets the order by which nodes are explored (e.g.FIFO, LIFO etc.)
    # we are assuming the root node is valid, i.e., it doesn't violate the constraints
    frontier.add(root_node, problem)
    # keep track of search resources
    resources=ComputationalResources(iteration_bound=iter_limit, time_bound=time_limit, depth_bound=depth_bound)
    #initiliaze closed list if relevant
    closed_list = ClosedList() if use_closed_list else None
    # keeping track of the best solution so far
    best_node = None
    try:

        while not frontier.is_empty():

            # get the current node and its value
            cur_node = frontier.extract()
            cur_value = cur_node.value
            if logging:logger.info('best_first_search resources %s cur_node:%s cur_value:%f' % (resources.__str__(),cur_node.__str__(), cur_value))


            # update resources (iteration count will advance by 1)
            # check resource limit has not been reached
            resources.update()
            if resources.are_exhausted(node=cur_node):
                if logging: logger.info('best_first_search: resources exhausted')
                if is_anytime and best_node:
                    return [best_node, best_plan, resources]
                else:
                    return [None, None, resources]

            # if the closed list was specified - check if this state should be explored again
            if closed_list:
                print('Closed list:\n')
                closed_list.print()
                # if the state is already in the closed list and a better value was found
                # extract it from the closed list
                if not closed_list.get(cur_node.state['key']) or problem.is_better(cur_value, closed_list.get(cur_node.state['key'])):
                    # update value in closed list
                    closed_list.add_or_update(key=cur_node.state['key'],value=cur_value)
                else:
                    continue


            # keep the best node so far
            if best_node is None or problem.is_better(cur_value, best_value):
                best_value = cur_value
                best_node  = cur_node
                best_plan  = best_node.get_transition_path_string()

            # check if termination criteria had been met - and stop the search if it has
            if termination_criteria:
                for criterion in termination_criteria:
                    if criterion.isTerminal(cur_node, problem):
                        plan = cur_node.get_transition_path_string()
                        if logging: logger.info('best_first_search: termination_criteria reached with solution %s' % (cur_node.get_transition_path_string()))
                        return [cur_node, plan, resources]

            # get the succsessor states of the state of the current node
            all_successors = problem.get_successors(state=cur_node.state)
            successors = []
            for action, outcomes in all_successors:
                for state,_ in outcomes:
                    new_node = Node(state, action, cur_node)
                    new_node.value = problem.evaluate(new_node.get_transition_path())
                    successors.append(new_node)

            # if pruning is applied - prune the set of successors
            if prune_func is not None:
                successors = prune_func(successors, cur_node)
            if sort_successors:
                # sort successors to make sure goal is reached at the same time for all approaches
                successors = sorted(successors, key=lambda x: x.get_transition_path_string(), reverse=False)

            # add successors to the frontier
            for child in successors:
                frontier.add(child,problem)
        if is_anytime:
            # search graph fully explored without finding a solution
            if logging: logger.info('best_first_search: returning best solution')
            return [best_node, best_plan, resources]

        else:
            # search graph fully explored without finding a solution
            if logging: logger.info('best_first_search: search graph fully explored without finding a solution')
            return [None, None, resources]

    except Exception as e:
        if logging: logger.info('best_first_search: exception occurred: %s'%str(e))
        raise e

def breadth_first_search(problem, use_closed_list=False, iter_limit=None, time_limit=None, logging=False):
    return best_first_search(problem, frontier=aidm.search.frontier.FIFOQueue(),
                             termination_criteria=[CriteriaGoalState()], prune_func=None, use_closed_list=use_closed_list,is_anytime=False,
                             iter_limit=iter_limit, time_limit=time_limit, depth_bound=None, logging=logging)

def depth_first_search(problem, use_closed_list=False, iter_limit=None, time_limit=None, logging=False):
    return best_first_search(problem, frontier=aidm.search.frontier.LIFOQueue(),
                             termination_criteria=[CriteriaGoalState()], prune_func=None, use_closed_list=use_closed_list, iter_limit=iter_limit,
                             time_limit=time_limit, depth_bound=None, logging=logging)

def depth_first_search_l(problem, depth_bound:int, use_closed_list=False, iter_limit=None, time_limit=None, logging=False):
    resources=None
    for l in range(depth_bound):
        [node, plan, resources] = best_first_search(problem, frontier=aidm.search.frontier.LIFOQueue(),
                             termination_criteria=[CriteriaGoalState()], prune_func=None,use_closed_list=use_closed_list, iter_limit=iter_limit,
                             time_limit=time_limit, depth_bound=l, logging=logging)
        if plan: return [node, plan, resources]
    # plan not found
    return [None, None, resources]

def a_star(problem, heuristic_func, use_closed_list=False, iter_limit=None, time_limit=None, logging=False):
    #f_func is equal to g+h
    f_func = lambda x,y: problem.evaluate(path=x.get_transition_path())+heuristic_func(x,y)
    return best_first_search(problem=problem, frontier=aidm.search.frontier.PriorityQueue(f_func),
                             termination_criteria=[CriteriaGoalState()], prune_func=None, use_closed_list=use_closed_list, iter_limit=iter_limit,
                             time_limit=time_limit, depth_bound=None, logging=logging)

def greedy_best_first_search(problem, heuristic_func, use_closed_list=False, iter_limit=None, time_limit=None, logging=False):
    # f_func is equal to h
    return best_first_search(problem=problem, frontier=aidm.search.frontier.PriorityQueue(heuristic_func),
                             termination_criteria=[CriteriaGoalState()], prune_func=None,use_closed_list=use_closed_list, iter_limit=iter_limit,
                             time_limit=time_limit, depth_bound=None, logging=logging)








