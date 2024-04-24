__author__ = 'sarah'

from ..core import utils
from ..core.resources import ComputationalResources
from ..core.utils import logger, Node
from ..search import heuristic

def best_first_search(problem, frontier, closed_list=None, termination_criteria=None, prune_func=None, iter_limit=None, time_limit=None, logging=False):
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
       - constraints - prunes states that do not comply with the constraints
    """

    # init the search node
    root_node = Node(problem.get_current_state(), None, None)
    # the frontier sets the order by which nodes are explored (e.g.FIFO, LIFO etc.)
    # we are assuming the root node is valid, i.e., it doesn't violate the constraints
    frontier.add(root_node)

    # keeping the best value found so far
    best_value = None
    # keeping the best solution found so far
    best_node = None
    # counting number of explored nodes
    explored_count = 0
    # a flag used to indicate that the termination criteria has not yet been reached
    continue_search = True
    # false while there are still nodes to explore and the termination condition has not been met
    ex_terminated = False
    # if search resources have been defined, reset the count
    resources = None
    if iter_limit or time_limit:
        resources=ComputationalResources(iteration_bound=iter_limit, time_bound=time_limit)

    try:

        while not frontier.is_empty() and continue_search:

            # count explored nodes
            explored_count += 1

            # check resource limit has not been reached
            if resources and resources.are_exhausted():
                ex_terminated = True
                break

            # get the current node
            cur_node = frontier.extract()
            cur_value = problem.evaluate(cur_node)

            if logging:logger.info('best_first_search explored_count %d cur_node:%s' % (explored_count,cur_node))

            # add the node to the closed list
            if closed_list:
                closed_list.add(cur_node)

            if best_node is None or problem.is_better_or_equal(cur_value, best_value):
                best_value = cur_value
                best_node = cur_node

            # check if termination criteria had been met - and stop the search if it has
            if termination_criteria is not None and termination_criteria.isTerminal(best_node, best_value, problem):
                if logging: logger.info('best_first_search: termination_criteria reached')
                break

            # get the succsessor states of the state of the current node
            for state,action,_ in problem.get_successors(cur_node.state):
                successors.append(Node(state, action, cur_node) )

            # if pruning is applied - prune the set of successors
            if prune_func is not None:
                successors = prune_func(successors, cur_node)

            # sort successors to make sure goal is reached at the same time for all approaches
            successors = sorted(successors, key=lambda x: x.get_transition_path_string(), reverse=False)
            if logging: logger.info('best_first_search: succ_count:%d'% (len(successors)))

            # if there are no successors, move to next node, otherwise: evaluate each child
            if successors is None or len(successors) == 0:
                continue

            # add children to the frontier
            # if the closed list was specified - add it only if it's not already there
            for child in successors:
                already_in_closed_list = False
                if closed_list is not None:
                    if closed_list.is_in_list(child):
                        already_in_closed_list = True
                if not already_in_closed_list and child not in frontier:
                    frontier.add(child)
                    if closed_list:
                        closed_list.add(child)

        # return the best solution found
        if logging: logger.info('best_first_search: solution is: %s'%(best_node.get_transition_path_string()))
        best_plan = best_node.get_transition_path_string()
        return [best_value, best_node, best_plan, explored_count, ex_terminated]

    except Exception as e:
        if logging: logger.info('best_first_search: exception occurred: %s'%str(e))
        raise e

def breadth_first_search(problem, iter_limit=None, time_limit=None, logging=False):
    return best_first_search(problem, frontier=utils.FIFOQueue(), closed_list=utils.ClosedListOfKeys(),
                             termination_criteria=utils.TerminationCriteriaGoalStateReached(), prune_func=None,
                             iter_limit=iter_limit, time_limit=time_limit, logging=logging)

def depth_first_search(problem, iter_limit=None, time_limit=None, logging=False):
    return best_first_search(problem, frontier=utils.LIFOQueue(), closed_list=utils.ClosedListOfKeys(),
                             termination_criteria=utils.TerminationCriteriaGoalStateReached(), prune_func=None,
                             iter_limit=iter_limit, time_limit=time_limit, logging=logging)

def depth_first_search_l(problem, max_depth, iter_limit=None, time_limit=None, logging=False):
    return best_first_search(problem, frontier=utils.LIFOQueue(), closed_list=utils.ClosedListOfKeys(),
                             termination_criteria=utils.TerminationCriteriaGoalStateReached(), prune_func=None,
                             iter_limit=iter_limit, time_limit=time_limit, logging=logging)

def a_star(problem, heuristic_func=heuristic, iter_limit=None, time_limit=None, logging=False):
    f_func = lambda x: x.get_path_cost(problem)[0]+heuristic_func(x)
    return best_first_search(problem=problem, frontier=utils.PriorityQueue(f_func),
                             closed_list=utils.ClosedListOfKeys(),
                             termination_criteria=utils.TerminationCriteriaGoalStateReached(), prune_func=None,
                             iter_limit=iter_limit, time_limit=time_limit, logging=logging)


def greedy_best_first_search(problem, heuristic_func, iter_limit=None, time_limit=None, logging=False):
    return best_first_search(problem=problem, frontier=utils.PriorityQueue(heuristic_func),
                             closed_list=utils.ClosedListOfKeys(),
                             termination_criteria=utils.TerminationCriteriaGoalStateReached(), prune_func=None,
                             iter_limit=iter_limit, time_limit=time_limit, logging=logging)










