from aidm.core.problem import Problem
from aidm.core.utils import State, Action


# TODO: take care of transition function and the duplication of env for each node (and for the termination criteria)
class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual content for this node.
    Also specifies the transtion that got us to this state, and the total path_cost (also known as g) to reach the node.
    Other functions may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state:State, action:Action, parent=None, value=None):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.value = value
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state.__str__())

    def __lt__(self, node):
        return self.state.key < node.state.key

    def get_node_path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def get_transition_path(self):
        """Return a list of transitions (actions) forming the execution path from the root to this node."""
        node, path_back = self, []
        while node:
            state= node.parent.state if node.parent else None
            next_state= node.state
            path_back.append([state,node.action,next_state])
            node = node.parent
        return list(reversed(path_back))

    def get_transition_path_string(self):
        """Return a list of transitions forming the execution path from the root to this node."""
        node, path_back = self, []
        while node:
            action_name = 'None'
            if node.action is not None:
                action_name = node.action.__str__()
            if action_name != 'None':
                path_back.append(action_name)

            node = node.parent
        return list(reversed(path_back))


    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)
