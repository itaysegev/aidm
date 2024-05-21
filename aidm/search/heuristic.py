__author__ = 'sarah'


def zero_heuristic(node,problem):
    return 0


def goal_heuristic(node,problem):
    if problem.is_goal_state(node.state):
        return 0
    else:
        return 1

